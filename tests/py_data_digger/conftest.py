from typing import Optional

from pydantic import BaseModel, Field


class PydanticModel(BaseModel):
    name: Optional[str] = Field(default="John Doe")
    nested_dict: Optional[dict] = Field(default_factory=lambda: {"a": 1})


class SomeObject:
    def __init__(self) -> None:
        self.nested_dict = {"nested_array": [9, 8, 7]}
        self.nested_string = "This is a string inside object"
        self.nested_pydatic_model = PydanticModel()


def dict_example() -> dict:
    """Dict example with all sorts of nested data: lists, arrays, dicts, strings and objects."""
    return {
        "string_item": "This is a string",
        "object_item": SomeObject(),
        "nested_dict": {
            "sub_item_array": [1, 2, 3],
            "sub_item_string": "Another string",
            "sub_item_dict": {"a": 0, "b": 1},
            "sub_item_tuple": ("x", "y", "z"),
            "sub_item_object": SomeObject(),
        },
        "keys": ["The key 1", "The key 2"],
    }


def tuple_example() -> dict:
    """Tuple example with some nested data."""
    return (
        "This is a string inside tuple",
        ["a", "b", "c"],
        ("x", "y", "z"),
        SomeObject(),
        {"foo": 0, "bar": 1},
    )


def array_example() -> dict:
    """Array example with some nested data."""
    return [
        "This is a string inside array",
        ["a", "b", "c"],
        ("x", "y", "z"),
        SomeObject(),
        {"foo": 0, "bar": 1},
    ]
