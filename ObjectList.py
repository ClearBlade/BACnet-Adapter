from bacpypes.apdu import ReadPropertyRequest, ReadPropertyACK
from bacpypes.basetypes import PropertyIdentifier
from bacpypes.constructeddata import ArrayOf
from bacpypes.iocb import IOCB

from PropertyList import PropertyList


class ObjectList:
    def __init__(self, list_of_ids, device, bacnet_adapter):
        print(list_of_ids)
        self.object_ids = list_of_ids
        self.device = device
        self.bacnet_adapter = bacnet_adapter
        self.prop_list_for_obj = {}

    def get_properties_for_each_object(self):
        for obj in self.object_ids:
            self._get_prop_for_obj(obj)

    def _get_prop_for_obj(self, obj_id):
        request = ReadPropertyRequest(
            destination=self.device.source,
            objectIdentifier=obj_id,
            propertyIdentifier='propertyList'
        )
        iocb = IOCB(request)
        iocb.add_callback(self._got_properties_for_object, obj_id)
        self.bacnet_adapter.request_io(iocb)

    def _got_properties_for_object(self, iocb, object_id):
        if iocb.ioError:
            print("error getting property list: %s", str(iocb.ioError))
            return
        elif iocb.ioResponse:
            apdu = iocb.ioResponse
            if not isinstance(apdu, ReadPropertyACK):
                print("response was not ReadPropertyACK")
                return
            self.prop_list_for_obj[object_id] = PropertyList(apdu.propertyValue.cast_out(ArrayOf(PropertyIdentifier)), object_id, self.device,
                                         self.bacnet_adapter)
            self.prop_list_for_obj[object_id].get_values_for_properties()

