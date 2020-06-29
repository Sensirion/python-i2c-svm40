# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest
import time


@pytest.mark.needs_device
def test(device):
    """
    Test if start_measurement() and stop_measurement() work as expected.
    """

    # start continuous measurement and make sure it worked
    device.start_measurement()
    time.sleep(1.)
    voc_index, humidity, temperature = device.read_measured_values()
    assert humidity.percent_rh > 0

    # stop and restart measurement
    device.stop_measurement()
    voc_index, humidity, temperature = device.read_measured_values()
    assert humidity.percent_rh == 0
    device.start_measurement()
    time.sleep(1.)
    voc_index, humidity, temperature = device.read_measured_values()
    assert humidity.percent_rh > 0
