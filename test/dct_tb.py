from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.common import *
from litejpeg.core.dct import *

dw = 12
ds = 64

input_pixel = [140, 144, 147, 140, 140, 155, 179, 175, 144, 152, 140, 147, 140, 148, 167, 179, 152, 155, 136, 167, 163,
               162, 152, 172, 168, 145, 156, 160, 152, 155, 136, 160, 162, 148, 156, 148, 140, 136, 147, 162, 147, 167,
               140, 155, 155, 140, 136, 162, 136, 156, 123, 167, 162, 144, 140, 147, 148, 155, 136, 155, 152, 147, 147,
               136]

output_dct_model = [186, -18, 15, -9, 23, -9, -14, 19, 21, -34, 26, -9, -11, 11, 14, 7, -10, -24, -2, 6, -18, 3, -20, -1, -8,
              -5, 14, -15, -8, -3, -3, 8, -3, 10, 8, 1, -11, 18, 18, 15, 4, -2, -18, 8, 8, -4, 1, -7, 9, 1, -3, 4, -1,
              -7, -1, -2, 0, -8, -2, 2, 1, 4, -6, 0]

omit_table = ["dct_" + str(i) for i in range(ds)]

class TB(Module):
    def __init__(self):
        self.submodules.streamer = PacketStreamer(EndpointDescription(dct_block_layout(dw,ds)))
        self.submodules.DCT = DCT()
        self.submodules.logger = PacketLogger(EndpointDescription(dct_block_layout(dw,ds)))


        self.comb += [
            self.streamer.source.connect(self.DCT.sink),
            self.DCT.source.connect(self.logger.sink)
        ]

        for i in range(ds):
            name = "dct_" + str(i)
            #self.comb += getattr(self.DCT.sink.payload, name)[0:12].eq(self.streamer.source)
            #self.comb += getattr(self.logger.sink, name).eq(self.DCT.source)

        self.comb += [
            Record.connect(self.streamer.source, self.DCT.sink, omit=omit_table ),
            Record.connect(self.DCT.source, self.logger.sink, omit=omit_table )
        ]

def main_generator(dut):

    packet = Packet(input_pixel)
    for i in range(1):
        dut.streamer.send(packet)
        yield from dut.logger.receive()
        print(dut.logger.packet)
        print(output_dct_model)


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
