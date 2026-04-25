from aiogram import Bot


async def check_subscriptions(bot: Bot, user_id: int, channels: list) -> list:
    not_subscribed = []
    for channel_id, channel_title, invite_link in channels:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status in ("left", "kicked"):
                not_subscribed.append((channel_id, channel_title, invite_link))
        except Exception:
            not_subscribed.append((channel_id, channel_title, invite_link))
    return not_subscribed
