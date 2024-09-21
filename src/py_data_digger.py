from typing import Any, List, Mapping, Sequence, Union

LIST_INDICES_MUST_BE_INTEGERS_MSG = "list indices must be integers or slices, not"
OBJECT_IS_NOT_SUBSCRIPTABLE_MSG = "object is not subscriptable"


class SeekError(ValueError):
    """Raised when the seek method fails to go further."""

    def __init__(
        self,
        current_accessor_index: int,
        original_data: type,
        accessors: List[Any],
        original_error: Exception,
    ) -> None:
        error_name = type(original_error).__name__
        original_data_name = type(original_data).__name__
        path_items = [original_data_name] + [
            str(a) for a in accessors[: current_accessor_index + 1]
        ]
        self.message = (
            f"Data digger can't go any further: {error_name}\n"
            f"Path traveled: {' -> '.join(path_items)}"
        )
        super().__init__(self.message)


def seek(
    data: Union[Sequence, Mapping],
    *accessors: List[Any],
    seek_objects: bool = False,
) -> object:
    """Navigate through the data.

    If there is no key, index or attribute with a given accessor, raises SeekError.

    Parameters:
      data: The list, tuple, dict to be searched. By default it can't access object attributes
      accessors: The keys, indexes or attribute names (only if seek_objects is True) to be accessed
      seek_objects: If seek_objects is True, also tries to get an attribute of an object
      with the given name

    Raises:
      SeekError: if there is no key, index or attribute with a given accessor. The exception message
      will provide details on where it could not access.

    Examples:
    .. code-block:: python
      my_dict = {
      'item_a': ['apple', 'pea'],
      }

      seek(my_dict, 'item_a', 0)
      >>> 'apple'

      seek(my_dict, 'item_b', 0)
      >>> SeekError



    When seek_objects is True:
    .. code-block:: python

      person = Person(name='John Doe')
      my_dict = {
      'item_with_object': person
      }

      seek(my_dict, 'item_with_object', 'name', seek_objects=True)
      >>> 'John Doe'

      seek(my_dict, 'item_with_object', 'age', seek_objects=True)
      >>> SeekError
    """
    result = data
    for index, accessor in enumerate(accessors):
        try:
            result = result[accessor]
        except (KeyError, ValueError) as e:
            raise SeekError(index, data, accessors, e) from e
        except TypeError as e:
            error = SeekError(index, data, accessors, e)
            if seek_objects:
                result = _look_for_object_attribute(result, data, accessors, index)
                continue
            if LIST_INDICES_MUST_BE_INTEGERS_MSG in str(e):
                raise error from e
            if OBJECT_IS_NOT_SUBSCRIPTABLE_MSG in str(e):
                raise error from e
            raise error from e
    return result


def dig(
    data: Union[Sequence, Mapping], *accessors: List[Any], dig_objects: bool = False
) -> object:
    """Safely navigate through the nested data.

    If there is no key, index or attribute with a given accessor, returns None.

    Parameters:
      data: The list, tuple, dict to be searched. By default it can't access object attributes
      accessors: The keys, indexes or attribute names (only if dig_objects is True) to be accessed
      dig_objects: If dig_objects is True, also tries to get an attribute of an object
      with the given name.

    Examples:
    .. code-block:: python
      my_dict = {
      'item_a': ['apple', 'pea'],
      }

      dig(my_dict, 'item_a', 0)
      >>> 'apple'

      dig(my_dict, 'item_b', 0)
      >>> None



    When dig_objects is True:
    .. code-block:: python

      person = Person(name='John Doe')
      my_dict = {
      'item_with_object': person
      }

      dig(my_dict, 'item_with_object', 'name', dig_objects=True)
      >>> 'John Doe'

      dig(my_dict, 'item_with_object', 'age', dig_objects=True)
      >>> None
    """
    try:
        return seek(data, *accessors, seek_objects=dig_objects)
    except SeekError:
        return None


def _look_for_object_attribute(
    result: object, original_data: object, accessors: list[object], index: int
) -> object:
    try:
        return getattr(result, accessors[index])
    except AttributeError as e:
        raise SeekError(index, original_data, accessors, e) from e
