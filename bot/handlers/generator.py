import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from ..states import QRGeneration
from ..keyboards import (
    qr_type_kb, customize_kb, fill_color_kb, bg_color_kb,
    gradient_kb, dot_style_kb, format_kb, icon_kb,
    wifi_enc_kb, main_menu_kb, subscription_kb,
)
from ..emojis import emoji, ec
from ..config import ADMINS
from ..database import db
from ..services.qr_engine import qr_engine, encode_qr_data
from ..services.subscription import check_subscriptions

router = Router()

TYPE_PROMPTS = {
    "url": "🔗 Send me a URL (e.g., https://example.com):",
    "text": "📝 Send me the text to encode:",
    "phone": "📞 Send me a phone number (e.g., +1234567890):",
    "email": "📧 Send me an email address:",
    "sms": "💬 Send phone:message (e.g., +1234567890:Hello):",
}

TYPE_NAMES = {
    "url": "🔗 Link", "text": "📝 Text", "phone": "📞 Phone",
    "email": "📧 Email", "wifi": "📶 WiFi", "vcard": "👤 Contact",
    "sms": "💬 SMS",
}


def build_settings(data: dict, force_png: bool = False) -> dict:
    return {
        "fill_color": data.get("fill_color", "#000000"),
        "bg_color": data.get("bg_color", "#FFFFFF"),
        "bg_transparent": data.get("bg_transparent", False),
        "dot_style": data.get("dot_style", "square"),
        "format": "png" if force_png else data.get("format", "png"),
        "error_correction": data.get("error_correction", "H"),
        "gradient_enabled": data.get("gradient_enabled", False),
        "gradient_start": data.get("gradient_start", "#000000"),
        "gradient_end": data.get("gradient_end", "#0066FF"),
        "gradient_direction": data.get("gradient_direction", "horizontal"),
        "bg_gradient_enabled": data.get("bg_gradient_enabled", False),
        "bg_gradient_start": data.get("bg_gradient_start", "#FFFFFF"),
        "bg_gradient_end": data.get("bg_gradient_end", "#DDDDFF"),
        "bg_gradient_direction": data.get("bg_gradient_direction", "vertical"),
        "icon_path": data.get("icon_path"),
        "icon_size": 0.2,
    }


def fmt_text(data: dict) -> str:
    qr_type = TYPE_NAMES.get(data.get("qr_type", ""), "QR")
    fill = data.get("fill_color", "#000000")
    bg = "Transparent" if data.get("bg_transparent") else data.get("bg_color", "#FFFFFF")
    grad = "✅" if data.get("gradient_enabled") else "❌"
    bg_grad = "✅" if data.get("bg_gradient_enabled") else "❌"
    dot = data.get("dot_style", "square").title()
    fmt = data.get("format", "png").upper()
    icon = "✅" if data.get("icon_path") else "❌"
    return (
        f"🎨 {ec('gear')} QR Settings\n\n"
        f"📋 Type: {qr_type}\n"
        f"🎨 Fill: <code>{fill}</code>\n"
        f"🖼 BG: <code>{bg}</code>\n"
        f"🌈 Gradient: {grad}  |  BG Grad: {bg_grad}\n"
        f"⬛ Dot: {dot}  |  📄 Format: {fmt}\n"
        f"🖼 Icon: {icon}\n\n"
        f"{ec('lightning')} Customize or generate!"
    )


