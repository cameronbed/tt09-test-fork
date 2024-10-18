# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random


@cocotb.test()
async def test_project(dut):
    """Test the Kogge-Stone Adder for 1000 cases"""

    # Initialize the clock with a 100KHz frequency
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Ensure reset is not active
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Function to compute expected sum and carry
    def kogge_stone_adder(a, b):
        result = a + b
        sum_val = result & 0xF  # 4-bit sum
        carry_out = (result >> 4) & 1  # 1-bit carry-out
        return sum_val, carry_out

    # Run 1000 random test cases
    for _ in range(1000):
        # Randomly generate 4-bit inputs for `a` and `b`
        a_val = random.randint(0, 15)
        b_val = random.randint(0, 15)

        # Set the inputs in the DUT
        dut.a.value = a_val
        dut.b.value = b_val

        # Wait for a few clock cycles
        await ClockCycles(dut.clk, 10)

        # Compute expected values
        expected_sum, expected_carry = kogge_stone_adder(a_val, b_val)

        # Log the values and assert correctness
        dut._log.info(f"Testing inputs a={a_val}, b={b_val}")
        dut._log.info(f"Expected sum={expected_sum}, carry_out={expected_carry}")
        
        # Check if the DUT output matches the expected results
        assert dut.sum.value == expected_sum, f"Sum mismatch: Expected {expected_sum}, Got {dut.sum.value}"
        assert dut.carry_out.value == expected_carry, f"Carry mismatch: Expected {expected_carry}, Got {dut.carry_out.value}"
    
    dut._log.info("All 1000 test cases passed.")
