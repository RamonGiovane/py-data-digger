from types import BuiltinFunctionType

from pytest import raises

from src.py_data_digger import dig
from tests.py_data_digger.conftest import dict_example


class TestDigFailureWithDictInput:
    """Test the method's sad path with dict as initial input."""

    @staticmethod
    def test_dict_key_error() -> None:
        test_dict = dict_example()

        with raises(KeyError):
            test_dict["unknow_key"]

        assert dig(test_dict, "unknow_key") is None

    @staticmethod
    def test_dict_nested_key_error() -> None:
        test_dict = dict_example()

        with raises(KeyError):
            test_dict["nested_dict"]["sub_item_dict"]["unknow_key"]

        assert dig(test_dict, "nested_dict", "sub_item_dict", "unknow_key") is None


class TestDigFailureWithStringInput:
    """Test the method's sad path with string as initial input."""

    @staticmethod
    def test_string_index_error() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        with raises(IndexError):
            test_str[1000]

        assert dig(test_str, 1000) is None

    @staticmethod
    def test_string_index_error_on_substring() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        with raises(IndexError):
            test_str[0][1]

        assert dig(test_str, 0, 1) is None

    @staticmethod
    def test_string_type_error_indices_must_be_integers() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        with raises(TypeError) as ex_info:
            test_str["islower"]
        assert "string indices must be integers, not 'str'" in str(ex_info.value)

        assert dig(test_str, "islower") is None
        assert dig(test_str, "islower", dig_objects=True) is not None
        assert type(dig(test_str, "islower", dig_objects=True)) is BuiltinFunctionType

    @staticmethod
    def test_string_attribute_error_when_dig_objects_is_on_but_there_is_no_attribute_with_given_name() -> (
        None
    ):
        test_str = "Lorem ipsum dolor sit amet"

        with raises(AttributeError) as ex_info:
            getattr(test_str, "_islower2")  # noqa: B009
        assert "'str' object has no attribute '_islower2'" in str(ex_info.value)
