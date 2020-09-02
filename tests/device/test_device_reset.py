# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest
import time


@pytest.mark.needs_device
def test(device):
    """
    Test if device_reset() works as expected by changing a volatile setting,
    perform the reset, and then verifying that the setting was reset to its
    default value.
    """
    # start continuous measurement and make sure it worked
    device.start_measurement()
    time.sleep(1.)
    voc_index, humidity, temperature = device.read_measured_values()
    assert humidity.percent_rh > 0

    # reset device -> device should exit the measurement mode
    device.device_reset()

    # check that we are not in measurement mode - expect zero for all values
    time.sleep(1.)
    voc_index, humidity, temperature = device.read_measured_values()
    assert humidity.percent_rh == 0.
