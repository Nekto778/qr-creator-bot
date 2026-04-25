import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from ..states import QRGeneration
from ..i18n import t, TYPE_NAMES, TYPE_PROMPTS
from ..emojis import pe, ec
from ..keyboards import (
    qr_type_kb, customize_kb, fill_color_kb, bg_color_kb,
    gradient_kb, dot_style_kb, format_kb, icon_kb,
    wifi_enc_kb, main_menu_kb, subscription_kb, resolution_kb,
)
from ..config import ADMINS
from ..database import db
from ..services.qr_engine import qr_engine, encode_qr_data
from ..services.subscription import check_subscriptions

router = Router()


def build_settings(data: dict, force_png: bool = False, force_resolution: int = 0) -> dict:
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
        "resolution": force_resolution,
    }


def fmt_text(data: dict, lang: str) -> str:
    qr_type_key = data.get("qr_type", "")
    qr_type = TYPE_NAMES.get(qr_type_key, {}).get(lang, "QR")
    fill = data.get("fill_color", "#000000")
    bg = "Transparent" if data.get("bg_transparent") else data.get("bg_color", "#FFFFFF")
    grad = pe("check") if data.get("gradient_enabled") else pe("cross")
    bg_grad = pe("check") if data.get("bg_gradient_enabled") else pe("cross")
    dot = data.get("dot_style", "square").title()
    fmt = data.get("format", "png").upper()
    icon = pe("check") if data.get("icon_path") else pe("cross")
    res = data.get("resolution", 0)
    res_str = f"{res}×{res}" if res else "auto"
    return t("qr_settings", lang,
             qr_type=qr_type, fill=fill, bg=bg,
             grad=grad, bg_grad=bg_grad, dot=dot, fmt=fmt, icon=icon)


