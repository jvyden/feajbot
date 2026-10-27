import asyncio
import random
from typing import override

from maubot import MessageEvent, Plugin
from maubot.handlers import command, event
from mautrix.types import EventType, TextMessageEventContent
from mautrix.types.event.message import MessageType
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper


class Config(BaseProxyConfig):
    @override
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("room_id");

class FeajBot(Plugin):
    loop_task: asyncio.Future
    mins_remaining: int = 5;

    @override
    async def start(self) -> None:
        if not self.config:
            raise TypeError("no config found");
        self.config.load_and_update();
        self.loop_task = asyncio.create_task(self.bot_loop())
        # await self.meow();

    @override
    async def stop(self) -> None:
        _ = self.loop_task.cancel()

    @override
    @classmethod
    def get_config_class(cls) -> type[BaseProxyConfig]:
        return Config

    def get_room_id(self) -> str:
        if not self.config:
            raise TypeError("no config found");
        roomId: str | None = self.config.get("room_id", None);  # pyright: ignore[reportAny]

        if not roomId:
            raise KeyError("could not find room id");

        return roomId;


    async def meow(self) -> None:
        self.log.info("meowing");
        room_id: str = self.get_room_id();

        rooms = await self.client.get_joined_rooms();
        room = None;

        for inner_room in rooms:
            if inner_room != room_id:
                continue;

            room = inner_room;
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
                await asyncio.sleep(60);
                self.mins_remaining -= 1;

                if self.mins_remaining <= 0:
                    minutes = random.randrange(10, 300);
                    self.log.info(f"will meow in {minutes} minutes next")
                    self.mins_remaining = minutes;
                    await self.meow();
        except asyncio.CancelledError:
            self.log.debug("Bot loop stopped")
        except Exception:
            self.log.exception("Error in bot loop")

    @command.passive("dean", case_insensitive=True)  # pyright: ignore[reportUntypedFunctionDecorator]
    async def dean_command(self, evt: MessageEvent, match: tuple[str]) -> None:
        _ = evt;
        _ = match;
        self.log.info("passive dean");
        await self.meow();

    @event.on(EventType.ROOM_MESSAGE)  # pyright: ignore[reportArgumentType, reportUntypedFunctionDecorator]
    async def handle_message(self, evt: MessageEvent) -> None:
        room_id: str = self.get_room_id();
        if evt.room_id != room_id:
            return;

        minutes = random.randrange(1, 2);
        self.mins_remaining -= minutes;
        self.log.info(f"lowering mins by {minutes}, now at {self.mins_remaining}");
