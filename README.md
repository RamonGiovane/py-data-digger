![example workflow](https://github.com/RamonGiovane/py-data-digger/actions/workflows/python-app.yml/badge.svg?branch=main)

# py-data-digger
Safely navigate through unsafe data: dicts, tuples, lists, strings and objects

Inspired on Ruby's [dig](https://www.rubydoc.info/stdlib/core/Hash:dig).

```
pip install py-data-digger
```

## Why?
### TLDR: 
Sometimes you don't want to deal with Python exceptions when accessing lists and dicts. If the data you need isn't there, you just want to **move on**...

**No ifs, no try-excepts!**

```python
from py_data_digger import dig

components: list | None = dig(nasty_dict, "machines", 0, "engine", "components")
```

### Detailed explanation
In some occasions (like when web scrapping) you need to grab some data from a deeply nested structure like this:
```python
nasty_dict = {
    "machines": [
        {
            "machine_id": "1234567890",
            "engine": {
                "id": "321abcde",
                "name": "Motor XPTO",
                "components": [
                    {"id": "0942323", "name": "Cog"},
                    {"id": "1642723", "name": "Piston"},
                    {"id": "8412321", "name": "Bar", "extras": ["Foo"]},
                ],
            },
        }
    ]
}
```

Suppose we want to take the list of components of the engine of a machine (the only present).

### 🚨 The unsafe strategy:
```python
components: list = nasty_dict["machines"][0]["engine"]["components"]
```

This is unsafe because it is highly prone to raise `IndexError`, `KeyError`, `TypeError` if you use the wrong key/index or if the data just isn't there.

### 😴 The safe (but boring) strategy:
```python
machines: list | None = nasty_dict.get("machines", None)
machine: dict | None = next(iter(machines), None) if machines else None
engine: dict | None = machine.get("engine", None) if machine is not None else None
components: list | None: engine.get("components", None) if engine is not None else None
  
```

This is not only tedious but labourious!
At least, it's safe. We would not raise errors to break our code.


## Introducing `dig`
With this tool we may quickly and securely navigate through all sorts of nested data.

Let's consider the `nasty_dict` from the past section and that we also want to access the list of components.
```python
from py_data_digger import dig

components: list | None = dig(nasty_dict, "machines", 0, "engine", "components")
```

That's it! All the access problems are solved. If the data you want isn't there, it returns `None` and you can just **move on**!
```python
components: list | None = dig(nasty_dict, "machines", 0, "engine_2", "components")
if components is None:
  return None
```

## Introducing `seek`
Not satisfied with `None` returns?

The `seek` function works just like `dig`, but it will raise an error if the path informed could not be found.

```python
from py_data_digger import seek


components: list = seek(nasty_dict, "machines", 0, "engine_2", "components")
>>> SeekError: Data digger can't go any further: KeyError
Path traveled: dict -> machines -> 0 -> engine_2
```

The cool thing is, you would need to handle just one exception (`SeekError`). It also shows where it failed to seek 😎

## Seeking/digging objects
And there is more!
If you also want to look inside object attributes, you may do it by passing a special flag.
This way it will be compatible with any nested objects like **Pydantic** models and **dataclasses**!
```python
  person = Person(name='John Doe')
  my_dict = {
  'item_with_object': person
  }

  dig(my_dict, 'item_with_object', 'name', dig_objects=True)
  >>> 'John Doe'

  dig(my_dict, 'item_with_object', 'age', dig_objects=True)
  >>> None

  seek(my_dict, 'item_with_object', 'name', seek_objects=True)
  >>> 'John Doe'

  seek(my_dict, 'item_with_object', 'age', seek_objects=True)
  >>> SeekError
```

⚠️ The special flag is required because attribute names may conflict with other mapped keys. Use with caution.
