# dictobj

dictobj is a Python library that allows easy creation of data objects.
These data objects can then be converted from and to dictionaries,
allowing easy JSON serialisation.

## Example

```python
import dictobj

Instrument = dictobj.data_class("Instrument", [
    "name",
    "material",
])


saxophone = Instrument("saxophone", "brass")

serialised_saxophone = dictobj.obj_to_dict(saxophone)
unserialised_saxophone = dictobj.dict_to_obj(serialised_saxophone)

print unserialised_saxophone.material # Prints "brass"
```

## License

[2-Clause BSD](http://opensource.org/licenses/BSD-2-Clause)
