import asyncio
import datetime

import requests
from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, UserStatusLastMonth, UserStatusEmpty

import config


async def check_cas(user_id: int):
    response = requests.get(f"https://api.cas.chat/check?user_id={user_id}")
    print(user_id, response.json())
    return response.json()["ok"]


async def is_scam(user):
    is_cas_banned = await check_cas(user.id)

    return is_cas_banned or user.fake or user.scam


def is_inactive(user):
    statuses = [UserStatusEmpty]

    if config.strict:
        statuses += UserStatusLastMonth

    return user.deleted or type(user.status) in statuses or (user.status is None and not user.bot)


async def clear_chat(client):
    deleted_accounts = 0
    async for user in client.iter_participants(config.GROUP):
        print(vars(user))

        if await is_scam(user) or is_inactive(user):
            print("try kicking...\n")
            try:
                deleted_accounts += 1

                if not config.testing:
                    await client(EditBannedRequest(config.GROUP, user, ChatBannedRights(
                        until_date=datetime.timedelta(minutes=1),
                        view_messages=True
                    )))

            except Exception as exc:
                print(f"Failed to kick one deleted account because: {str(exc)}")
        await asyncio.sleep(0.5)

    if deleted_accounts:
        print(f"Kicked {deleted_accounts} Deleted Accounts")
    else:
        print(f"No deleted accounts found in group")


if __name__ == "__main__":
    with TelegramClient("remove_inactive", config.api_id, config.api_hash) as tgclient:
        asyncio.get_event_loop().run_until_complete(clear_chat(tgclient))
