import threading, json
from bacpypes.app import BIPSimpleApplication
from bacpypes.apdu import WhoIsRequest
from bacpypes.pdu import GlobalBroadcast, Address

from Device import Device
from MQTT import MQTT


class BACnetAdapter(BIPSimpleApplication):
    def __init__(self, device, hostname, args):
        print("BACnetAdapter __init__")
        BIPSimpleApplication.__init__(self, device, hostname)
        self.who_is_request = None
        self.credentials = args
        self.interval = args["whoisInterval"]
        self.low_limit = args["lowerDeviceIdLimit"]
        self.high_limit = args["upperDeviceIdLimit"]
        self.mqtt = None
        # todo - create our devices with the provided IPs in the device-config.json file
        # during device creation we should also get some info on each device, mainly the objectName on the device object

    def request(self, apdu):
        print("BACnetAdapter request")
        if isinstance(apdu, WhoIsRequest):
            self.who_is_request = apdu

        BIPSimpleApplication.request(self, apdu)

    def do_IAmRequest(self, apdu):
        print("do_IAmRequest")
        if not self.who_is_request:
            return
        else:
            print(apdu.iAmDeviceIdentifier)
            device = Device(apdu.iAmDeviceIdentifier, apdu.pduSource, self)
            device.get_object_list()

    def send_props_to_platform(self, device, obj, props):
        print("send_props_to_platform")
        obj_to_send = {
            'device': {
                'id': device.id,
                'name': device.name,
                'source': device.source
            },
            'object': obj,
            'properties': props
        }
        try:
            msg = json.dumps(obj_to_send, ensure_ascii=False, default=json_serial)
            print(msg)
            self.mqtt.PublishTopic("bacnet/in", str(msg))
        except Exception as e:
            print(e)

    def start(self):
        print("start")
        if self.mqtt is None:
            self.mqtt = MQTT(self.credentials)

        self.who_is(self.low_limit, self.high_limit, Address("10.16.163.20"))
        # todo - here we will want to loop through each device we have, and kick off getting all objects and properties for the device
        timer = threading.Timer(self.interval, self.start)
        timer.daemon = True
        timer.start()


def json_serial(obj):
    print("json_serial")
    """JSON serializer for objects not serializable by default json code"""
    #if isinstance(obj, TimeStamp):
    return str(obj)