from typing import Sequence, Dict

from app.models.item import Item
from app.models.item_type import ItemType


def items_to_dict(items: Sequence[Item]) -> Dict[ItemType, int]:
    d = dict()
    for i in items:
        d[i.item_type] = d.get(i.item_type, 0) + 1
    return d
