from types import BuiltinFunctionType

from pytest import raises

from src.py_data_digger import SeekError, seek
from tests.py_data_digger.conftest import (
    SomeObject,
    array_example,
    dict_example,
    tuple_example,
)


class TestSeekSuccessWithDictInput:
    """Test the method's happy path with dict as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_dict = dict_example()

        assert test_dict["string_item"] == "This is a string"
        assert seek(test_dict, "string_item") == "This is a string"

        assert test_dict["nested_dict"]["sub_item_string"] == "Another string"
        assert seek(test_dict, "nested_dict", "sub_item_string") == "Another string"

        assert test_dict["nested_dict"]["sub_item_string"][0] == "A"
        assert seek(test_dict, "nested_dict", "sub_item_string", 0) == "A"

        assert test_dict["nested_dict"]["sub_item_string"][-1] == "g"
        assert seek(test_dict, "nested_dict", "sub_item_string", -1) == "g"

    @staticmethod
    def test_nested_arrays() -> None:
        test_dict = dict_example()

        assert test_dict["nested_dict"]["sub_item_array"][0] == 1
        assert seek(test_dict, "nested_dict", "sub_item_array", 0) == 1

        assert test_dict["nested_dict"]["sub_item_array"][-1] == 3
        assert seek(test_dict, "nested_dict", "sub_item_array", -1) == 3

    @staticmethod
    def test_nested_tuples() -> None:
        test_dict = dict_example()

        assert test_dict["nested_dict"]["sub_item_tuple"][0] == "x"
        assert seek(test_dict, "nested_dict", "sub_item_tuple", 0) == "x"

        assert test_dict["nested_dict"]["sub_item_tuple"][-1] == "z"
        assert seek(test_dict, "nested_dict", "sub_item_tuple", -1) == "z"

    @staticmethod
    def test_nested_objects_with_seek_objects_as_true() -> None:

        test_dict = dict_example()

        assert type(test_dict["object_item"].nested_dict) is dict
        assert (
            type(seek(test_dict, "object_item", "nested_dict", seek_objects=True))
            is dict
        )

        assert (
            seek(
                test_dict,
                "nested_dict",
                "sub_item_object",
                "nested_dict",
                "nested_array",
                0,
                seek_objects=True,
            )
            == 9
        )

    @staticmethod
    def test_access_dict_attribute_when_seek_attributes_is_on() -> None:
        test_dict = dict_example()

        assert type(test_dict.items) is BuiltinFunctionType

        with raises(SeekError):
            seek(test_dict, "items")

        assert type(seek(test_dict, "items", seek_objects=True)) is BuiltinFunctionType

    @staticmethod
    def test_access_dict_key_with_same_name_of_a_dict_attribute() -> None:
        test_dict = dict_example()

        assert type(test_dict.keys) is BuiltinFunctionType

        assert test_dict["keys"] == ["The key 1", "The key 2"]
        assert seek(test_dict, "keys") == ["The key 1", "The key 2"]

    @staticmethod
    def test_access_dict_key_with_same_name_of_a_dict_attribute_when_seek_attributes_is_on() -> (
        None
    ):
        test_dict = dict_example()
        another_test_dict = {}

        assert type(test_dict.keys) is BuiltinFunctionType
        assert type(another_test_dict.keys) is BuiltinFunctionType

        assert test_dict["keys"] == ["The key 1", "The key 2"]

        assert seek(test_dict, "keys", seek_objects=True) == ["The key 1", "The key 2"]


class TestSeekSuccessWithTupleInput:
    """Test the method's happy path with tuple as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_tuple = tuple_example()

        assert test_tuple[0] == "This is a string inside tuple"
        assert seek(test_tuple, 0) == "This is a string inside tuple"

        assert test_tuple[0][0] == "T"
        assert seek(test_tuple, 0, 0) == "T"

        assert test_tuple[0][-1] == "e"
        assert seek(test_tuple, 0, -1) == "e"

    @staticmethod
    def test_nested_arrays() -> None:
        test_tuple = tuple_example()

        assert test_tuple[1] == ["a", "b", "c"]
        assert seek(test_tuple, 1) == ["a", "b", "c"]

        assert test_tuple[1][0] == "a"
        assert seek(test_tuple, 1, 0) == "a"

        assert test_tuple[1][-1] == "c"
        assert seek(test_tuple, 1, -1) == "c"

    @staticmethod
    def test_nested_tuples() -> None:
        test_tuple = tuple_example()

        assert test_tuple[2] == ("x", "y", "z")
        assert seek(test_tuple, 2) == ("x", "y", "z")

        assert test_tuple[2][0] == "x"
        assert seek(test_tuple, 2, 0) == "x"

        assert test_tuple[2][-1] == "z"
        assert seek(test_tuple, 2, -1) == "z"

    @staticmethod
    def test_nested_dicts() -> None:
        test_tuple = tuple_example()

        assert test_tuple[-1] == {"foo": 0, "bar": 1}
        assert seek(test_tuple, -1) == {"foo": 0, "bar": 1}

        assert test_tuple[-1]["foo"] == 0
        assert seek(test_tuple, -1, "foo") == 0

        assert test_tuple[-1]["bar"] == 1
        assert seek(test_tuple, -1, "bar") == 1

    @staticmethod
    def test_nested_objects_with_seek_objects_as_true() -> None:
        test_tuple = tuple_example()

        assert type(test_tuple[3]) is SomeObject
        assert type(seek(test_tuple, 3, seek_objects=True)) is SomeObject

        assert test_tuple[3].nested_dict == {"nested_array": [9, 8, 7]}
        assert seek(test_tuple, 3, "nested_dict", seek_objects=True) == {
            "nested_array": [9, 8, 7]
        }

        assert test_tuple[3].nested_dict["nested_array"] == [9, 8, 7]
        assert seek(
            test_tuple, 3, "nested_dict", "nested_array", seek_objects=True
        ) == [9, 8, 7]

        assert test_tuple[3].nested_dict["nested_array"][0] == 9
        result = seek(
            test_tuple, 3, "nested_dict", "nested_array", 0, seek_objects=True
        )
        assert result == 9

        assert test_tuple[3].nested_dict["nested_array"][-1] == 7
        result = seek(
            test_tuple, 3, "nested_dict", "nested_array", -1, seek_objects=True
        )
        assert result == 7


