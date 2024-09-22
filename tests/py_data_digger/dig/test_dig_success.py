from types import BuiltinFunctionType

from pydantic import BaseModel

from src.py_data_digger import dig
from tests.py_data_digger.conftest import (
    PydanticModel,
    SomeObject,
    array_example,
    dict_example,
    tuple_example,
)


class TestDigSuccessWithDictInput:
    """Test the method's happy path with dict as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_dict = dict_example()

        assert test_dict["string_item"] == "This is a string"
        assert dig(test_dict, "string_item") == "This is a string"

        assert test_dict["nested_dict"]["sub_item_string"] == "Another string"
        assert dig(test_dict, "nested_dict", "sub_item_string") == "Another string"

        assert test_dict["nested_dict"]["sub_item_string"][0] == "A"
        assert dig(test_dict, "nested_dict", "sub_item_string", 0) == "A"

        assert test_dict["nested_dict"]["sub_item_string"][-1] == "g"
        assert dig(test_dict, "nested_dict", "sub_item_string", -1) == "g"

    @staticmethod
    def test_nested_arrays() -> None:
        test_dict = dict_example()

        assert test_dict["nested_dict"]["sub_item_array"][0] == 1
        assert dig(test_dict, "nested_dict", "sub_item_array", 0) == 1

        assert test_dict["nested_dict"]["sub_item_array"][-1] == 3
        assert dig(test_dict, "nested_dict", "sub_item_array", -1) == 3

    @staticmethod
    def test_nested_tuples() -> None:
        test_dict = dict_example()

        assert test_dict["nested_dict"]["sub_item_tuple"][0] == "x"
        assert dig(test_dict, "nested_dict", "sub_item_tuple", 0) == "x"

        assert test_dict["nested_dict"]["sub_item_tuple"][-1] == "z"
        assert dig(test_dict, "nested_dict", "sub_item_tuple", -1) == "z"

    @staticmethod
    def test_nested_objects_with_seek_objects_as_true() -> None:

        test_dict = dict_example()

        assert type(test_dict["object_item"].nested_dict) is dict
        assert (
            type(dig(test_dict, "object_item", "nested_dict", dig_objects=True)) is dict
        )

        assert (
            dig(
                test_dict,
                "nested_dict",
                "sub_item_object",
                "nested_dict",
                "nested_array",
                0,
                dig_objects=True,
            )
            == 9
        )

    @staticmethod
    def test_access_dict_attribute_when_seek_attributes_is_on() -> None:
        test_dict = dict_example()

        assert type(test_dict.items) is BuiltinFunctionType

        assert dig(test_dict, "items") is None

        assert type(dig(test_dict, "items", dig_objects=True)) is BuiltinFunctionType

    @staticmethod
    def test_access_dict_key_with_same_name_of_a_dict_attribute() -> None:
        test_dict = dict_example()

        assert type(test_dict.keys) is BuiltinFunctionType

        assert test_dict["keys"] == ["The key 1", "The key 2"]
        assert dig(test_dict, "keys") == ["The key 1", "The key 2"]

    @staticmethod
    def test_access_dict_key_with_same_name_of_a_dict_attribute_when_seek_attributes_is_on() -> (
        None
    ):
        test_dict = dict_example()
        another_test_dict = {}

        assert type(test_dict.keys) is BuiltinFunctionType
        assert type(another_test_dict.keys) is BuiltinFunctionType

        assert test_dict["keys"] == ["The key 1", "The key 2"]

        assert dig(test_dict, "keys", dig_objects=True) == ["The key 1", "The key 2"]


class TestDigSuccessWithTupleInput:
    """Test the method's happy path with tuple as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_tuple = tuple_example()

        assert test_tuple[0] == "This is a string inside tuple"
        assert dig(test_tuple, 0) == "This is a string inside tuple"

        assert test_tuple[0][0] == "T"
        assert dig(test_tuple, 0, 0) == "T"

        assert test_tuple[0][-1] == "e"
        assert dig(test_tuple, 0, -1) == "e"

    @staticmethod
    def test_nested_arrays() -> None:
        test_tuple = tuple_example()

        assert test_tuple[1] == ["a", "b", "c"]
        assert dig(test_tuple, 1) == ["a", "b", "c"]

        assert test_tuple[1][0] == "a"
        assert dig(test_tuple, 1, 0) == "a"

        assert test_tuple[1][-1] == "c"
        assert dig(test_tuple, 1, -1) == "c"

    @staticmethod
    def test_nested_tuples() -> None:
        test_tuple = tuple_example()

        assert test_tuple[2] == ("x", "y", "z")
        assert dig(test_tuple, 2) == ("x", "y", "z")

        assert test_tuple[2][0] == "x"
        assert dig(test_tuple, 2, 0) == "x"

        assert test_tuple[2][-1] == "z"
        assert dig(test_tuple, 2, -1) == "z"

    @staticmethod
    def test_nested_dicts() -> None:
        test_tuple = tuple_example()

        assert test_tuple[-1] == {"foo": 0, "bar": 1}
        assert dig(test_tuple, -1) == {"foo": 0, "bar": 1}

        assert test_tuple[-1]["foo"] == 0
        assert dig(test_tuple, -1, "foo") == 0

        assert test_tuple[-1]["bar"] == 1
        assert dig(test_tuple, -1, "bar") == 1

    @staticmethod
    def test_nested_objects_with_seek_objects_as_true() -> None:
        test_tuple = tuple_example()

        assert type(test_tuple[3]) is SomeObject
        assert type(dig(test_tuple, 3, dig_objects=True)) is SomeObject

        assert test_tuple[3].nested_dict == {"nested_array": [9, 8, 7]}
        assert dig(test_tuple, 3, "nested_dict", dig_objects=True) == {
            "nested_array": [9, 8, 7]
        }

        assert test_tuple[3].nested_dict["nested_array"] == [9, 8, 7]
        assert dig(test_tuple, 3, "nested_dict", "nested_array", dig_objects=True) == [
            9,
            8,
            7,
        ]

        assert test_tuple[3].nested_dict["nested_array"][0] == 9
        result = dig(test_tuple, 3, "nested_dict", "nested_array", 0, dig_objects=True)
        assert result == 9

        assert test_tuple[3].nested_dict["nested_array"][-1] == 7
        result = dig(test_tuple, 3, "nested_dict", "nested_array", -1, dig_objects=True)
        assert result == 7


