from bacpypes.object import get_datatype
from bacpypes.iocb import IOCB
from bacpypes.apdu import ReadPropertyRequest, ReadPropertyACK


class PropertyList:
    def __init__(self, list_of_props, object, device, bacnet_adapter):
        print("PropertyList __init__")
        self.list_of_props = []
        for prop in list_of_props:
            if isinstance(prop, object):
                datatype = get_datatype(object[0], prop)
                if not datatype:
                    print("no datatype found for prop: %s", prop)
                    pass
                else:
                    self.list_of_props.append(prop)
        self.device = device
        self.object = object
        self.bacnet_adapter = bacnet_adapter
        self.prop_values = {}

    def get_values_for_properties(self):
        print("PropertyList get_values_for_properties")
        for prop in self.list_of_props:
            self._get_value_for_prop(prop)

    def _get_value_for_prop(self, prop):
        print("PropertyList _get_value_for_prop")
        request = ReadPropertyRequest(
            destination=self.device.source,
            objectIdentifier=self.object,
            propertyIdentifier=prop
        )
        iocb = IOCB(request)
        iocb.add_callback(self._got_prop, prop)
        self.bacnet_adapter.request_io(iocb)

    def _got_prop(self, iocb, prop):
        print("PropertyList _got_prop")
        if iocb.ioError:
            self.prop_values[prop] = str(iocb.ioError)
        elif iocb.ioResponse:
            apdu = iocb.ioResponse
            if not isinstance(apdu, ReadPropertyACK):
                print("response was not ReadPropertyACK")
                return
            datatype = get_datatype(self.object[0], prop)
            value = apdu.propertyValue.cast_out(datatype)
            self.prop_values[prop] = value
            if len(self.prop_values) == len(self.list_of_props):
                self.send_props_to_cb_platform()

    def send_props_to_cb_platform(self):
        print("PropertyList send_props_to_cb_platform")
        self.bacnet_adapter.send_props_to_platform(self.device, self.object, self.prop_values)