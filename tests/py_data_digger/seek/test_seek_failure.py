from pytest import raises

from src.py_data_digger import SeekError, seek
from tests.py_data_digger.conftest import dict_example


class TestSeekFailureWithDictInput:
    """Test the method's sad path with dict as initial input."""

    @staticmethod
    def test_dict_key_error() -> None:
        test_dict = dict_example()

        with raises(KeyError):
            test_dict["unknow_key"]

        with raises(SeekError) as ex_info:
            seek(test_dict, "unknow_key")

        assert type(ex_info.value.__cause__) is KeyError
        assert "Path traveled: dict -> unknow_key" in ex_info.value.message

    @staticmethod
    def test_dict_nested_key_error() -> None:
        test_dict = dict_example()

        with raises(KeyError):
            test_dict["nested_dict"]["sub_item_dict"]["unknow_key"]

        with raises(SeekError) as ex_info:
            seek(test_dict, "nested_dict", "sub_item_dict", "unknow_key")

        assert type(ex_info.value.__cause__) is KeyError
        assert (
            "Path traveled: dict -> nested_dict -> sub_item_dict -> unknow_key"
            in ex_info.value.message
        )


class TestSeekFailureWithStringInput:
    """Test the method's sad path with string as initial input."""

    @staticmethod
    def test_string_index_error() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        with raises(IndexError):
            test_str[1000]

        with raises(SeekError) as ex_info:
            seek(test_str, 1000)

        assert type(ex_info.value.__cause__) is IndexError
        assert "Path traveled: str -> 1000" in ex_info.value.message

    @staticmethod
    def test_string_index_error_on_substring() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        with raises(IndexError):
            test_str[0][1]

        with raises(SeekError) as ex_info:
            seek(test_str, 0, 1)

        assert type(ex_info.value.__cause__) is IndexError
        assert "Path traveled: str -> 0" in ex_info.value.message

    @staticmethod
    def test_string_type_error_indices_must_be_integers() -> None:
        test_str = "Lorem ipsum dolor sit amet"

        with raises(TypeError) as ex_info:
            test_str["islower"]
        assert "string indices must be integers, not 'str'" in str(ex_info.value)

        with raises(SeekError) as ex_info:
            seek(test_str, "islower")

        assert type(ex_info.value.__cause__) is TypeError
        assert "Path traveled: str -> islower" in ex_info.value.message

    @staticmethod
    def test_string_attribute_error_when_seek_objects_is_on_but_there_is_no_attribute_with_given_name() -> (
        None
    ):
        test_str = "Lorem ipsum dolor sit amet"

        with raises(AttributeError) as ex_info:
            getattr(test_str, "_islower2")  # noqa: B009
        assert "'str' object has no attribute '_islower2'" in str(ex_info.value)

        with raises(SeekError) as ex_info:
            seek(test_str, "_islower2", seek_objects=True)

        assert type(ex_info.value.__cause__) is AttributeError
        assert type(ex_info.value.__cause__) is AttributeError
        assert "'str' object has no attribute '_islower2'" in str(
            ex_info.value.__cause__
        )
        assert "Path traveled: str -> _islower2" in ex_info.value.message
