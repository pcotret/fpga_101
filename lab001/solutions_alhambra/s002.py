#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led",  0, Pins("45"), IOStandard("LVCMOS33")),
    ("clk12", 0, Pins("49"), IOStandard("LVCMOS33")),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk12"
    default_clk_period = 1e9/12e6

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-hx8k-tq144:4k", _io, toolchain="icestorm")

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)
platform = Platform()

# Create our module (fpga description)
class Blink(Module):
    def __init__(self, blink_freq, sys_clk_freq, led):
        counter = Signal(32)
        # synchronous assignments
        self.sync += [
            counter.eq(counter + 1),
            If(counter == int((sys_clk_freq/blink_freq)/8 - 1),
                counter.eq(0),
                led.eq(~led)
            )
        ]
        # combinatorial assignements
        self.comb += []

module = Blink(1, 100e6, platform.request("user_led"))

# Build --------------------------------------------------------------------------------------------

platform.build(module)