class TestDigSuccessWithArrayInput:
    """Test the method's happy path with array as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_array = array_example()

        assert test_array[0] == "This is a string inside array"
        assert dig(test_array, 0) == "This is a string inside array"

        assert test_array[0][0] == "T"
        assert dig(test_array, 0, 0) == "T"

        assert test_array[0][-1] == "y"
        assert dig(test_array, 0, -1) == "y"

    @staticmethod
    def test_nested_arrays() -> None:
        test_array = array_example()

        assert test_array[1] == ["a", "b", "c"]
        assert dig(test_array, 1) == ["a", "b", "c"]

        assert test_array[1][0] == "a"
        assert dig(test_array, 1, 0) == "a"

        assert test_array[1][-1] == "c"
        assert dig(test_array, 1, -1) == "c"

    @staticmethod
    def test_nested_tuples() -> None:
        test_array = array_example()

        assert test_array[2] == ("x", "y", "z")
        assert dig(test_array, 2) == ("x", "y", "z")

        assert test_array[2][0] == "x"
        assert dig(test_array, 2, 0) == "x"

        assert test_array[2][-1] == "z"
        assert dig(test_array, 2, -1) == "z"

    @staticmethod
    def test_nested_dicts() -> None:
        test_array = array_example()

        assert test_array[-1] == {"foo": 0, "bar": 1}
        assert dig(test_array, -1) == {"foo": 0, "bar": 1}

        assert test_array[-1]["foo"] == 0
        assert dig(test_array, -1, "foo") == 0

        assert test_array[-1]["bar"] == 1
        assert dig(test_array, -1, "bar") == 1

    @staticmethod
    def test_nested_objects_with_seek_objects_as_true() -> None:
        test_array = array_example()

        assert type(test_array[3]) is SomeObject
        assert type(dig(test_array, 3, dig_objects=True)) is SomeObject

        assert test_array[3].nested_dict == {"nested_array": [9, 8, 7]}
        assert dig(test_array, 3, "nested_dict", dig_objects=True) == {
            "nested_array": [9, 8, 7]
        }

        assert test_array[3].nested_dict["nested_array"] == [9, 8, 7]
        assert dig(test_array, 3, "nested_dict", "nested_array", dig_objects=True) == [
            9,
            8,
            7,
        ]

        assert test_array[3].nested_dict["nested_array"][0] == 9
        result = dig(test_array, 3, "nested_dict", "nested_array", 0, dig_objects=True)
        assert result == 9

        assert test_array[3].nested_dict["nested_array"][-1] == 7
        result = dig(test_array, 3, "nested_dict", "nested_array", -1, dig_objects=True)
        assert result == 7


class TestDigSuccessWithObjectInput:
    """Test the method's happy path with object as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_obj = SomeObject()

        assert test_obj.nested_string == "This is a string inside object"
        assert (
            dig(test_obj, "nested_string", dig_objects=True)
            == "This is a string inside object"
        )

        assert test_obj.nested_string[0] == "T"
        assert dig(test_obj, "nested_string", 0, dig_objects=True) == "T"

        assert test_obj.nested_string[-1] == "t"
        assert dig(test_obj, "nested_string", -1, dig_objects=True) == "t"

    @staticmethod
    def test_nested_dicts() -> None:
        test_obj = SomeObject()

        assert test_obj.nested_dict == {"nested_array": [9, 8, 7]}
        assert dig(test_obj, "nested_dict", dig_objects=True) == {
            "nested_array": [9, 8, 7]
        }

        assert test_obj.nested_dict == {"nested_array": [9, 8, 7]}
        assert dig(test_obj, "nested_dict", "nested_array", dig_objects=True) == [
            9,
            8,
            7,
        ]

    @staticmethod
    def test_nested_pydantic_models() -> None:
        test_obj = SomeObject()

        assert isinstance(test_obj.nested_pydatic_model, BaseModel)
        assert isinstance(
            dig(test_obj, "nested_pydatic_model", dig_objects=True), BaseModel
        )

        assert test_obj.nested_pydatic_model.nested_dict["a"] == 1
        assert (
            dig(test_obj, "nested_pydatic_model", "nested_dict", "a", dig_objects=True)
            == 1
        )


