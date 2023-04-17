import datetime
import json
from abc import abstractmethod


class Serializable:
    def serialize(self) -> str:
        return json.dumps(self.to_json())

    @abstractmethod
    def to_json(self):
        pass


def format_date(date: datetime.datetime):
    return date.strftime("%Y-%m-%d %H:%M:%S")
