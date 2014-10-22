import uuid
import sys


def _fields(obj):
    return getattr(obj, _fields_attr)


_fields_attr = str(uuid.uuid4())


def data_class(name, fields):
    def _to_field(field):
        if isinstance(field, basestring):
            return Field(field)
        else:
            return field
    
    fields = [_to_field(field) for field in fields]
    
    def __init__(self, *args, **kwargs):
        for field_index, field in enumerate(fields):
            if field_index < len(args):
                setattr(self, field.name, args[field_index])
            elif field.name in kwargs:
                setattr(self, field.name, kwargs.pop(field.name))
            else:
                raise TypeError("Missing argument: {0}".format(field.name))
                
        for field_name in kwargs:
            raise TypeError("{0}.__init__ does not take keyword argument {1}".format(name, field_name))
    
    def __eq__(self, other):
        if isinstance(other, new_type):
            return all(
                getattr(self, field.name) == getattr(other, field.name)
                for field in fields
            )
        else:
            return NotImplemented
        
    def __ne__(self, other):
        return not (self == other)
        
    def __repr__(self):
        values = (getattr(self, field.name) for field in fields)
        return "{0}({1})".format(name, ", ".join(map(str, values)))
        
    def __str__(self):
        return repr(self)
    
    properties = {
        "__init__": __init__,
        "__eq__": __eq__,
        "__ne__": __ne__,
        "__repr__": __repr__,
        "__str__": __str__,
        _fields_attr: fields,
    }
    
    new_type = type(name, (object,), properties)
    try:
        new_type.__module__ = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    
    return new_type


class Field(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


field = Field


if sys.version_info[0] >= 3:
    basestring = str
