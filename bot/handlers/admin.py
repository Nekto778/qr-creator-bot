from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from ..states import AdminBroadcast, AdminChannels
from ..config import ADMINS
from ..database import db
from ..emojis import emoji
from ..keyboards import admin_panel_kb, admin_channels_kb, broadcast_confirm_kb, main_menu_kb

router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMINS


@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer("Access denied.", show_alert=True)
        return
    await callback.answer()
    await callback.message.edit_text(
        f"{emoji('gear')} Admin Panel",
        reply_markup=admin_panel_kb(),
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    total_users = await db.get_user_count()
    total_qr = await db.get_qr_count()
    new_users, today_qr = await db.get_today_stats()
    channels = await db.get_channels()
    text = (
        f"{emoji('chart')} Statistics\n\n"
        f"👥 Total users: <b>{total_users}</b>\n"
        f"🆕 New today: <b>{new_users}</b>\n"
        f"📊 Total QR codes: <b>{total_qr}</b>\n"
        f"📈 QR today: <b>{today_qr}</b>\n"
        f"📢 Required channels: <b>{len(channels)}</b>"
    )
    await callback.message.edit_text(text, reply_markup=admin_panel_kb())


@router.callback_query(F.data == "admin_broadcast")
async def broadcast_start(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    await callback.message.edit_text(
        f"{emoji('loudspeaker')} Send me the broadcast message text:"
    )
    await state.set_state(AdminBroadcast.entering_text)


@router.message(AdminBroadcast.entering_text)
async def broadcast_text(message: Message, state: FSMContext):
    await state.update_data(bc_text=message.text)
    await message.answer(
        f"{emoji('loudspeaker')} Preview:\n\n{message.text}\n\nSend this to all users?",
        reply_markup=broadcast_confirm_kb(),
    )
    await state.set_state(AdminBroadcast.confirming)


@router.callback_query(F.data == "bc_confirm", AdminBroadcast.confirming)
async def broadcast_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    data = await state.get_data()
    text = data.get("bc_text", "")
    users = await db.get_active_users()
    sent = 0
    failed = 0

    await callback.message.edit_text(f"{emoji('loudspeaker')} Sending... 0/{len(users)}")

    for (user_id,) in users:
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except Exception:
            failed += 1
            await db.block_user(user_id)

    await db.add_broadcast(callback.from_user.id, text, sent, failed)
    await callback.message.edit_text(
        f"{emoji('check')} Broadcast complete!\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}\n"
        f"📊 Total: {len(users)}",
        reply_markup=admin_panel_kb(),
    )
    await state.clear()


@router.callback_query(F.data == "bc_cancel", AdminBroadcast.confirming)
async def broadcast_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        f"{emoji('cross')} Broadcast cancelled.",
        reply_markup=admin_panel_kb(),
    )
    await state.clear()


@router.callback_query(F.data == "admin_channels")
async def admin_channels(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    channels = await db.get_channels()
    if not channels:
        await callback.message.edit_text(
            f"{emoji('people')} No required channels.\nAdd one below:",
            reply_markup=admin_channels_kb([]),
        )
    else:
        text = f"{emoji('people')} Required Channels:\n\n"
        for ch_id, ch_title, _ in channels:
            text += f"📢 {ch_title} (ID: <code>{ch_id}</code>)\n"
        await callback.message.edit_text(text, reply_markup=admin_channels_kb(channels))


@router.callback_query(F.data == "admin_add_channel")
async def add_channel_start(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    await callback.message.edit_text(
        "Send me the channel ID or @username\n"
        "(Bot must be admin in the channel):"
    )
    await state.set_state(AdminChannels.entering_channel)


@router.message(AdminChannels.entering_channel)
async def process_channel(message: Message, state: FSMContext, bot: Bot):
    raw = message.text.strip()
    try:
        if raw.startswith("@"):
            chat = await bot.get_chat(raw)
        else:
            chat = await bot.get_chat(int(raw))
        await db.add_channel(chat.id, chat.title or raw, chat.invite_link or "")
        await message.answer(
            f"{emoji('check')} Channel added: {chat.title or raw}",
            reply_markup=admin_panel_kb(),
        )
    except Exception as e:
        await message.answer(
            f"{emoji('cross')} Failed. Make sure the bot is admin.\nError: {e}",
            reply_markup=admin_panel_kb(),
        )
    await state.clear()


@router.callback_query(F.data.startswith("rmch_"))
async def remove_channel(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    channel_id = int(callback.data.replace("rmch_", ""))
    await db.remove_channel(channel_id)
    channels = await db.get_channels()
    if channels:
        text = f"{emoji('people')} Required Channels:\n\n"
        for ch_id, ch_title, _ in channels:
            text += f"📢 {ch_title} (ID: <code>{ch_id}</code>)\n"
        await callback.message.edit_text(text, reply_markup=admin_channels_kb(channels))
    else:
        await callback.message.edit_text(
            f"{emoji('people')} No required channels.",
            reply_markup=admin_channels_kb([]),
        )
