import asyncio
import datetime

from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, UserStatusLastMonth

import config

api_id = 12345
api_hash = 'paste it here'


async def clear_chat(client):
    deleted_accounts = 0
    async for user in client.iter_participants(config.GROUP):
        print(user)
        if user.deleted or user.status is UserStatusLastMonth:
            try:
                deleted_accounts += 1
                await client(EditBannedRequest(config.GROUP, user, ChatBannedRights(
                    until_date=datetime.timedelta(minutes=1),
                    view_messages=True
                )))
            except Exception as exc:
                print(f"Failed to kick one deleted account because: {str(exc)}")

    if deleted_accounts:
        print(f"Kicked {deleted_accounts} Deleted Accounts")
    else:
        print(f"No deleted accounts found in group")


if __name__ == "__main__":
    with TelegramClient("remove_inactive", api_id, api_hash) as tgclient:
        asyncio.get_event_loop().run_until_complete(clear_chat(tgclient))
