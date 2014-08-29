import re
import uuid
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import json
import sys


def dumps(obj):
    return json.dumps(obj_to_dict(obj))


def loads(string, cls):
    return dict_to_obj(json.loads(string), cls)


def dict_to_obj(dict_kwargs, cls):
    dict_kwargs_without_camel_case = dict(
        (_from_camel_case(key), value)
        for key, value in _iteritems(dict_kwargs)
    )
    
    fields = dict(
        (field.name, field)
        for field in _fields(cls)
    )
    
    def _read_value(key, value):
        field = fields[key]
        if field.type is None:
            return value
        else:
            return dict_to_obj(value, field.type)
    
    raw_kwargs = (
        (key, value)
        for key, value in _iteritems(dict_kwargs_without_camel_case)
        if key in fields
    )
    
    cls_kwargs = dict(
        (key, _read_value(key, value))
        for key, value in raw_kwargs
    )
    
    return cls(**cls_kwargs)


def obj_to_dict(obj):
    def _serialise(value):
        if hasattr(value, _fields_attr):
            return obj_to_dict(value)
        else:
            return value
    
    return OrderedDict(
        (_to_camel_case(field.name), _serialise(getattr(obj, field.name)))
        for field in _fields(obj)
    )
    

def obj_to_flat_list(obj):
    result = []
    
    def _serialise_obj(value):
        if hasattr(value, _fields_attr):
            for field in _fields(value):
                _serialise_obj(getattr(value, field.name))
        else:
            result.append(value)
            
    _serialise_obj(obj)
    return result


def flat_list_to_obj(values, cls):
    values = list(reversed(values))
    
    def _unserialise_type(target_type):
        if target_type is None:
            return values.pop()
        else:
            args = [
                _unserialise_type(field.type)
                for field in _fields(target_type)
            ]
            return target_type(*args)
    
    
    return _unserialise_type(cls)


def _fields(obj):
    return getattr(obj, _fields_attr)


def _from_camel_case(string):
    # http://stackoverflow.com/questions/1175208
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _to_camel_case(value):
    # http://stackoverflow.com/questions/4303492
    def camelcase(): 
        yield lambda s: s.lower()
        while True:
            yield lambda s: s.capitalize()

    c = camelcase()
    return "".join(next(c)(x) if x else '_' for x in value.split("_"))


_fields_attr = str(uuid.uuid4())


def data_class(name, fields):
    def _to_field(field):
        if isinstance(field, basestring):
            return Field(field)
        else:
            return field
    
    fields = [_to_field(field) for field in fields]
    
    def __init__(self, *args, **kwargs):
        if len(args) > len(fields):
            raise TypeError("__init__ takes {0} positional argument{1} but {2} were given".format(
                len(fields) + 1, "s" if len(fields) == 1 else "", len(args) + 1))
        
        for field_index, field in enumerate(fields):
            if field_index < len(args):
                setattr(self, field.name, args[field_index])
            elif field.name in kwargs:
                setattr(self, field.name, kwargs.pop(field.name))
            else:
                raise TypeError("Missing argument: {0}".format(field.name))
                
        for field_name in kwargs:
            raise TypeError("{0}.__init__ does not take keyword argument '{1}'".format(name, field_name))
    
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
    return new_type


class Field(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


field = Field


if sys.version_info[0] == 3:
    basestring = str
    
    def _iteritems(x):
        return x.items()
else:
    def _iteritems(x):
        return x.iteritems()
