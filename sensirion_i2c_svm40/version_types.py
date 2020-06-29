# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

import logging
log = logging.getLogger(__name__)


class FirmwareVersion(object):
    """
    Class representing the firmware version of a device.
    """

    def __init__(self, major, minor, debug):
        """
        Constructor.

        :param byte major: Major version (0..255).
        :param byte minor: Minor version (0..99).
        :param bool debug: Debug flag (False for official releases).
        """
        super(FirmwareVersion, self).__init__()
        self.major = major
        self.minor = minor
        self.debug = debug

    def __str__(self):
        return '{}.{}{}'.format(self.major, self.minor,
                                self.debug and '-debug' or '')


class HardwareVersion(object):
    """
    Class representing the hardware version of a device.
    """

    def __init__(self, major, minor):
        """
        Constructor.

        :param byte major: Major version (0..255).
        :param byte minor: Minor version (0..99).
        """
        super(HardwareVersion, self).__init__()
        self.major = major
        self.minor = minor

    def __str__(self):
        return '{}.{}'.format(self.major, self.minor)


class ProtocolVersion(object):
    """
    Class representing the I2C protocol version of an I2C device.
    """

    def __init__(self, major, minor):
        """
        Constructor.

        :param byte major: Major version (0..255).
        :param byte minor: Minor version (0..99).
        """
        super(ProtocolVersion, self).__init__()
        self.major = major
        self.minor = minor

    def __str__(self):
        return '{}.{}'.format(self.major, self.minor)


class Version(object):
    """
    Class representing all version numbers of an I2C device. This is used for
    the "Get Version" command.
    """

    def __init__(self, firmware, hardware, protocol):
        """
        Constructor.

        :param ~sensirion_i2c_svm40.version_types.FirmwareVersion firmware:
            Firmware version.
        :param ~sensirion_i2c_svm40.version_types.HardwareVersion hardware:
            Hardware version.
        :param ~sensirion_i2c_svm40.version_types.ProtocolVersion protocol:
            SHDLC protocol version.
        """
        super(Version, self).__init__()
        self.firmware = firmware
        self.hardware = hardware
        self.protocol = protocol

    def __str__(self):
        return 'Firmware {}, Hardware {}, Protocol {}'.format(
            self.firmware, self.hardware, self.protocol
        )
