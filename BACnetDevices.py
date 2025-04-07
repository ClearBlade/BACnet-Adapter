from clearblade import Devices
from clearblade.ClearBladeCore import System

from bacpypes.apdu import WhoIsRequest, IAmRequest, ReadPropertyRequest
from bacpypes.basetypes import CharacterString
from bacpypes.constructeddata import ArrayOf
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address
from bacpypes.primitivedata import ObjectIdentifier

class BACnetDevices():

    BACNET_DEVICES_COLLECTION_NAME = "bacnet_devices"
    def __init__(self, cb_client, bacnet_adapter, system: System):
        self.cb_client = cb_client
        self.bacnet_adapter = bacnet_adapter
        self.cb_collection = system.Collection(self.cb_client, collectionName=self.BACNET_DEVICES_COLLECTION_NAME)
        devices = self.cb_collection.getItems()

        self.devices = {}
        for device in devices:
            # first check if we have any new devices, if so initialize them
            if device["device_name"] == None or device["device_name"] == "".encode('utf-8'):
                self._initialize_new_deivce(device["item_id"], device["ip_address"].encode('utf-8'))
            # for easier look up later, let's translate device array into an object with device ip as the key
        self.devices[device["ip_address"]] = device
        print(self.devices)

    def _initialize_new_deivce(self, device_item_id, device_ip):
        self.bacnet_adapter.who_is(None, None, Address(device_ip))

    def got_new_device_who_is_response(self, apdu):
        # first check that this new device is one we actually care about (some times we get whois responses from other devices, even though the request was targeted to a specific ip rather than a global address)
        if not str(apdu.pduSource) in self.devices:
            print("got who is response from a device we don't care about")
            return
    # now we need to get the device name using the identifier we just got
        request = ReadPropertyRequest(
            destination=apdu.pduSource,
            objectIdentifier=apdu.iAmDeviceIdentifier,
            propertyIdentifier='objectName'
        )
        iocb = IOCB(request)
        iocb.add_callback(self._got_device_object_name, apdu.iAmDeviceIdentifier)
        self.bacnet_adapter.request_io(iocb)

    def _got_device_object_name(self, iocb, device_id):
        if iocb.ioError:
            print("error (%s) when attempting to get objectName of device (%s %s)" % (str(iocb.ioError), iocb.pduSource, iocb.pduSource))
        else:
            apdu = iocb.ioResponse
            device_name = apdu.propertyValue.cast_out(CharacterString)
        #we now have everything we need to update the device data in the collection
        query = {
        "FILTERS": [
            [{
            "EQ": [{
                "ip_address": str(apdu.pduSource)
            }]
            }]
        ]
        }
        changes = {
        "device_name": device_name,
        "bacnet_device_identifier":  device_id[1],	    
        "default_sensor_data_fetch": "cov"
        }
        # results = self.cb_collection.update(changes, query)   
        results = self.cb_collection.updateItems(changes, query)
        if results["count".encode('utf-8')] != 1:
            print("failed to update the deivce")
        else:
        #rather then fetch from the server again, just update these here
            self.devices[str(apdu.pduSource)]["device_name"] = device_name.decode("utf-8")
            self.devices[str(apdu.pduSource)]["default_sensor_data_fetch"] = "cov".decode("utf-8")
            self.devices[str(apdu.pduSource)]["bacnet_device_identifier"] = device_id[1]
            self._get_new_sensors_for_new_device(apdu.pduSource, device_id)

    def _get_new_sensors_for_new_device(self, source, device_id):
        request = ReadPropertyRequest(
            destination=source,
            objectIdentifier=device_id,
            propertyIdentifier="objectList"
        )
        iocb = IOCB(request)
        iocb.add_callback(self._got_sensors_for_device)
        self.bacnet_adapter.request_io(iocb)
        
    def _got_sensors_for_device(self, iocb):
        if iocb.ioError:
            print("error (%s) when attempting to get objectList of device (%s)" % (str(iocb.ioError), iocb.pduSource))
        else:
            apdu = iocb.ioResponse
            new_sensors = apdu.propertyValue.cast_out(ArrayOf(ObjectIdentifier))
            self.bacnet_adapter.bacnet_sensors.add_new_sensors_from_device(new_sensors, self.devices[str(apdu.pduSource)])