import threading, json
from bacpypes.app import BIPSimpleApplication
from bacpypes.apdu import WhoIsRequest
from bacpypes.pdu import GlobalBroadcast

from Device import Device
from MQTT import MQTT


class BACnetAdapter(BIPSimpleApplication):
    def __init__(self, device, hostname, args):
        BIPSimpleApplication.__init__(self, device, hostname)
        self.who_is_request = None
        self.credentials = args
        self.interval = args["whoisInterval"]
        self.mqtt = None

    def request(self, apdu):
        if isinstance(apdu, WhoIsRequest):
            self.who_is_request = apdu
        BIPSimpleApplication.request(self, apdu)

    def do_IAmRequest(self, apdu):
        if not self.who_is_request:
            return
        else:
            print apdu.iAmDeviceIdentifier
            device = Device(apdu.iAmDeviceIdentifier, apdu.pduSource, self)
            device.get_object_list()

    def send_props_to_platform(self, device, obj, props):
        obj_to_send = {
            'device': device,
            'object': obj,
            'properties': props
        }
        try:
            msg = json.dumps(obj_to_send, ensure_ascii=False, default=json_serial)
            self.mqtt.PublishTopic("bacnet/in", str(msg))
        except Exception as e:
            print e

    def start(self):
        if self.mqtt is None:
            self.mqtt = MQTT(self.credentials)
        self.who_is(None, None, GlobalBroadcast())
        timer = threading.Timer(self.interval, self.start)
        timer.daemon = True
        timer.start()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    #if isinstance(obj, TimeStamp):
    return str(obj)
