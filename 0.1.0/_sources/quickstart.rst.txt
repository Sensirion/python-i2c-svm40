Quick Start
===========

In order to correctly select I²C as interface, the interface select pin must be
pulled low to GND before or at the same time the sensor is powered up.

Linux I²C Bus Example
---------------------

Following example code shows how to use this driver with a Sensirion SVM40
connected to a Linux I²C bus (e.g. Raspberry Pi).


.. sourcecode:: python

    import time
    from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
    from sensirion_i2c_svm40 import Svm40I2cDevice


    with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
        device = Svm40I2cDevice(I2cConnection(i2c_transceiver))
        device.device_reset()

        # Print some device information
        print("Version: {}".format(device.get_version()))
        print("Serial Number: {}".format(device.get_serial_number()))

        # Start measurement
        device.start_measurement()
        print("Measurement started... ")
        while True:
            time.sleep(10.)
            air_quality, humidity, temperature = device.read_measured_values()
            # use default formatting for printing output:
            print("{}, {}, {}".format(air_quality, humidity, temperature))


SensorBridge Example
--------------------

Following example code shows how to use this driver with a Sensirion SVM40
connected to the computer using a `Sensirion SEK-SensorBridge`_. The driver
for the SensorBridge can be installed with
``pip install sensirion-shdlc-sensorbridge``.


.. sourcecode:: python

    import time
    from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
    from sensirion_shdlc_sensorbridge import SensorBridgePort, \
        SensorBridgeShdlcDevice, SensorBridgeI2cProxy
    from sensirion_i2c_driver import I2cConnection
    from sensirion_i2c_svm40 import Svm40I2cDevice

    # Connect to the SensorBridge with default settings:
    #  - baudrate:      460800
    #  - slave address: 0
    with ShdlcSerialPort(port='COM1', baudrate=460800) as port:
        bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
        print("SensorBridge SN: {}".format(bridge.get_serial_number()))

        # Configure SensorBridge port 1 for SVM40
        bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
        bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
        bridge.switch_supply_on(SensorBridgePort.ONE)

        # Create SVM40 device
        i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
        device = Svm40I2cDevice(I2cConnection(i2c_transceiver))

        # Print some device information
        print("Version: {}".format(device.get_version()))
        print("Serial Number: {}".format(device.get_serial_number()))

        # Start measurement
        device.start_measurement()
        print("Measurement started... ")
        while True:
            time.sleep(10.)
            air_quality, humidity, temperature = device.read_measured_values()
            # use default formatting for printing output:
            print("{}, {}, {}".format(air_quality, humidity, temperature))


.. _Sensirion SEK-SensorBridge: https://www.sensirion.com/sensorbridge/
