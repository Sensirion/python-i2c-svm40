# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import SensirionI2cCommand, CrcCalculator
from .response_types import AirQuality, Humidity, Temperature
from .version_types import FirmwareVersion, HardwareVersion, ProtocolVersion, \
    Version
from struct import unpack


class Svm40I2cCmdBase(SensirionI2cCommand):
    """
    SVM40 I²C base command.
    """

    def __init__(self, command, tx_data, rx_length, read_delay, timeout,
                 post_processing_time=0.0):
        """
        Constructs a new SVM40 I²C command.

        :param int/None command:
            The command ID to be sent to the device. None means that no
            command will be sent, i.e. only ``tx_data`` (if not None) will
            be sent. No CRC is added to these bytes since the command ID
            usually already contains a CRC.
        :param bytes-like/list/None tx_data:
            Bytes to be extended with CRCs and then sent to the I²C device.
            None means that no write header will be sent at all (if ``command``
            is None too). An empty list means to send the write header (even if
            ``command`` is None), but without data following it.
        :param int/None rx_length:
            Number of bytes to be read from the I²C device, including CRC
            bytes. None means that no read header is sent at all. Zero means
            to send the read header, but without reading any data.
        :param float read_delay:
            Delay (in Seconds) to be inserted between the end of the write
            operation and the beginning of the read operation. This is needed
            if the device needs some time to prepare the RX data, e.g. if it
            has to perform a measurement. Set to 0.0 to indicate that no delay
            is needed, i.e. the device does not need any processing time.
        :param float timeout:
            Timeout (in Seconds) to be used in case of clock stretching. If the
            device stretches the clock longer than this value, the transceive
            operation will be aborted with a timeout error. Set to 0.0 to
            indicate that the device will not stretch the clock for this
            command.
        :param float post_processing_time:
            Maximum time in seconds the device needs for post processing of
            this command until it is ready to receive the next command. For
            example after a device reset command, the device might need some
            time until it is ready again. Usually this is 0.0s, i.e. no post
            processing is needed.
        """
        super(Svm40I2cCmdBase, self).__init__(
            command=command,
            tx_data=tx_data,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=timeout,
            crc=CrcCalculator(8, 0x31, 0xFF),
            command_bytes=2,
            post_processing_time=post_processing_time,
        )


class Svm40I2cCmdGetSerialNumber(Svm40I2cCmdBase):
    """
    SVM40 command to get the serial number.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdGetSerialNumber, self).__init__(
            command=0xD033,
            tx_data=b'',
            rx_length=39,
            read_delay=0.001,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
        :return: The serial number as a hex formatted ASCII string.
        :rtype: string
        """
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        return str(checked_data.decode('utf-8').rstrip('\0'))


class Svm40I2cCmdDeviceReset(Svm40I2cCmdBase):
    """
    SVM40 command to get the product name.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdDeviceReset, self).__init__(
            command=0xD304,
            tx_data=b'',
            rx_length=None,
            read_delay=0.,
            timeout=0.,
            post_processing_time=0.1,
        )


class Svm40I2cCmdGetVersion(Svm40I2cCmdBase):
    """
    SVM40 command to get the device version.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdGetVersion, self).__init__(
            command=0xD100,
            tx_data=b'',
            rx_length=12,
            read_delay=0.001,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
        :return: The version of the device.
        :rtype: ~sensirion_i2c_svm40.version_types.Version
        """
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        firmware_major, firmware_minor, firmware_debug, hardware_major, \
            hardware_minor, protocol_major, protocol_minor = \
            unpack(">BB?BBBBx", checked_data)
        return Version(
            FirmwareVersion(
                major=firmware_major,
                minor=firmware_minor,
                debug=firmware_debug
            ),
            hardware=HardwareVersion(
                major=hardware_major,
                minor=hardware_minor,
            ),
            protocol=ProtocolVersion(
                major=protocol_major,
                minor=protocol_minor
            )
        )


class Svm40I2cCmdStartMeasurement(Svm40I2cCmdBase):
    """
    SVM40 command to starts the continuous measurement in polling mode.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdStartMeasurement, self).__init__(
            command=0x0010,
            tx_data=b'',
            rx_length=None,
            read_delay=0.,
            timeout=0.,
            post_processing_time=0.001,
        )


class Svm40I2cCmdStopMeasurement(Svm40I2cCmdBase):
    """
    SVM40 command to leave the measurement mode and go to idle mode.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdStopMeasurement, self).__init__(
            command=0x0104,
            tx_data=b'',
            rx_length=None,
            read_delay=0.,
            timeout=0.,
            post_processing_time=0.05,
        )


class Svm40I2cCmdReadMeasuredValuesAsIntegers(Svm40I2cCmdBase):
    """
    SVM40 command to get the the new measurement results as integers.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdReadMeasuredValuesAsIntegers, self).__init__(
            command=0x03A6,
            tx_data=b'',
            rx_length=9,
            read_delay=0.001,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
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
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        air_quality_ticks, humidity_ticks, temperature_ticks = \
            unpack(">3h", checked_data)
        return AirQuality(air_quality_ticks), \
            Humidity(humidity_ticks), \
            Temperature(temperature_ticks)


class Svm40I2cCmdReadMeasuredValuesAsIntegersWithRaw(Svm40I2cCmdBase):
    """
    SVM40 command to get the the new measurement results as integers with raw
    values added.
    """

    def __init__(self):
        """
        Constructs a new command.
        """
        super(Svm40I2cCmdReadMeasuredValuesAsIntegersWithRaw, self).__init__(
            command=0x03B0,
            tx_data=b'',
            rx_length=18,
            read_delay=0.001,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
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
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        air_quality_ticks, humidity_ticks, temperature_ticks,\
            raw_voc_ticks, raw_humidity_ticks, raw_temperature_ticks = \
            unpack(">6h", checked_data)
        return AirQuality(air_quality_ticks), \
            Humidity(humidity_ticks), \
            Temperature(temperature_ticks), \
            raw_voc_ticks, \
            Humidity(raw_humidity_ticks), \
            Temperature(raw_temperature_ticks)
