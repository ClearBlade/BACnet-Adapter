from BACnetAdapter import BACnetAdapter

from bacpypes.core import run, enable_sleeping
from bacpypes.service.device import LocalDeviceObject

import sys, argparse

credentials = {}


def _parse_args(argv):
    parser = argparse.ArgumentParser(description='BACnetAdapter')
    parser.add_argument('--systemKey', required=True, help='The System Key of the ClearBlade platform the BACnet adapter will connect to.')
    parser.add_argument('--systemSecret', required=True, help='The System Secret of the ClearBlade platform the BACnet adapter will connect to.')
    parser.add_argument('--deviceName', required=True, help='The name of the device, defined within the devices table of the ClearBlade platform, representing the BACnet Adapter.')
    parser.add_argument('--activeKey', required=True, help='The Active Key, defined within the devices table of the ClearBlade platform, corresponding to the BACnet Adapter.')
    parser.add_argument('--ipAddress', required=True, help='The ip address of the device this adapter is running on')
    parser.add_argument('--whoisInterval', dest="whoisInterval", default=120, type=int, help='The amount of time to wait between each successive scan for BACnet devices. The default is 120 (2 minutes)')
    parser.add_argument('--platformUrl', dest="platformURL", default="https://platform.clearblade.com", help='The url of the ClearBlade platform the BACnet adapter will connect to. The default is https://platform.clearblade.com')

    return vars(parser.parse_args(args=argv[1:]))

args = _parse_args(sys.argv)

print args

this_device = LocalDeviceObject(
    objectName="clearblade",
    objectIdentifier=599,
    maxApduLengthAccepted=1024,
    segmentationSupported="segmentedBoth",
    vendorIdentifier=15
)

adapter = BACnetAdapter(this_device, args['ipAddress'] + "/24", args)
adapter.start()

services_supported = adapter.get_services_supported()

this_device.protocolServicesSupported = services_supported.value

enable_sleeping()

run()
