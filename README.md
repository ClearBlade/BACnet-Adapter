# BACnet Adapter
This adapter is written with python, and provides a simple interface between BACnet devices and MQTT messaging via the ClearBlade platform. It asks all BACnet devices on the network to identify themselves, and then gets all objects and properties for each device, and finally sends that data to the ClearBlade platform via MQTT. All messages are sent to the topic `bacnet/in`.

# Dependencies
- Python 3.x
- ClearBlade Python SDK v2.4.4 (instructions [here](https://github.com/ClearBlade/ClearBlade-Python-SDK/))
- Eclipse Paho Python SDK (instructions [here](https://eclipse.org/paho/clients/python/))
- BACpypes BACnet Python SDK (instructions [here](http://bacpypes.readthedocs.io/en/latest/?badge=latest))

# Build and Release

## Python Virtual Environment
./bin/python3 main.py --systemKey e096d7fe0cd2e790bbeaf98fca30 --deviceName bacnet-adapter --activeKey y1q48r3Rm8EPSS36b4m8C11873 --ipAddress 10.0.0.88 --platformUrl https://demo.clearblade.com

python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
/path/to/new/virtual/environment/bin/pip3 install some-python-library


## Development Installation
To install the package in development mode:
```bash
pip install -e .
```

## Development Dependencies
For development, you'll need additional packages:
```bash
pip install -r requirements-dev.txt
```

# Usage
Before starting the adapter you will need to add an entry to the device table of the system you want to use. When creating the device make sure it is enabled, and allow key authorization. Finally be sure to set a value for the `active_key` column after creation. You will need this, and th device name when starting the adapter.

To start the adapter you simply need to run `python main.py` with the following command line flags:

|Name|Description|
|---|---|
|`--systemKey` (required)|The ClearBlade Platform system key you would like to have MQTT messages published to|
|`--deviceName` (required)|The device name that you set for the adapter|
|`--activeKey` (required)|The active key that you set for the adapter|
|`--ipAddress` (required)|The IP address of the device you are running the adapter on|
|`--platformUrl` (optional)|The URL for the ClearBlade Platform instance you want to use. If not provided, defaults to https://platform.clearblade.com|
|`--whoisInterval` (optional)|Set the length of time (in seconds) between who is messages. Defaults to 120.

# MQTT Message Format
Here is an example MQTT message sent from the BACnet adapter to the platform.

```json
{
  "device": {
    "source": "20:0x7a0100000000",
    "id": [
      "device",
      378
    ]
  },
  "object": [
    "analogInput",
    0
  ],
  "properties": {
    "notificationClass": 0,
    "reliability": "noFaultDetected",
    "eventTimeStamps": [
      "<bacpypes.basetypes.TimeStamp object at 0x108f2b110>",
      "<bacpypes.basetypes.TimeStamp object at 0x108f2b3d0>",
      "<bacpypes.basetypes.TimeStamp object at 0x108f2ba50>"
    ],
    "covIncrement": 0.10000000149011612,
    "timeDelay": 10,
    "deadband": 1,
    "ackedTransitions": [
      1,
      1,
      1
    ],
    "notifyType": "event",
    "deviceType": "",
    "units": "degreesFahrenheit",
    "presentValue": 153,
    "objectType": "analogInput",
    "statusFlags": [
      1,
      0,
      0,
      0
    ],
    "description": "",
    "objectName": "TempSensor1",
    "highLimit": 250,
    "limitEnable": [
      1,
      1
    ],
    "lowLimit": 0,
    "objectIdentifier": [
      "analogInput",
      0
    ],
    "profileName": "123-AI",
    "updateInterval": 100,
    "outOfService": false,
    "maxPresValue": 250,
    "minPresValue": 0,
    "propertyList": [
      "presentValue",
      "objectName",
      "description",
      1008,
      "updateInterval",
      "minPresValue",
      "maxPresValue",
      "covIncrement",
      "objectType",
      "objectIdentifier",
      "deviceType",
      "statusFlags",
      "eventState",
      "reliability",
      "outOfService",
      1007,
      "units",
      "resolution",
      "timeDelay",
      "notificationClass",
      "highLimit",
      "lowLimit",
      "deadband",
      "limitEnable",
      "eventEnable",
      "ackedTransitions",
      "notifyType",
      "eventTimeStamps",
      "profileName",
      1001,
      1006,
      "propertyList"
    ],
    "eventState": "highLimit",
    "eventEnable": [
      0,
      0,
      0
    ],
    "resolution": 0.10000000149011612
  }
}
```
