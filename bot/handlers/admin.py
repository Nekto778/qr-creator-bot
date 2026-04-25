from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from ..states import AdminBroadcast, AdminChannels
from ..config import ADMINS
from ..database import db
from ..i18n import t
from ..emojis import pe, ec
from ..keyboards import admin_panel_kb, admin_channels_kb, broadcast_confirm_kb, main_menu_kb

router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMINS


@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer(t("access_denied", "en"), show_alert=True)
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("admin_panel", lang),
        reply_markup=admin_panel_kb(lang),
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    total_users = await db.get_user_count()
    total_qr = await db.get_qr_count()
    new_users, today_qr = await db.get_today_stats()
    channels = await db.get_channels()
    text = t("stats_text", lang,
             total=total_users, new=new_users,
             qr_total=total_qr, qr_today=today_qr,
             channels=len(channels))
    await callback.message.edit_text(text, reply_markup=admin_panel_kb(lang))


@router.callback_query(F.data == "admin_broadcast")
async def broadcast_start(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t("bc_enter", lang))
    await state.set_state(AdminBroadcast.entering_text)


@router.message(AdminBroadcast.entering_text)
async def broadcast_text(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.update_data(bc_text=message.text)
    await message.answer(
        t("bc_preview", lang, text=message.text),
        reply_markup=broadcast_confirm_kb(lang),
    )
    await state.set_state(AdminBroadcast.confirming)


@router.callback_query(F.data == "bc_confirm", AdminBroadcast.confirming)
async def broadcast_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    data = await state.get_data()
    text = data.get("bc_text", "")
    users = await db.get_active_users()
    sent = 0
    failed = 0

    await callback.message.edit_text(t("bc_sending", lang, total=len(users)))

    for (user_id,) in users:
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except Exception:
            failed += 1
            await db.block_user(user_id)

    await db.add_broadcast(callback.from_user.id, text, sent, failed)
    await callback.message.edit_text(
        t("bc_done", lang, sent=sent, failed=failed, total=len(users)),
        reply_markup=admin_panel_kb(lang),
    )
    await state.clear()


@router.callback_query(F.data == "bc_cancel", AdminBroadcast.confirming)
async def broadcast_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("bc_cancelled", lang),
        reply_markup=admin_panel_kb(lang),
    )
    await state.clear()


@router.callback_query(F.data == "admin_channels")
async def admin_channels(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    channels = await db.get_channels()
    if not channels:
        await callback.message.edit_text(
            t("ch_none", lang),
            reply_markup=admin_channels_kb(lang, []),
        )
    else:
        text = t("ch_list", lang)
        for ch_id, ch_title, _ in channels:
            text += f"{pe('loudspeaker')} {ch_title} (ID: <code>{ch_id}</code>)\n"
        await callback.message.edit_text(text, reply_markup=admin_channels_kb(lang, channels))


@router.callback_query(F.data == "admin_add_channel")
async def add_channel_start(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t("ch_prompt", lang))
    await state.set_state(AdminChannels.entering_channel)


@router.message(AdminChannels.entering_channel)
async def process_channel(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    raw = message.text.strip()
    try:
        if raw.startswith("@"):
            chat = await bot.get_chat(raw)
        else:
            chat = await bot.get_chat(int(raw))
        await db.add_channel(chat.id, chat.title or raw, chat.invite_link or "")
        await message.answer(
            t("ch_added", lang, title=chat.title or raw),
            reply_markup=admin_panel_kb(lang),
        )
    except Exception as e:
        await message.answer(
            t("ch_failed", lang, err=str(e)),
            reply_markup=admin_panel_kb(lang),
        )
    await state.clear()


@router.callback_query(F.data.startswith("rmch_"))
async def remove_channel(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        return
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    channel_id = int(callback.data.replace("rmch_", ""))
    await db.remove_channel(channel_id)
    channels = await db.get_channels()
    if channels:
        text = t("ch_list", lang)
        for ch_id, ch_title, _ in channels:
            text += f"{pe('loudspeaker')} {ch_title} (ID: <code>{ch_id}</code>)\n"
        await callback.message.edit_text(text, reply_markup=admin_channels_kb(lang, channels))
    else:
        await callback.message.edit_text(
            t("ch_none", lang),
            reply_markup=admin_channels_kb(lang, []),
        )
