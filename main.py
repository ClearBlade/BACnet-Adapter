from BACnetAdapter import BACnetAdapter

from bacpypes.core import run, enable_sleeping
from bacpypes.service.device import LocalDeviceObject

import sys, argparse

ADAPTER_VERSION = "1.0"

# When using bacpypes, we are required to register a local device to be able to communicate with other BACnet devices.
# A name/description of the local BACnet device being registered
LOCAL_BACNET_DEVICE_OBJECT_NAME = "ClearBlade BACnet Adapter v" + ADAPTER_VERSION
# A unique identifier for this device on the BACnet network. (Note, you may need to change this depending on your BACnet
# device number scheme to avoid conflicts)
LOCAL_BACNET_DEVICE_OBJECT_IDENTIFIER = 599
# The max size of an Application Layer Protocol Data Units accepted by our local BACnet device. This is in bytes,
# and the max value for BACnet/IP is 1476 (which is our default)
LOCAL_BACNET_DEVICE_MAX_APDU_LENGTH_ACCEPTED = 1476
# Specifies if our local device supports send or receiving segmented, or multipart APDU messages. segmentedBoth represents,
# being able to both send and receive these type of messages
LOCAL_BACNET_DEVICE_SEGMENTATION_SUPPORTED = "segmentedBoth"
# The vendor id for our local device. This allows for communicated of vendor specific or propritary object types. You may
# need to change this based on what type of devices your BACnet network (we are using 5 (Johnson Controls) by default.
# You can find a list of currently registered vendor IDs here: http://www.bacnet.org/VendorID/BACnet%20Vendor%20IDs.htm
LOCAL_BACNET_DEVICE_VENDOR_IDENTIFIER = 5

credentials = {}

print "BACnet-Adapter v" + ADAPTER_VERSION


def _parse_args(argv):
    parser = argparse.ArgumentParser(description='BACnetAdapter')
    parser.add_argument('--systemKey', required=True, help='The System Key of the ClearBlade platform the BACnet adapter will connect to. ex. b6b99d8e0bc6e486b2a9abe294cb01')
    parser.add_argument('--systemSecret', required=True, help='The System Secret of the ClearBlade platform the BACnet adapter will connect to. ex. B6B99D8E0B98EEBDD2D099A9F863')
    parser.add_argument('--deviceName', required=True, help='The name of the device, defined within the devices table of the ClearBlade platform, representing the BACnet Adapter. ex. BACNetAdapter')
    parser.add_argument('--activeKey', required=True, help='The Active Key, defined within the devices table of the ClearBlade platform, corresponding to the BACnet Adapter. ex. my_super_secret_key')
    parser.add_argument('--ipAddress', required=True, help='The ip address of the device this adapter is running on (must be an IP address, and not localhost or domain) ex. 192.168.0.19')
    parser.add_argument('--whoisInterval', dest="whoisInterval", default=120, type=int, help='The amount of time to wait between each successive scan for BACnet devices. The default is 120 (2 minutes)')
    parser.add_argument('--platformUrl', dest="platformURL", default="https://platform.clearblade.com", help='The url of the ClearBlade platform the BACnet adapter will connect to. The default is https://platform.clearblade.com. ex. https://<my custom domain>.clearblade.com')

    return vars(parser.parse_args(args=argv[1:]))

args = _parse_args(sys.argv)

this_device = LocalDeviceObject(
    objectName=LOCAL_BACNET_DEVICE_OBJECT_NAME,
    objectIdentifier=LOCAL_BACNET_DEVICE_OBJECT_IDENTIFIER,
    maxApduLengthAccepted=LOCAL_BACNET_DEVICE_MAX_APDU_LENGTH_ACCEPTED,
    segmentationSupported=LOCAL_BACNET_DEVICE_SEGMENTATION_SUPPORTED,
    vendorIdentifier=LOCAL_BACNET_DEVICE_VENDOR_IDENTIFIER
)

adapter = BACnetAdapter(this_device, args['ipAddress'] + "/24", args)
adapter.start()

services_supported = adapter.get_services_supported()

this_device.protocolServicesSupported = services_supported.value

enable_sleeping()

run()
