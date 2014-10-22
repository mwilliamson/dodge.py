import sys
import json
import re
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from .data import _fields_attr, _fields


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


if sys.version_info[0] >= 3:
    def _iteritems(x):
        return x.items()
else:
    def _iteritems(x):
        return x.iteritems()
