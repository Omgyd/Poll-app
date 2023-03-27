from typing import List
from connection import get_connection
import datetime
import pytz
import database


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.text = option_text
        self.poll_id = poll_id
        self.id = _id


    def __repr__(self):
        return f"Option({self.text!r}, {self.poll_id!r}, {self.id!r})"
    

    def save(self):
        with get_connection() as connection:
            new_option_id = database.add_options(connection, self.text, self.poll_id)
            self.id = new_option_id


    @classmethod
    def get(cls, option_id: int) -> "Option":
        with get_connection() as connection:
            option = database.get_options(connection, option_id)
            return cls(option[1], option[2], option[0])

    def vote(self, username: str):
        with get_connection() as connection:
            datetime_utc = datetime.datetime.now(tz=pytz.utc)
            current_timestamp = datetime_utc.timestamp()
            database.add_poll_vote(connection, username, current_timestamp, self.id)


    @property
    def votes(self):
        with get_connection() as connection:
            votes = database.get_votes_for_option(connection, self.id)
            return votes