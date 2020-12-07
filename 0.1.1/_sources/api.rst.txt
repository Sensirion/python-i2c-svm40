API Reference
=============


Svm40I2cDevice
--------------

.. automodule:: sensirion_i2c_svm40.device


Response Data Types
-------------------

Air Quality
^^^^^^^^^^^

.. autoclass:: sensirion_i2c_svm40.response_types.AirQuality

Humidity
^^^^^^^^

.. autoclass:: sensirion_i2c_svm40.response_types.Humidity

Temperature
^^^^^^^^^^^

.. autoclass:: sensirion_i2c_svm40.response_types.Temperature

Version
^^^^^^^

.. automodule:: sensirion_i2c_svm40.version_types


Commands
--------

.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdGetSerialNumber
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdDeviceReset
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdStartContinuousMeasurement
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdStopMeasurement
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdGetVocAlgorithmTuningParameters
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdSetVocAlgorithmTuningParameters
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdGetVocAlgorithmState
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdSetVocAlgorithmState
.. autoclass:: sensirion_i2c_svm40.commands.generated.Svm40I2cCmdStoreNvData
.. autoclass:: sensirion_i2c_svm40.commands.wrapped.Svm40I2cCmdGetVersion
.. autoclass:: sensirion_i2c_svm40.commands.wrapped.Svm40I2cCmdReadMeasuredValues
.. autoclass:: sensirion_i2c_svm40.commands.wrapped.Svm40I2cCmdReadMeasuredValuesRaw
.. autoclass:: sensirion_i2c_svm40.commands.wrapped.Svm40I2cCmdGetTemperatureOffsetForRhtMeasurements
.. autoclass:: sensirion_i2c_svm40.commands.wrapped.Svm40I2cCmdSetTemperatureOffsetForRhtMeasurements
