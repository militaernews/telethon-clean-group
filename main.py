import asyncio

import requests
from pyrogram import Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.raw.types import UserStatusLastMonth, UserStatusEmpty
from pyrogram.types import User

import config


def check_cas(user_id: int):
    response = requests.get(f"https://api.cas.chat/check?user_id={user_id}")
    print(user_id, response.json())
    return response.json()["ok"]


async def is_scam(user: User):
    is_cas_banned = check_cas(user.id)

    return is_cas_banned or user.is_fake or user.is_scam


def is_inactive(user: User):
    statuses = [UserStatusEmpty, UserStatusLastMonth] if config.strict else [UserStatusEmpty]

    return user.is_deleted or isinstance(user.status, tuple(statuses)) or (user.status is None and not user.is_bot)


async def clear_chat():
    client = Client(
        name="clean_group",
        api_id=config.api_id,
        api_hash=config.api_hash,
        phone_number=config.NUMBER,

    )

    await client.start()

    deleted_accounts = 0
    async for member in client.get_chat_members(config.GROUP, filter=ChatMembersFilter.SEARCH):
        user = member.user
        print(vars(user))

        if await is_scam(user) or is_inactive(user):
            print("try kicking...\n")
            try:
                deleted_accounts += 1

                if not config.testing:
                    await client.ban_chat_member(
                        chat_id=config.GROUP,
                        user_id=user.id
                    )

            except Exception as exc:
                print(f"Failed to kick one deleted account because: {str(exc)}")
        await asyncio.sleep(0.5)

    if deleted_accounts:
        print(f"Kicked {deleted_accounts} Deleted Accounts")
    else:
        print("No deleted accounts found in group")


if __name__ == "__main__":
    asyncio.run(clear_chat())
