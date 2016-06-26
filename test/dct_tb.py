from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.common import *
from litejpeg.core.dct import *
from test.common import DCTData

dw = 12
ds = 64

omit_table = ["dct_" + str(i) for i in range(ds)]

class TB(Module):
    def __init__(self):
        self.submodules.streamer = PacketStreamer(EndpointDescription( [(  ["data", dw*ds])]  ))
        self.submodules.DCT = DCT()
        self.submodules.logger = PacketLogger(EndpointDescription( [(  ["data", dw*ds])]  ))

        self.comb += [
            Record.connect(self.streamer.source, self.DCT.sink, omit=["data"]),
            Record.connect(self.DCT.source, self.logger.sink, omit=omit_table),
         ]

        for i in range(ds):
            name = "dct_" + str(i)
            self.comb += getattr(self.DCT.sink.payload, name).eq(self.streamer.source.data[i*dw:(i+1)*dw])
            self.comb += self.logger.sink.data[i*dw:(i+1)*dw].eq(getattr(self.DCT.source,name))


def main_generator(dut):
    model =  DCTData(ds,dw)
    paralell_packet = [model.pack_dct()]
    packet = Packet(paralell_packet)

    for i in range(1):
        dut.streamer.send(packet)
        yield from dut.logger.receive()
        print(dut.logger.packet)
        print(model.output_dct)
        print(model.output_dct_model)

if __name__ == "__main__":
    tb = TB()
    generators = {"sys": [main_generator(tb)]}
    generators = {
        "sys": [main_generator(tb),
                tb.streamer.generator(),
                tb.logger.generator()]
    }
    clocks = {"sys": 10}
    run_simulation(tb, generators, clocks, vcd_name="dct.vcd")
