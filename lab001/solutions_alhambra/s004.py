#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led",  0, Pins("45"), IOStandard("LVCMOS33")),
    ("user_led",  1, Pins("44"), IOStandard("LVCMOS33")),
    ("user_led",  2, Pins("43"), IOStandard("LVCMOS33")),
    ("user_led",  3, Pins("42"), IOStandard("LVCMOS33")),
    ("user_led",  4, Pins("41"), IOStandard("LVCMOS33")),
    ("user_led",  5, Pins("39"), IOStandard("LVCMOS33")),
    ("user_led",  6, Pins("38"), IOStandard("LVCMOS33")),
    ("user_led",  7, Pins("37"), IOStandard("LVCMOS33")),

    ("user_sw",  0, Pins("34"), IOStandard("LVCMOS33")),
    ("user_sw",  1, Pins("33"), IOStandard("LVCMOS33")),

    ("clk12", 0, Pins("49"), IOStandard("LVCMOS33")),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name = "clk12"
    default_clk_period = 10.0

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-hx8k-tq144:4k", _io, toolchain="icestorm")

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)
platform = Platform()

# Create our module (fpga description)
class Switches(Module):
    def __init__(self, platform):     
        # synchronous assignments
        self.sync += []
        # combinatorial assignements
        sw = platform.request("user_sw", 0)
        for i in range(0, 4):
            led = platform.request("user_led", i)
            self.comb += led.eq(~sw)
        sw = platform.request("user_sw", 1)
        for i in range(4,8):
            led = platform.request("user_led", i)
            self.comb += led.eq(sw)

module = Switches(platform)

# Build --------------------------------------------------------------------------------------------

platform.build(module)

