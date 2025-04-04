from bacpypes.apdu import ReadPropertyRequest, ReadPropertyACK, ReadPropertyMultipleACK, PropertyReference, ReadAccessSpecification, ReadPropertyMultipleRequest
from bacpypes.basetypes import PropertyIdentifier, CharacterString
from bacpypes.constructeddata import ArrayOf, Array
from bacpypes.iocb import IOCB

from PropertyList import PropertyList

from utils import decode_multiple_properties


class ObjectList:
    def __init__(self, list_of_ids, device, bacnet_adapter):
        self.object_ids = list_of_ids
        self.device = device
        self.bacnet_adapter = bacnet_adapter
        self.prop_list_for_obj = {}

    def get_properties_for_each_object(self):
        for obj in self.object_ids:
            if obj[0] != 'trendLog' and obj[0] != 'device':
                self._get_prop_for_obj(obj)

    def _get_prop_for_obj(self, obj_id):

        props_to_get = ['objectName', 'description', 'presentValue', 'units']

        prop_ref_list = []

        for prop in props_to_get:
            ref = PropertyReference(
                propertyIdentifier=prop
            )
            prop_ref_list.append(ref)

        read_access_spec = ReadAccessSpecification(
            objectIdentifier=obj_id,
            listOfPropertyReferences=prop_ref_list,
        )

        request = ReadPropertyMultipleRequest(
            listOfReadAccessSpecs=[read_access_spec],
            destination=self.device.source
        )

        iocb = IOCB(request)
        iocb.add_callback(self._got_properties_for_object, obj_id)
        self.bacnet_adapter.request_io(iocb)

    def _got_properties_for_object(self, iocb, object_id):
        print(f'info for obj {object_id}')
        if iocb.ioError:
            print(f"error getting property list: {str(iocb.ioError)}")
            return
        else:
            apdu = iocb.ioResponse
            if not isinstance(apdu, ReadPropertyMultipleACK):
                print("response was not ReadPropertyACK")
                return
            props_obj = decode_multiple_properties(apdu.listOfReadAccessResults)
            # add obj and device info to the props obj, we want to send this to the platform
            print(props_obj)

            self.bacnet_adapter.send_props_to_platform(self.device, object_id, props_obj)