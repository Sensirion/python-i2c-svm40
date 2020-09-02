# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import I2cDevice
from .commands import Svm40I2cCmdGetSerialNumber, Svm40I2cCmdDeviceReset, \
    Svm40I2cCmdGetVersion, Svm40I2cCmdStartMeasurement, \
    Svm40I2cCmdStopMeasurement, Svm40I2cCmdReadMeasuredValuesAsIntegers, \
    Svm40I2cCmdReadMeasuredValuesAsIntegersWithRaw


class Svm40I2cDevice(I2cDevice):
    """
    SVM40 I²C device class to allow executing I²C commands.
    """

    def __init__(self, connection, slave_address=0x6A):
        """
        Constructs a new SVM40 I²C device.

        :param ~sensirion_i2c_driver.connection.I2cConnection connection:
            The I²C connection to use for communication.
        :param byte slave_address:
            The I²C slave address, defaults to 0x6A.
        """
        super(Svm40I2cDevice, self).__init__(connection, slave_address)

    def device_reset(self):
        """
        Execute a device reset (reboot firmware, similar to power cycle).
        """
        return self.execute(Svm40I2cCmdDeviceReset())

    def get_serial_number(self):
        """
        Get the serial number of the device.

        :return: The serial number as a hex formatted ASCII string.
        :rtype: string
        """
        return self.execute(Svm40I2cCmdGetSerialNumber())

    def get_version(self):
        """
        Get the version of the device firmware, hardware and SHDLC protocol.

        :return: The device version.
        :rtype: ~sensirion_i2c_svm40.response_types.Version
        """
        return self.execute(Svm40I2cCmdGetVersion())

    def start_measurement(self):
        """
        Starts continuous measurement in polling mode.

        .. note:: This command is only available in idle mode.
        """
        return self.execute(Svm40I2cCmdStartMeasurement())

    def stop_measurement(self):
        """
        Leaves the measurement mode and returns to the idle mode.

        .. note:: This command is only available in measurement mode.
        """
        return self.execute(Svm40I2cCmdStopMeasurement())

    def read_measured_values(self):
        """
        Returns the new measurement results.

        .. note:: This command is only available in measurement mode. The
                  firmware updates the measurement values every second. Polling
                  data with a faster sampling rate will return the same values.
                  The first measurement is available 1 second after the start
                  measurement command is issued. Any readout prior to this will
                  return zero initialized values.

        :return:
            The measured air quality, humidity and temperature.

            - air_quality (:py:class:`~sensirion_i2c_svm40.response_types.AirQuality`) -
              Air quality response object.
            - humidity (:py:class:`~sensirion_i2c_svm40.response_types.Humidity`) -
              Humidity response object.
            - temperature (:py:class:`~sensirion_i2c_svm40.response_types.Temperature`) -
              Temperature response object.
        :rtype:
            tuple
        """  # noqa: E501
        return self.execute(Svm40I2cCmdReadMeasuredValuesAsIntegers())

    def read_measured_values_raw(self):
        """
        Returns the new measurement results with raw values added.

        .. note:: This command is only available in measurement mode. The
                  firmware updates the measurement values every second. Polling
                  data with a faster sampling rate will return the same values.
                  The first measurement is available 1 second after the start
                  measurement command is issued. Any readout prior to this will
                  return zero initialized values.

        :return:
            The measured air quality, humidity and temperature including the
            raw values without algorithm compensation.

            - air_quality (:py:class:`~sensirion_i2c_svm40.response_types.AirQuality`) -
              Air quality response object.
            - humidity (:py:class:`~sensirion_i2c_svm40.response_types.Humidity`) -
              Humidity response object.
            - temperature (:py:class:`~sensirion_i2c_svm40.response_types.Temperature`) -
              Temperature response object.
            - raw_voc_ticks (int) -
              Raw VOC output ticks as read from the SGP sensor.
            - raw_humidity (:py:class:`~sensirion_i2c_svm40.response_types.Humidity`) -
              Humidity response object.
            - raw_temperature (:py:class:`~sensirion_i2c_svm40.response_types.Temperature`) -
              Temperature response object.
        :rtype:
            tuple
        """  # noqa: E501
        return self.execute(Svm40I2cCmdReadMeasuredValuesAsIntegersWithRaw())
