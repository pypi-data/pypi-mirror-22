from hwt.hdlObjects.constants import READ, WRITE, NOP
from hwt.simulator.agentBase import SyncAgentBase
from hwt.simulator.shortcuts import oscilate


class BramPort_withoutClkAgent(SyncAgentBase):
    """
    :ivar requests: list of tuples (request type, address, [write data]) - used for driver
    :ivar data: list of data in memory, used for monitor
    :ivar mem: if agent is in monitor mode (= is slave) all reads and writes are performed on
        mem object
    """
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=clk, rstn=rstn, allowNoReset=True)

        self.requests = []
        self.readPending = False
        self.readed = []

        self.mem = {}

    def doReq(self, s, req):
        rw = req[0]
        addr = req[1]

        if rw == READ:
            rw = 0
            wdata = None
            self.readPending = True

        elif rw == WRITE:
            wdata = req[2]
            rw = 1
        else:
            raise NotImplementedError(rw)

        intf = self.intf
        s.w(rw, intf.we)
        s.w(addr, intf.addr)
        s.w(wdata, intf.din)

    def onReadReq(self, s, addr):
        """
        on readReqRecieved in monitor mode
        """
        self.requests.append((READ, addr))

    def onWriteReq(self, s, addr, data):
        """
        on writeReqRecieved in monitor mode
        """
        self.requests.append((WRITE, addr, data))

    def monitor(self, s):
        intf = self.intf

        yield s.updateComplete

        if self.requests:
            req = self.requests.pop(0)
            t = req[0]
            addr = req[1]
            assert addr._isFullVld(), s.now
            if t == READ:
                s.write(self.mem[addr.val], intf.dout)
            else:
                assert t == WRITE
                s.write(None, intf.dout)
                self.mem[addr.val] = req[2]

        if self.enable:
            en = s.read(intf.en)
            assert en.vldMask
            if en.val:
                we = s.read(intf.we)
                assert we.vldMask

                addr = s.read(intf.addr)
                if we.val:
                    data = s.read(intf.din)
                    self.onWriteReq(s, addr, data)
                else:
                    self.onReadReq(s, addr)

    def getDrivers(self):
        return [self.driver]

    def driver(self, s):
        intf = self.intf
        readPending = self.readPending
        if self.requests and self.enable:
            req = self.requests.pop(0)
            if req is NOP:
                s.w(0, intf.en)
                s.w(0, intf.we)
                self.readPending = False
            else:
                self.doReq(s, req)
                s.w(1, intf.en)
        else:
            s.w(0, intf.en)
            s.w(0, intf.we)
            self.readPending = False

        if readPending:
            yield s.updateComplete
            d = s.r(intf.dout)
            self.readed.append(d)


class BramPortAgent(BramPort_withoutClkAgent):
    def __init__(self, intf, clk=None, rstn=None):
        if clk is None:
            clk = intf.clk
        super().__init__(intf, clk=clk, rstn=rstn)

    def getDrivers(self):
        drivers = super(BramPortAgent, self).getDrivers()
        drivers.append(oscilate(self.intf.clk))
        return drivers