async def show_customize(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    qr_data = data.get("qr_data", "")
    if not qr_data:
        await callback.message.edit_text("Error. Start over.", reply_markup=main_menu_kb())
        await state.clear()
        return
    settings = build_settings(data, force_png=True)
    img = qr_engine.generate(qr_data, settings)
    text = fmt_text(data)
    media = InputMediaPhoto(
        media=BufferedInputFile(img.getvalue(), "qr_preview.png"),
        caption=text,
    )
    try:
        await callback.message.edit_media(media, reply_markup=customize_kb())
    except Exception:
        await callback.message.answer_photo(
            BufferedInputFile(img.getvalue(), "qr_preview.png"),
            caption=text,
            reply_markup=customize_kb(),
        )


@router.callback_query(F.data == "gen_start")
async def start_generation(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    channels = await db.get_channels()
    if channels:
        not_subbed = await check_subscriptions(bot, callback.from_user.id, channels)
        if not_subbed:
            await callback.message.edit_text(
                f"{emoji('shield')} Subscribe to all channels first:",
                reply_markup=subscription_kb(not_subbed),
            )
            await state.set_state(QRGeneration.choosing_type)
            return
    await callback.message.edit_text(
        f"{emoji('lightning')} Select QR code type:",
        reply_markup=qr_type_kb(),
    )
    await state.set_state(QRGeneration.choosing_type)


@router.callback_query(F.data == "sub_check")
async def check_sub(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    channels = await db.get_channels()
    not_subbed = await check_subscriptions(bot, callback.from_user.id, channels) if channels else []
    if not_subbed:
        await callback.answer("You haven't subscribed yet!", show_alert=True)
        return
    await callback.message.edit_text(
        f"{emoji('lightning')} Select QR code type:",
        reply_markup=qr_type_kb(),
    )
    await state.set_state(QRGeneration.choosing_type)


@router.callback_query(F.data.startswith("type_"), StateFilter(QRGeneration.choosing_type))
async def select_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    qr_type = callback.data.replace("type_", "")
    await state.update_data(qr_type=qr_type)
    if qr_type == "wifi":
        await callback.message.edit_text("📶 Send me the WiFi network name (SSID):")
        await state.set_state(QRGeneration.entering_wifi_ssid)
    elif qr_type == "vcard":
        await callback.message.edit_text("👤 Send me the contact name:")
        await state.set_state(QRGeneration.entering_vcard_name)
    elif qr_type in TYPE_PROMPTS:
        await callback.message.edit_text(TYPE_PROMPTS[qr_type])
        await state.set_state(QRGeneration.entering_data)
    else:
        await callback.message.edit_text("Unknown type.", reply_markup=qr_type_kb())


@router.message(QRGeneration.entering_data)
async def process_simple_data(message: Message, state: FSMContext):
    data = await state.get_data()
    qr_type = data.get("qr_type", "text")
    qr_data = encode_qr_data(qr_type, message.text)
    await state.update_data(qr_data=qr_data, raw_data=message.text)
    data = await state.get_data()
    settings = build_settings(data, force_png=True)
    img = qr_engine.generate(qr_data, settings)
    await message.answer_photo(
        BufferedInputFile(img.getvalue(), "qr_preview.png"),
        caption=fmt_text(data),
        reply_markup=customize_kb(),
    )
    await state.set_state(QRGeneration.customizing)


@router.message(QRGeneration.entering_wifi_ssid)
async def wifi_ssid(message: Message, state: FSMContext):
    await state.update_data(wifi_ssid=message.text)
    await message.answer("🔑 Send me the WiFi password (or '-' if open):")
    await state.set_state(QRGeneration.entering_wifi_password)


@router.message(QRGeneration.entering_wifi_password)
async def wifi_password(message: Message, state: FSMContext):
    await state.update_data(wifi_password=message.text)
    await message.answer("🔒 Select encryption type:", reply_markup=wifi_enc_kb())
    await state.set_state(QRGeneration.entering_wifi_encryption)


@router.callback_query(F.data.startswith("wifi_enc_"), StateFilter(QRGeneration.entering_wifi_encryption))
async def wifi_enc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    enc_map = {"wifi_enc_wpa": "WPA", "wifi_enc_wep": "WEP", "wifi_enc_open": "nopass"}
    enc = enc_map.get(callback.data, "WPA")
    data = await state.get_data()
    pwd = data.get("wifi_password", "")
    if enc == "nopass":
        pwd = ""
    qr_data = encode_qr_data("wifi", "", {
        "ssid": data.get("wifi_ssid", ""), "password": pwd, "encryption": enc,
    })
    await state.update_data(qr_data=qr_data, raw_data=f"WiFi: {data.get('wifi_ssid')}")
    data = await state.get_data()
    settings = build_settings(data, force_png=True)
    img = qr_engine.generate(qr_data, settings)
    await callback.message.answer_photo(
        BufferedInputFile(img.getvalue(), "qr_preview.png"),
        caption=fmt_text(data),
        reply_markup=customize_kb(),
    )
    await state.set_state(QRGeneration.customizing)


@router.message(QRGeneration.entering_vcard_name)
async def vcard_name(message: Message, state: FSMContext):
    await state.update_data(vcard_name=message.text)
    await message.answer("📞 Send me the contact phone number:")
    await state.set_state(QRGeneration.entering_vcard_phone)


@router.message(QRGeneration.entering_vcard_phone)
async def vcard_phone(message: Message, state: FSMContext):
    await state.update_data(vcard_phone=message.text)
    await message.answer("📧 Send me the email (or '-' to skip):")
    await state.set_state(QRGeneration.entering_vcard_email)


@router.message(QRGeneration.entering_vcard_email)
async def vcard_email(message: Message, state: FSMContext):
    data = await state.get_data()
    email = message.text if message.text != "-" else ""
    qr_data = encode_qr_data("vcard", "", {
        "name": data.get("vcard_name", ""),
        "phone": data.get("vcard_phone", ""),
        "email": email,
    })
    await state.update_data(qr_data=qr_data, raw_data=f"Contact: {data.get('vcard_name')}")
    data = await state.get_data()
    settings = build_settings(data, force_png=True)
    img = qr_engine.generate(qr_data, settings)
    await message.answer_photo(
        BufferedInputFile(img.getvalue(), "qr_preview.png"),
        caption=fmt_text(data),
        reply_markup=customize_kb(),
    )
    await state.set_state(QRGeneration.customizing)


@router.callback_query(F.data == "cust_fill", QRGeneration.customizing)
async def show_fill(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=fill_color_kb())


@router.callback_query(F.data == "cust_bg", QRGeneration.customizing)
async def show_bg(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=bg_color_kb())


@router.callback_query(F.data == "cust_grad", QRGeneration.customizing)
async def show_grad(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=gradient_kb())


@router.callback_query(F.data == "cust_dot", QRGeneration.customizing)
async def show_dot(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=dot_style_kb())


@router.callback_query(F.data == "cust_icon", QRGeneration.customizing)
async def show_icon(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_reply_markup(reply_markup=icon_kb(bool(data.get("icon_path"))))


@router.callback_query(F.data == "cust_fmt", QRGeneration.customizing)
async def show_fmt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=format_kb())


@router.callback_query(F.data == "cust_back", QRGeneration.customizing)
async def cust_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("fill_"), QRGeneration.customizing)
async def select_fill(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "fill_custom":
        await callback.message.answer("🎨 Send me the fill color as HEX (e.g., #FF5500):")
        await state.update_data(color_target="fill")
        await state.set_state(QRGeneration.entering_custom_color)
        return
    hex_color = callback.data.replace("fill_", "")
    await state.update_data(fill_color=hex_color)
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("bg_"), QRGeneration.customizing)
async def select_bg(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "bg_custom":
        await callback.message.answer("🎨 Send me the background color as HEX (e.g., #FF5500):")
        await state.update_data(color_target="bg")
        await state.set_state(QRGeneration.entering_custom_color)
        return
    if callback.data == "bg_transparent":
        await state.update_data(bg_transparent=True, bg_color="#FFFFFF")
        await show_customize(callback, state)
        return
    if callback.data == "bg_gradient":
        await state.update_data(bg_gradient_enabled=True)
        await show_customize(callback, state)
        return
    hex_color = callback.data.replace("bg_", "")
    await state.update_data(bg_color=hex_color, bg_transparent=False)
    await show_customize(callback, state)


@router.message(QRGeneration.entering_custom_color)
async def custom_color(message: Message, state: FSMContext):
    raw = message.text.strip().lstrip("#")
    if len(raw) not in (3, 6) or not all(c in "0123456789abcdefABCDEF" for c in raw):
        await message.answer("❌ Invalid HEX. Try again (e.g., #FF5500):")
        return
    hex_color = f"#{raw}"
    data = await state.get_data()
    target = data.get("color_target", "fill")
    if target == "fill":
        await state.update_data(fill_color=hex_color)
    else:
        await state.update_data(bg_color=hex_color, bg_transparent=False)
    await state.set_state(QRGeneration.customizing)
    data = await state.get_data()
    settings = build_settings(data, force_png=True)
    qr_data = data.get("qr_data", "")
    if qr_data:
        img = qr_engine.generate(qr_data, settings)
        await message.answer_photo(
            BufferedInputFile(img.getvalue(), "qr_preview.png"),
            caption=fmt_text(data),
            reply_markup=customize_kb(),
        )


@router.callback_query(F.data.startswith("grad_"), QRGeneration.customizing)
async def grad_toggle(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "grad_on":
        await state.update_data(gradient_enabled=True)
    elif callback.data == "grad_off":
        await state.update_data(gradient_enabled=False)
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("grds_"), QRGeneration.customizing)
async def grad_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(gradient_start=callback.data.replace("grds_", ""), gradient_enabled=True)
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("grde_"), QRGeneration.customizing)
async def grad_end(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(gradient_end=callback.data.replace("grde_", ""), gradient_enabled=True)
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("grdd_"), QRGeneration.customizing)
async def grad_dir(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(gradient_direction=callback.data.replace("grdd_", ""), gradient_enabled=True)
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("dot_"), QRGeneration.customizing)
async def select_dot(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(dot_style=callback.data.replace("dot_", ""))
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("fmt_"), QRGeneration.customizing)
async def select_fmt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(format=callback.data.replace("fmt_", ""))
    await show_customize(callback, state)


@router.callback_query(F.data == "icon_upload", QRGeneration.customizing)
async def upload_icon(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("📷 Send me the icon image (PNG/JPG):")
    await state.set_state(QRGeneration.waiting_icon_upload)


@router.callback_query(F.data == "icon_remove", QRGeneration.customizing)
async def remove_icon(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    icon_path = data.get("icon_path")
    if icon_path and os.path.exists(icon_path):
        os.remove(icon_path)
    await state.update_data(icon_path=None)
    await show_customize(callback, state)


@router.message(QRGeneration.waiting_icon_upload, F.photo)
async def process_icon(message: Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    os.makedirs("data/icons", exist_ok=True)
    icon_path = f"data/icons/{message.from_user.id}_{photo.file_unique_id}.png"
    await bot.download(photo, destination=icon_path)
    await state.update_data(icon_path=icon_path)
    data = await state.get_data()
    settings = build_settings(data, force_png=True)
    qr_data = data.get("qr_data", "")
    if qr_data:
        img = qr_engine.generate(qr_data, settings)
        await message.answer_photo(
            BufferedInputFile(img.getvalue(), "qr_preview.png"),
            caption=fmt_text(data),
            reply_markup=customize_kb(),
        )
    await state.set_state(QRGeneration.customizing)


@router.callback_query(F.data == "cust_generate", QRGeneration.customizing)
async def generate_final(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    qr_data = data.get("qr_data", "")
    if not qr_data:
        await callback.message.edit_text("Error. Start over.", reply_markup=main_menu_kb())
        await state.clear()
        return

    fmt = data.get("format", "png")
    settings = build_settings(data)

    try:
        await callback.message.edit_caption(f"{ec('lightning')} Generating...")
    except Exception:
        pass

    img = qr_engine.generate(qr_data, settings)
    is_admin = callback.from_user.id in ADMINS

    if fmt == "svg":
        await callback.message.answer_document(
            BufferedInputFile(img.getvalue(), "qr_code.svg"),
            caption=f"{emoji('check')} Your SVG QR code!",
            reply_markup=main_menu_kb(is_admin),
        )
    else:
        await callback.message.answer_photo(
            BufferedInputFile(img.getvalue(), "qr_code.png"),
            caption=f"{emoji('check')} Your QR code!",
            reply_markup=main_menu_kb(is_admin),
        )

    await db.add_qr_code(callback.from_user.id, data.get("qr_type", "text"), data.get("raw_data", ""), fmt)

    icon_path = data.get("icon_path")
    if icon_path and os.path.exists(icon_path):
        try:
            os.remove(icon_path)
        except OSError:
            pass

    await state.clear()
