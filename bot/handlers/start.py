from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from ..config import ADMINS
from ..database import db
from ..i18n import t
from ..keyboards import main_menu_kb, language_kb
from ..states import LanguageSelect

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    exists = await db.user_exists(message.from_user.id)
    if not exists:
        await message.answer(t("choose_lang"), reply_markup=language_kb())
        await state.set_state(LanguageSelect.choosing)
        return
    lang = await db.get_user_lang(message.from_user.id)
    is_admin = message.from_user.id in ADMINS
    await message.answer(
        t("welcome", lang),
        reply_markup=main_menu_kb(lang, is_admin),
    )


@router.callback_query(F.data.startswith("lang_"), LanguageSelect.choosing)
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.replace("lang_", "")
    if lang not in ("en", "ru"):
        lang = "en"
    await callback.answer()
    if not await db.user_exists(callback.from_user.id):
        await db.add_user(
            callback.from_user.id,
            callback.from_user.username,
            callback.from_user.first_name,
            language=lang,
        )
    else:
        await db.set_user_lang(callback.from_user.id, lang)
    is_admin = callback.from_user.id in ADMINS
    await callback.message.edit_text(
        t("lang_set", lang) + "\n\n" + t("welcome", lang),
        reply_markup=main_menu_kb(lang, is_admin),
    )
    await state.clear()


@router.callback_query(F.data == "change_lang")
async def change_lang(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        t("choose_lang", await db.get_user_lang(callback.from_user.id)),
        reply_markup=language_kb(),
    )


@router.callback_query(F.data.startswith("lang_"))
async def change_lang_select(callback: CallbackQuery):
    lang = callback.data.replace("lang_", "")
    if lang not in ("en", "ru"):
        lang = "en"
    await callback.answer()
    await db.set_user_lang(callback.from_user.id, lang)
    is_admin = callback.from_user.id in ADMINS
    await callback.message.edit_text(
        t("lang_set", lang),
        reply_markup=main_menu_kb(lang, is_admin),
    )


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await db.get_user_lang(callback.from_user.id)
    is_admin = callback.from_user.id in ADMINS
    await callback.answer()
    try:
        await callback.message.edit_text(
            t("main_menu", lang),
            reply_markup=main_menu_kb(lang, is_admin),
        )
    except Exception:
        await callback.message.answer(
            t("main_menu", lang),
            reply_markup=main_menu_kb(lang, is_admin),
        )


@router.callback_query(F.data == "my_qr")
async def my_qr_codes(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.answer()
    count = await db.get_user_qr_count(callback.from_user.id)
    is_admin = callback.from_user.id in ADMINS
    await callback.message.edit_text(
        t("my_qr", lang, count=count),
        reply_markup=main_menu_kb(lang, is_admin),
    )
