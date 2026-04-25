from aiogram.utils.keyboard import InlineKeyboardBuilder
from .i18n import t

COLOR_PRESETS = [
    ("⬛ Black|#000000", "⬛ Чёрный|#000000"),
    ("🟥 Red|#FF0000", "🟥 Красный|#FF0000"),
    ("🟧 Orange|#FF8C00", "🟧 Оранжевый|#FF8C00"),
    ("🟨 Yellow|#FFD700", "🟨 Жёлтый|#FFD700"),
    ("🟩 Green|#00AA00", "🟩 Зелёный|#00AA00"),
    ("🟦 Blue|#0066FF", "🟦 Синий|#0066FF"),
    ("🟪 Purple|#8B00FF", "🟪 Фиолетовый|#8B00FF"),
    ("🩷 Pink|#FF69B4", "🩷 Розовый|#FF69B4"),
    ("⬜ White|#FFFFFF", "⬜ Белый|#FFFFFF"),
    ("🩶 Gray|#808080", "🩶 Серый|#808080"),
]

DOT_STYLES = [
    ("⬛ Square|square", "⬛ Квадрат|square"),
    ("🔲 Rounded|rounded", "🔲 Скруглённый|rounded"),
    ("⚫ Circle|circle", "⚫ Круглый|circle"),
    ("⬜ Gapped|gapped", "⬜ С зазором|gapped"),
]


def _cp(lang, idx):
    pair = COLOR_PRESETS[idx]
    return pair[0] if lang == "en" else pair[1]


def _ds(lang, idx):
    pair = DOT_STYLES[idx]
    return pair[0] if lang == "en" else pair[1]


def language_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🇬🇧 English", callback_data="lang_en")
    b.button(text="🇷🇺 Русский", callback_data="lang_ru")
    b.adjust(2)
    return b.as_markup()


def main_menu_kb(lang: str = "en", is_admin: bool = False):
    b = InlineKeyboardBuilder()
    b.button(text=t("gen_btn", lang), callback_data="gen_start")
    b.button(text=t("my_qr_btn", lang), callback_data="my_qr")
    b.button(text=t("lang_btn", lang), callback_data="change_lang")
    if is_admin:
        b.button(text=t("admin_btn", lang), callback_data="admin_panel")
        b.adjust(2, 1, 1)
    else:
        b.adjust(2, 1)
    return b.as_markup()


def qr_type_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    types = ["url", "text", "phone", "email", "wifi", "vcard", "sms"]
    for tp in types:
        b.button(text=t(f"type_{tp}", lang), callback_data=f"type_{tp}")
    b.button(text=t("back", lang), callback_data="back_main")
    b.adjust(2, 2, 2, 1, 1)
    return b.as_markup()


def customize_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("fill_color", lang), callback_data="cust_fill")
    b.button(text=t("bg_color", lang), callback_data="cust_bg")
    b.button(text=t("gradient", lang), callback_data="cust_grad")
    b.button(text=t("dot_style", lang), callback_data="cust_dot")
    b.button(text=t("center_icon", lang), callback_data="cust_icon")
    b.button(text=t("format", lang), callback_data="cust_fmt")
    b.button(text=t("generate", lang), callback_data="cust_generate")
    b.button(text=t("cancel", lang), callback_data="back_main")
    b.adjust(3, 3, 1, 1)
    return b.as_markup()


def fill_color_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    for i in range(len(COLOR_PRESETS)):
        parts = _cp(lang, i).split("|")
        b.button(text=parts[0], callback_data=f"fill_{parts[1]}")
    b.button(text=t("custom_hex", lang), callback_data="fill_custom")
    b.button(text=t("back", lang), callback_data="cust_back")
    b.adjust(5, 5, 2)
    return b.as_markup()


def bg_color_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    for i in range(len(COLOR_PRESETS)):
        parts = _cp(lang, i).split("|")
        b.button(text=parts[0], callback_data=f"bg_{parts[1]}")
    b.button(text=t("custom_hex", lang), callback_data="bg_custom")
    b.button(text=t("transparent", lang), callback_data="bg_transparent")
    b.button(text=t("bg_gradient", lang), callback_data="bg_gradient")
    b.button(text=t("back", lang), callback_data="cust_back")
    b.adjust(5, 5, 2, 1, 1)
    return b.as_markup()


