from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.common import *
from litejpeg.core.dct import DCT

input_pixel = [140, 144, 147, 140, 140, 155, 179, 175, 144, 152, 140, 147, 140, 148, 167, 179, 152, 155, 136, 167, 163,
               162, 152, 172, 168, 145, 156, 160, 152, 155, 136, 160, 162, 148, 156, 148, 140, 136, 147, 162, 147, 167,
               140, 155, 155, 140, 136, 162, 136, 156, 123, 167, 162, 144, 140, 147, 148, 155, 136, 155, 152, 147, 147,
               136]

output_dct = [186, -18, 15, -9, 23, -9, -14, 19, 21, -34, 26, -9, -11, 11, 14, 7, -10, -24, -2, 6, -18, 3, -20, -1, -8,
              -5, 14, -15, -8, -3, -3, 8, -3, 10, 8, 1, -11, 18, 18, 15, 4, -2, -18, 8, 8, -4, 1, -7, 9, 1, -3, 4, -1,
              -7, -1, -2, 0, -8, -2, 2, 1, 4, -6, 0]


class TB(Module):
    def __init__(self):
        self.submodules.streamer = PacketStreamer(EndpointDescription([("data", 8*64)]))
        self.submodules.DCT1D = DCT()
        self.submodules.logger = PacketLogger(EndpointDescription([("data", 8*64)]))


        self.comb += [
            self.streamer.source.connect(self.DCT.sink),
            self.DCT.source.connect(self.logger.sink)
        ]
        self.comb += [
            Record.connect(self.streamer.source, self.DCT.sink, omit=["data"]),
            self.DCT.sink.payload.eq(self.streamer.source.data[16:24]) ,


            Record.connect(self.DCT.source, self.logger.sink, omit=["data"]),
            self.logger.sink.data[16:24].eq(self.DCT.source)
        ]

def main_generator(dut):

    packet = Packet(input_pixel)
    for i in range(1):
        dut.streamer.send(packet)
        yield from dut.logger.receive()
        print(dut.logger.packet)
        print(output_dct)


if __name__ == "__main__":
    tb = TB()
    generators = {"sys": [main_generator(tb)]}
    generators = {
        "sys": [main_generator(tb),
                tb.streamer.generator(),
                tb.logger.generator()]
    }
    clocks = {"sys": 10}
    run_simulation(tb, generators, clocks, vcd_name="sim.vcd")
