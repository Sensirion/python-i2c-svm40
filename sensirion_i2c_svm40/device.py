# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import I2cDevice
from .commands import Svm40I2cCmdGetSerialNumber, Svm40I2cCmdDeviceReset, \
    Svm40I2cCmdGetVersion, Svm40I2cCmdStartContinuousMeasurement, \
    Svm40I2cCmdStopMeasurement, Svm40I2cCmdReadMeasuredValues, \
    Svm40I2cCmdReadMeasuredValuesRaw, \
    Svm40I2cCmdGetTemperatureOffsetForRhtMeasurements, \
    Svm40I2cCmdSetTemperatureOffsetForRhtMeasurements, \
    Svm40I2cCmdGetVocAlgorithmTuningParameters, \
    Svm40I2cCmdSetVocAlgorithmTuningParameters, \
    Svm40I2cCmdGetVocAlgorithmState, Svm40I2cCmdSetVocAlgorithmState, \
    Svm40I2cCmdStoreNvData


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

    def get_compensation_temperature_offset(self):
        """
        Gets the temperature offset for RHT measurements.

        :return: Temperature offset in degrees celsius.
        :rtype: float
        """
        return self.execute(
            Svm40I2cCmdGetTemperatureOffsetForRhtMeasurements())

    def set_compensation_temperature_offset(self, t_offset):
        """
        Sets the temperature offset for RHT measurements.

        .. note:: Execute the command
            :py:meth:`~sensirion_i2c_svm40.device.store_nv_data` command
            after writing the parameter to store it in the non-volatile memory
            of the device otherwise the parameter will be reset upton a device
            reset.

        :param float t_offset: Temperature offset in degrees celsius.
        """
        return self.execute(
            Svm40I2cCmdSetTemperatureOffsetForRhtMeasurements(t_offset))

    def get_voc_tuning_parameters(self):
        """
        Gets the currently set parameters for customizing the VOC algorithm.

        :return:
            - voc_index_offset (int) -
              VOC index representing typical (average) conditions. The default
              value is 100.
            - learning_time_hours (int) -
              Time constant of long-term estimator in hours. Past events will
              be forgotten after about twice the learning time. The default
              value is 12 hours.
            - gating_max_duration_minutes (int) -
              Maximum duration of gating in minutes (freeze of estimator during
              high VOC index signal). Zero disables the gating. The default
              value is 180 minutes.
            - std_initial (int) -
              Initial estimate for standard deviation. Lower value boosts
              events during initial learning period, but may result in larger
              device-to-device variations. The default value is 50.
        :rtype: tuple
        """
        return self.execute(Svm40I2cCmdGetVocAlgorithmTuningParameters())

    def set_voc_tuning_parameters(self, voc_index_offset, learning_time_hours,
                                  gating_max_duration_minutes, std_initial):
        """
        Sets parameters to customize the VOC algorithm. This command is only
        available in idle mode.

        .. note:: Execute the command
                  :py:meth:`~sensirion_i2c_svm40.device.store_nv_data` after
                  writing the parameter to store it in the non-volatile memory
                  of the device otherwise the parameter will be reset upton a
                  device reset.

        :param int voc_index_offset:
            VOC index representing typical (average) conditions. The default
            value is 100.
        :param int learning_time_hours:
            Time constant of long-term estimator in hours. Past events will be
            forgotten after about twice the learning time. The default value is
            12 hours.
        :param int gating_max_duration_minutes:
            Maximum duration of gating in minutes (freeze of estimator during
            high VOC index signal). Set to zero to disable the gating. The
            default value is 180 minutes.
        :param int std_initial:
            Initial estimate for standard deviation. Lower value boosts events
            during initial learning period, but may result in larger
            device-to-device variations. The default value is 50.
        """
        return self.execute(Svm40I2cCmdSetVocAlgorithmTuningParameters(
            voc_index_offset, learning_time_hours, gating_max_duration_minutes,
            std_initial))

    def store_nv_data(self):
        """
        Stores all customer engine parameters to the non-volatile memory.
        """
        return self.execute(Svm40I2cCmdStoreNvData())

    def get_voc_state(self):
        """
        Gets the current VOC algorithm state. Retrieved values can be used to
        set the VOC algorithm state to resume operation after a short
        interruption, skipping initial learning phase. This command is only
        available during measurement mode.

        .. note:: This feature can only be used after at least 3 hours of
                  continuous operation.

        :return: Current VOC algorithm state.
        :rtype: list(int)
        """
        return self.execute(Svm40I2cCmdGetVocAlgorithmState())

    def set_voc_state(self, state):
        """
        Set previously retrieved VOC algorithm state to resume operation after
        a short interruption, skipping initial learning phase. This command is
        only available in idle mode.

        .. note:: This feature should not be used after interruptions of more
                  than 10 minutes.

        :param list(int) state: Current VOC algorithm state.
        """
        return self.execute(Svm40I2cCmdSetVocAlgorithmState(state))

    def start_measurement(self):
        """
        Starts continuous measurement in polling mode.

        .. note:: This command is only available in idle mode.
        """
        return self.execute(Svm40I2cCmdStartContinuousMeasurement())

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
        return self.execute(Svm40I2cCmdReadMeasuredValues())

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
        return self.execute(Svm40I2cCmdReadMeasuredValuesRaw())
