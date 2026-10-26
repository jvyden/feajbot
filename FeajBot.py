import asyncio
import random
from datetime import datetime, timedelta
from typing import override

from maubot import Plugin
from mautrix.types import TextMessageEventContent
from mautrix.types.event.message import MessageType
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper


class Config(BaseProxyConfig):
    @override
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("room_id");

class FeajBot(Plugin):
    loop_task: asyncio.Future

    @override
    async def start(self) -> None:
        if not self.config:
            raise TypeError("no config found");
        self.config.load_and_update();
        self.loop_task = asyncio.create_task(self.bot_loop())
        await self.meow();

    @override
    async def stop(self) -> None:
        _ = self.loop_task.cancel()

    @override
    @classmethod
    def get_config_class(cls) -> type[BaseProxyConfig]:
        return Config

    async def meow(self) -> None:
        self.log.info("meowing");
        if not self.config:
            raise TypeError("no config found");
        roomId: str | None = self.config.get("room_id", None);  # pyright: ignore[reportAny]

        if not roomId:
            self.log.warning("could not find room id");
            return;

        rooms = await self.client.get_joined_rooms();
        room = None;

        for innerRoom in rooms:
            if innerRoom != roomId:
                continue;

            room = innerRoom;
            break;


        if not room:
            self.log.warning("could not find room");
            return;

        content = TextMessageEventContent(body="meow", msgtype=MessageType.TEXT)

        _ = await self.client.send_message(room, content);

    async def bot_loop(self) -> None:
        try:
            self.log.debug("Bot loop started")
            while True:
                now = datetime.now()
                minutes = random.randrange(1, 120);
                self.log.info(f"will meow in {minutes} minutes next")
                next_minute = (now + timedelta(minutes=minutes)).replace(second=0, microsecond=0)
                await asyncio.sleep((next_minute - now).total_seconds())
                await self.meow();
        except asyncio.CancelledError:
            self.log.debug("Bot loop stopped")
        except Exception:
            self.log.exception("Error in bot loop")
