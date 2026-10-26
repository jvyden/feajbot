import asyncio
from datetime import datetime, timedelta
import random
from typing import override

from maubot import Plugin
from mautrix.types import TextMessageEventContent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper


class Config(BaseProxyConfig):
    @override
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("room_id");

class FeajBot(Plugin):
    @override
    async def start(self) -> None:
        if not self.config:
            raise TypeError("no config found");
        self.config.load_and_update();

    @override
    @classmethod
    def get_config_class(cls) -> type[BaseProxyConfig]:
        return Config

    async def meow(self) -> None:
        self.log.info("meowing");
        if not self.config:
            raise TypeError("no config found");
        roomId: str | None = self.config.get("room_id", None);

        if not roomId:
            return;

        rooms = await self.client.get_joined_rooms();
        room = None;

        for innerRoom in rooms:
            if innerRoom != roomId:
                continue;

            room = innerRoom;
            break;


        if not room:
            return;

        content = TextMessageEventContent(body="meow")

        _ = await self.client.send_message(room, content);

    async def bot_loop(self) -> None:
        try:
            self.log.debug("Bot loop started")
            while True:
                now = datetime.now()
                # minutes = random.randrange(15, 120);
                minutes = random.randrange(1, 3);
                next_minute = (now + timedelta(minutes=minutes)).replace(second=0, microsecond=0)
                await asyncio.sleep((next_minute - now).total_seconds())
                await self.meow();
        except asyncio.CancelledError:
            self.log.debug("Bot loop stopped")
        except Exception:
            self.log.exception("Bot in reminder loop")