class TestSeekSuccessWithPydanticModelInput:
    """Test the method's happy path with object as initial input."""

    @staticmethod
    def test_nested_strings() -> None:
        test_obj = PydanticModel()

        assert test_obj.name == "John Doe"
        assert dig(test_obj, "name", dig_objects=True) == "John Doe"

        assert test_obj.name[0] == "J"
        assert dig(test_obj, "name", 0, dig_objects=True) == "J"

        assert test_obj.name[-1] == "e"
        assert dig(test_obj, "name", -1, dig_objects=True) == "e"

    @staticmethod
    def test_nested_dicts() -> None:
        test_obj = PydanticModel()

        assert test_obj.nested_dict == {"a": 1}
        assert dig(test_obj, "nested_dict", dig_objects=True) == {"a": 1}

        assert test_obj.nested_dict["a"] == 1
        assert dig(test_obj, "nested_dict", "a", dig_objects=True) == 1


class TestDigSuccessWithStringInput:
    """Test the method's happy path with string as initial input."""

    @staticmethod
    def test_strings() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        assert test_str == "Lorem ipsum dolor sit amet"
        assert dig(test_str) == "Lorem ipsum dolor sit amet"

        assert test_str[0] == "L"
        assert dig(test_str, 0) == "L"

        assert test_str[-1] == "t"
        assert dig(test_str, -1) == "t"
