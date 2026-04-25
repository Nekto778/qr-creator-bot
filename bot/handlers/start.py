from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from ..config import ADMINS
from ..database import db
from ..emojis import emoji
from ..keyboards import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )
    is_admin = message.from_user.id in ADMINS
    await message.answer(
        f"{emoji('wave')} Welcome to <b>QR Generator Bot</b>!\n\n"
        f"Create custom QR codes with advanced design:\n"
        f"• 🔗 Multiple types (URL, text, WiFi, etc.)\n"
        f"• 🎨 Custom colors & gradients\n"
        f"• ⬛ Rounded/dotted dot styles\n"
        f"• 🖼 Center icon support\n"
        f"• 📄 PNG & SVG export\n"
        f"• ⚡ Inline mode in any chat\n\n"
        f"Choose an option:",
        reply_markup=main_menu_kb(is_admin),
    )


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    is_admin = callback.from_user.id in ADMINS
    await callback.answer()
    try:
        await callback.message.edit_text(
            f"{emoji('wave')} Main Menu",
            reply_markup=main_menu_kb(is_admin),
        )
    except Exception:
        await callback.message.answer(
            f"{emoji('wave')} Main Menu",
            reply_markup=main_menu_kb(is_admin),
        )


@router.callback_query(F.data == "my_qr")
async def my_qr_codes(callback: CallbackQuery):
    await callback.answer()
    count = await db.get_user_qr_count(callback.from_user.id)
    is_admin = callback.from_user.id in ADMINS
    await callback.message.edit_text(
        f"{emoji('book')} Your QR Codes\n\n"
        f"📊 Total generated: <b>{count}</b>\n\n"
        f"Generate a new one from the main menu!",
        reply_markup=main_menu_kb(is_admin),
    )