def gradient_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("enable", lang), callback_data="grad_on")
    b.button(text=t("disable", lang), callback_data="grad_off")
    for i in range(6):
        parts = _cp(lang, i).split("|")
        label = parts[0].split(" ", 1)[1] if " " in parts[0] else parts[0]
        b.button(text=f"▶ {label}", callback_data=f"grds_{parts[1]}")
    for i in range(6):
        parts = _cp(lang, i).split("|")
        label = parts[0].split(" ", 1)[1] if " " in parts[0] else parts[0]
        b.button(text=f"◀ {label}", callback_data=f"grde_{parts[1]}")
    dir_names = {
        "en": [("➡️ Horiz", "horizontal"), ("⬇️ Vert", "vertical"), ("↗️ Diag", "diagonal"), ("⭕ Radial", "radial")],
        "ru": [("➡️ Гориз", "horizontal"), ("⬇️ Верт", "vertical"), ("↗️ Диаг", "diagonal"), ("⭕ Рад", "radial")],
    }
    for dn, dv in dir_names.get(lang, dir_names["en"]):
        b.button(text=dn, callback_data=f"grdd_{dv}")
    b.button(text=t("back", lang), callback_data="cust_back")
    b.adjust(2, 3, 3, 4, 1)
    return b.as_markup()


def dot_style_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    for i in range(len(DOT_STYLES)):
        parts = _ds(lang, i).split("|")
        b.button(text=parts[0], callback_data=f"dot_{parts[1]}")
    b.button(text=t("back", lang), callback_data="cust_back")
    b.adjust(2, 2, 1)
    return b.as_markup()


def format_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("png_raster", lang), callback_data="fmt_png")
    b.button(text=t("svg_vector", lang), callback_data="fmt_svg")
    b.button(text=t("back", lang), callback_data="cust_back")
    b.adjust(2, 1)
    return b.as_markup()


def icon_kb(lang: str = "en", has_icon: bool = False):
    b = InlineKeyboardBuilder()
    b.button(text=t("upload_icon", lang), callback_data="icon_upload")
    if has_icon:
        b.button(text=t("remove_icon", lang), callback_data="icon_remove")
    b.button(text=t("back", lang), callback_data="cust_back")
    if has_icon:
        b.adjust(1, 2)
    else:
        b.adjust(1, 1)
    return b.as_markup()


def wifi_enc_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    if lang == "ru":
        b.button(text="🔒 WPA/WPA2", callback_data="wifi_enc_wpa")
        b.button(text="🔑 WEP", callback_data="wifi_enc_wep")
        b.button(text="🔓 Открытая", callback_data="wifi_enc_open")
    else:
        b.button(text="🔒 WPA/WPA2", callback_data="wifi_enc_wpa")
        b.button(text="🔑 WEP", callback_data="wifi_enc_wep")
        b.button(text="🔓 Open", callback_data="wifi_enc_open")
    b.adjust(3)
    return b.as_markup()


def admin_panel_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("admin_stats", lang), callback_data="admin_stats")
    b.button(text=t("admin_broadcast", lang), callback_data="admin_broadcast")
    b.button(text=t("admin_channels", lang), callback_data="admin_channels")
    b.button(text=t("back", lang), callback_data="back_main")
    b.adjust(2, 1, 1)
    return b.as_markup()


def admin_channels_kb(lang: str = "en", channels: list = None):
    channels = channels or []
    b = InlineKeyboardBuilder()
    for ch_id, ch_title, invite_link in channels:
        label = f"❌ {ch_title}"
        b.button(text=label, callback_data=f"rmch_{ch_id}")
    b.button(text=t("ch_add", lang), callback_data="admin_add_channel")
    b.button(text=t("back", lang), callback_data="admin_panel")
    if channels:
        b.adjust(1, 2)
    else:
        b.adjust(2)
    return b.as_markup()


def broadcast_confirm_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("bc_confirm", lang), callback_data="bc_confirm")
    b.button(text=t("bc_cancel_btn", lang), callback_data="bc_cancel")
    b.adjust(2)
    return b.as_markup()


def subscription_kb(lang: str = "en", channels: list = None):
    channels = channels or []
    b = InlineKeyboardBuilder()
    for ch_id, ch_title, invite_link in channels:
        url = invite_link if invite_link else f"https://t.me/{ch_title}"
        b.button(text=f"📢 {ch_title}", url=url)
    b.button(text=t("sub_check", lang), callback_data="sub_check")
    b.adjust(1)
    return b.as_markup()