async def show_customize(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = await db.get_user_lang(callback.from_user.id)
    qr_data = data.get("qr_data", "")
    if not qr_data:
        await callback.message.edit_text(
            t("error_start_over", lang),
            reply_markup=main_menu_kb(lang, callback.from_user.id in ADMINS),
        )
        await state.clear()
        return
    settings = build_settings(data, force_png=True)
    img = qr_engine.generate(qr_data, settings)
    text = fmt_text(data, lang)
    media = InputMediaPhoto(
        media=BufferedInputFile(img.getvalue(), "qr_preview.png"),
        caption=text,
    )
    try:
        await callback.message.edit_media(media, reply_markup=customize_kb(lang))
    except Exception:
        await callback.message.answer_photo(
            BufferedInputFile(img.getvalue(), "qr_preview.png"),
            caption=text,
            reply_markup=customize_kb(lang),
        )


@router.callback_query(F.data == "gen_start")
async def start_generation(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    channels = await db.get_channels()
    if channels:
        not_subbed = await check_subscriptions(bot, callback.from_user.id, channels)
        if not_subbed:
            await callback.message.edit_text(
                t("sub_required", lang),
                reply_markup=subscription_kb(lang, not_subbed),
            )
            await state.set_state(QRGeneration.choosing_type)
            return
    await callback.message.edit_text(
        t("gen_start", lang),
        reply_markup=qr_type_kb(lang),
    )
    await state.set_state(QRGeneration.choosing_type)


@router.callback_query(F.data == "sub_check")
async def check_sub(callback: CallbackQuery, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(callback.from_user.id)
    channels = await db.get_channels()
    not_subbed = await check_subscriptions(bot, callback.from_user.id, channels) if channels else []
    if not_subbed:
        await callback.answer(t("sub_not_yet", lang), show_alert=True)
        return
    await callback.answer()
    await callback.message.edit_text(
        t("gen_start", lang),
        reply_markup=qr_type_kb(lang),
    )
    await state.set_state(QRGeneration.choosing_type)


@router.callback_query(F.data.startswith("type_"), StateFilter(QRGeneration.choosing_type))
async def select_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    qr_type = callback.data.replace("type_", "")
    await state.update_data(qr_type=qr_type)
    if qr_type == "wifi":
        await callback.message.edit_text(t("wifi_ssid", lang))
        await state.set_state(QRGeneration.entering_wifi_ssid)
    elif qr_type == "vcard":
        await callback.message.edit_text(t("vcard_name", lang))
        await state.set_state(QRGeneration.entering_vcard_name)
    elif qr_type in TYPE_PROMPTS:
        await callback.message.edit_text(t(TYPE_PROMPTS[qr_type], lang))
        await state.set_state(QRGeneration.entering_data)
    else:
        await callback.message.edit_text(t("gen_start", lang), reply_markup=qr_type_kb(lang))


@router.message(QRGeneration.entering_data)
async def process_simple_data(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    data = await state.get_data()
    qr_type = data.get("qr_type", "text")
    qr_data = encode_qr_data(qr_type, message.text)
    await state.update_data(qr_data=qr_data, raw_data=message.text)
    data = await state.get_data()
    settings = build_settings(data, force_png=True)
    img = qr_engine.generate(qr_data, settings)
    await message.answer_photo(
        BufferedInputFile(img.getvalue(), "qr_preview.png"),
        caption=fmt_text(data, lang),
        reply_markup=customize_kb(lang),
    )
    await state.set_state(QRGeneration.customizing)


@router.message(QRGeneration.entering_wifi_ssid)
async def wifi_ssid(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.update_data(wifi_ssid=message.text)
    await message.answer(t("wifi_password", lang))
    await state.set_state(QRGeneration.entering_wifi_password)


@router.message(QRGeneration.entering_wifi_password)
async def wifi_password(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.update_data(wifi_password=message.text)
    await message.answer(t("wifi_enc", lang), reply_markup=wifi_enc_kb(lang))
    await state.set_state(QRGeneration.entering_wifi_encryption)


@router.callback_query(F.data.startswith("wifi_enc_"), StateFilter(QRGeneration.entering_wifi_encryption))
async def wifi_enc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
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
        caption=fmt_text(data, lang),
        reply_markup=customize_kb(lang),
    )
    await state.set_state(QRGeneration.customizing)


@router.message(QRGeneration.entering_vcard_name)
async def vcard_name(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.update_data(vcard_name=message.text)
    await message.answer(t("vcard_phone", lang))
    await state.set_state(QRGeneration.entering_vcard_phone)


@router.message(QRGeneration.entering_vcard_phone)
async def vcard_phone(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.update_data(vcard_phone=message.text)
    await message.answer(t("vcard_email", lang))
    await state.set_state(QRGeneration.entering_vcard_email)


@router.message(QRGeneration.entering_vcard_email)
async def vcard_email(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
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
        caption=fmt_text(data, lang),
        reply_markup=customize_kb(lang),
    )
    await state.set_state(QRGeneration.customizing)


@router.callback_query(F.data == "cust_fill", QRGeneration.customizing)
async def show_fill(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=fill_color_kb(lang))


@router.callback_query(F.data == "cust_bg", QRGeneration.customizing)
async def show_bg(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=bg_color_kb(lang))


@router.callback_query(F.data == "cust_grad", QRGeneration.customizing)
async def show_grad(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=gradient_kb(lang))


@router.callback_query(F.data == "cust_dot", QRGeneration.customizing)
async def show_dot(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=dot_style_kb(lang))


@router.callback_query(F.data == "cust_icon", QRGeneration.customizing)
async def show_icon(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=icon_kb(lang, bool(data.get("icon_path"))))


@router.callback_query(F.data == "cust_fmt", QRGeneration.customizing)
async def show_fmt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=format_kb(lang))


@router.callback_query(F.data == "cust_back", QRGeneration.customizing)
async def cust_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("fill_"), QRGeneration.customizing)
async def select_fill(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    if callback.data == "fill_custom":
        await callback.message.answer(t("enter_hex_fill", lang))
        await state.update_data(color_target="fill")
        await state.set_state(QRGeneration.entering_custom_color)
        return
    hex_color = callback.data.replace("fill_", "")
    await state.update_data(fill_color=hex_color)
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("bg_"), QRGeneration.customizing)
async def select_bg(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    if callback.data == "bg_custom":
        await callback.message.answer(t("enter_hex_bg", lang))
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
    lang = await db.get_user_lang(message.from_user.id)
    raw = message.text.strip().lstrip("#")
    if len(raw) not in (3, 6) or not all(c in "0123456789abcdefABCDEF" for c in raw):
        await message.answer(t("invalid_hex", lang))
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
            caption=fmt_text(data, lang),
            reply_markup=customize_kb(lang),
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
    if callback.data == "fmt_png":
        lang = await db.get_user_lang(callback.from_user.id)
        data = await state.get_data()
        await state.set_state(QRGeneration.choosing_resolution)
        await callback.message.edit_text(
            t("select_resolution", lang),
            reply_markup=resolution_kb(lang),
        )
        return
    await show_customize(callback, state)


@router.callback_query(F.data.startswith("res_"), StateFilter(QRGeneration.choosing_resolution))
async def select_resolution(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    resolution = int(callback.data.replace("res_", ""))
    await state.update_data(resolution=resolution)
    await state.set_state(QRGeneration.customizing)
    await show_customize(callback, state)


@router.callback_query(F.data == "icon_upload", QRGeneration.customizing)
async def upload_icon(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.answer(t("upload_icon_prompt", lang))
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
    lang = await db.get_user_lang(message.from_user.id)
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
            caption=fmt_text(data, lang),
            reply_markup=customize_kb(lang),
        )
    await state.set_state(QRGeneration.customizing)


@router.callback_query(F.data == "cust_generate", QRGeneration.customizing)
async def generate_final(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await db.get_user_lang(callback.from_user.id)
    data = await state.get_data()
    qr_data = data.get("qr_data", "")
    if not qr_data:
        await callback.message.edit_text(
            t("error_start_over", lang),
            reply_markup=main_menu_kb(lang, callback.from_user.id in ADMINS),
        )
        await state.clear()
        return

    fmt = data.get("format", "png")
    resolution = data.get("resolution", 0)

    if fmt == "png" and not resolution:
        await state.set_state(QRGeneration.choosing_resolution)
        try:
            await callback.message.edit_caption(t("select_resolution", lang))
        except Exception:
            pass
        await callback.message.answer(
            t("select_resolution", lang),
            reply_markup=resolution_kb(lang),
        )
        return

    settings = build_settings(data, force_resolution=resolution)

    try:
        await callback.message.edit_caption(t("generating", lang))
    except Exception:
        pass

    img = qr_engine.generate(qr_data, settings)
    is_admin = callback.from_user.id in ADMINS

    if fmt == "svg":
        await callback.message.answer_document(
            BufferedInputFile(img.getvalue(), "qr_code.svg"),
            caption=t("qr_ready_svg", lang),
            reply_markup=main_menu_kb(lang, is_admin),
        )
    else:
        await callback.message.answer_document(
            BufferedInputFile(img.getvalue(), f"qr_{resolution}x{resolution}.png"),
            caption=t("qr_ready_png", lang),
            reply_markup=main_menu_kb(lang, is_admin),
        )

    await db.add_qr_code(callback.from_user.id, data.get("qr_type", "text"), data.get("raw_data", ""), fmt)

    icon_path = data.get("icon_path")
    if icon_path and os.path.exists(icon_path):
        try:
            os.remove(icon_path)
        except OSError:
            pass

    await state.clear()
