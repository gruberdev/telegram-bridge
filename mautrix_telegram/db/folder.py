# mautrix-telegram - A Matrix-Telegram puppeting bridge
# Copyright (C) 2021 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional, Iterable

from sqlalchemy import Column, BigInteger, String, Boolean, Text, func, sql

from mautrix.types import RoomID, ContentURI
from mautrix.util.db import Base

from ..types import TelegramID


class Folder(Base):
    __tablename__ = "folder"

    # Telegram folder information
    tgid: TelegramID = Column(BigInteger, primary_key=True)
    tg_receiver: TelegramID = Column(BigInteger, primary_key=True)
    title: str = Column(String, nullable=False)
    emoticon: str = Column(String, nullable=True)

    # Matrix space information
    mxid: Optional[RoomID] = Column(String, unique=True, nullable=True)

    @classmethod
    def get_by_tgid(cls, tgid: TelegramID, tg_receiver: TelegramID) -> Optional['Portal']:
        return cls._select_one_or_none(cls.c.tgid == tgid, cls.c.tg_receiver == tg_receiver)

    @classmethod
    def find_private_chats(cls, tg_receiver: TelegramID) -> Iterable['Portal']:
        yield from cls._select_all(cls.c.tg_receiver == tg_receiver, cls.c.peer_type == "user")

    @classmethod
    def get_by_mxid(cls, mxid: RoomID) -> Optional['Portal']:
        return cls._select_one_or_none(cls.c.mxid == mxid)

    @classmethod
    def get_by_username(cls, username: str) -> Optional['Portal']:
        return cls._select_one_or_none(func.lower(cls.c.username) == username)

    @classmethod
    def all(cls) -> Iterable['Portal']:
        yield from cls._select_all()
