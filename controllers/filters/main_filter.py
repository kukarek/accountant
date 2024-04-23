from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
import os
from misc.settings import Settings

class isUser(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        for user in Settings().admins:
            if user == message.from_id:
                return True
            
        return False
