from ruia.field import BaseField
from ruia import AttrField, Item, Request, Spider, TextField
import os

class ItemMeta(type):
    """
    Metaclass for an item
    """

    def __new__(cls, name, bases, attrs):
        __fields = dict(
            {
                (field_name, attrs.pop(field_name))
                for field_name, object in list(attrs.items())
                if isinstance(object, BaseField)
            }
        )
        print(__fields)
        attrs["__fields"] = __fields
        new_class = type.__new__(cls, name, bases, attrs)
        return new_class

class Item(metaclass=ItemMeta):
    title = TextField(css_select='h4.result_header > a')
    href = TextField(css_select='div.external-link > span.url')
    @classmethod
    def get_items(cls):
        items_field = getattr(cls, "__fields", {}).get("target_item", None)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))