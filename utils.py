from bacpypes.object import get_datatype
from bacpypes.constructeddata import Array
from bacpypes.primitivedata import Unsigned


def decode_multiple_properties(read_access_results_list):
    decoded_properties = {}
    for result in read_access_results_list:
        # here is the object identifier
        objectIdentifier = result.objectIdentifier
        # now come the property values per object
        for element in result.listOfResults:
            # get the property and array index
            propertyIdentifier = element.propertyIdentifier
            propertyArrayIndex = element.propertyArrayIndex

            # here is the read result
            readResult = element.readResult

            # check for an error, but do nothing if one happened todo - should that be the case?
            if readResult.propertyAccessError is None:
                # here is the value
                propertyValue = readResult.propertyValue

                # find the datatype
                datatype = get_datatype(objectIdentifier[0], propertyIdentifier)
                if not datatype:
                    raise TypeError("unknown datatype")

                # special case for array parts, others are managed by cast_out
                if issubclass(datatype, Array) and (propertyArrayIndex is not None):
                    if propertyArrayIndex == 0:
                        value = propertyValue.cast_out(Unsigned)
                    else:
                        value = propertyValue.cast_out(datatype.subtype)
                else:
                    value = propertyValue.cast_out(datatype)

                decoded_properties[propertyIdentifier] = value
    return decoded_properties