class TestSeekSuccessWithArrayInput:
    """Test the method's happy path with array as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_array = array_example()

        assert test_array[0] == "This is a string inside array"
        assert seek(test_array, 0) == "This is a string inside array"

        assert test_array[0][0] == "T"
        assert seek(test_array, 0, 0) == "T"

        assert test_array[0][-1] == "y"
        assert seek(test_array, 0, -1) == "y"

    @staticmethod
    def test_nested_arrays() -> None:
        test_array = array_example()

        assert test_array[1] == ["a", "b", "c"]
        assert seek(test_array, 1) == ["a", "b", "c"]

        assert test_array[1][0] == "a"
        assert seek(test_array, 1, 0) == "a"

        assert test_array[1][-1] == "c"
        assert seek(test_array, 1, -1) == "c"

    @staticmethod
    def test_nested_tuples() -> None:
        test_array = array_example()

        assert test_array[2] == ("x", "y", "z")
        assert seek(test_array, 2) == ("x", "y", "z")

        assert test_array[2][0] == "x"
        assert seek(test_array, 2, 0) == "x"

        assert test_array[2][-1] == "z"
        assert seek(test_array, 2, -1) == "z"

    @staticmethod
    def test_nested_dicts() -> None:
        test_array = array_example()

        assert test_array[-1] == {"foo": 0, "bar": 1}
        assert seek(test_array, -1) == {"foo": 0, "bar": 1}

        assert test_array[-1]["foo"] == 0
        assert seek(test_array, -1, "foo") == 0

        assert test_array[-1]["bar"] == 1
        assert seek(test_array, -1, "bar") == 1

    @staticmethod
    def test_nested_objects_with_seek_objects_as_true() -> None:
        test_array = array_example()

        assert type(test_array[3]) is SomeObject
        assert type(seek(test_array, 3, seek_objects=True)) is SomeObject

        assert test_array[3].nested_dict == {"nested_array": [9, 8, 7]}
        assert seek(test_array, 3, "nested_dict", seek_objects=True) == {
            "nested_array": [9, 8, 7]
        }

        assert test_array[3].nested_dict["nested_array"] == [9, 8, 7]
        assert seek(
            test_array, 3, "nested_dict", "nested_array", seek_objects=True
        ) == [9, 8, 7]

        assert test_array[3].nested_dict["nested_array"][0] == 9
        result = seek(
            test_array, 3, "nested_dict", "nested_array", 0, seek_objects=True
        )
        assert result == 9

        assert test_array[3].nested_dict["nested_array"][-1] == 7
        result = seek(
            test_array, 3, "nested_dict", "nested_array", -1, seek_objects=True
        )
        assert result == 7


class TestSeekSuccessWithObjectInput:
    """Test the method's happy path with object as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_obj = SomeObject()

        assert test_obj.nested_string == "This is a string inside object"
        assert (
            seek(test_obj, "nested_string", seek_objects=True)
            == "This is a string inside object"
        )

        assert test_obj.nested_string[0] == "T"
        assert seek(test_obj, "nested_string", 0, seek_objects=True) == "T"

        assert test_obj.nested_string[-1] == "t"
        assert seek(test_obj, "nested_string", -1, seek_objects=True) == "t"

    @staticmethod
    def test_nested_dicts() -> None:
        test_obj = SomeObject()

        assert test_obj.nested_dict == {"nested_array": [9, 8, 7]}
        assert seek(test_obj, "nested_dict", seek_objects=True) == {
            "nested_array": [9, 8, 7]
        }

        assert test_obj.nested_dict == {"nested_array": [9, 8, 7]}
        assert seek(test_obj, "nested_dict", "nested_array", seek_objects=True) == [
            9,
            8,
            7,
        ]


class TestSeekSuccessWithStringInput:
    """Test the method's happy path with string as initial input."""

    @staticmethod
    def test_strings() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        assert test_str == "Lorem ipsum dolor sit amet"
        assert seek(test_str) == "Lorem ipsum dolor sit amet"

        assert test_str[0] == "L"
        assert seek(test_str, 0) == "L"

        assert test_str[-1] == "t"
        assert seek(test_str, -1) == "t"
