from aiogram.utils.keyboard import InlineKeyboardBuilder
from .emojis import ec, EID

COLOR_PRESETS = [
    ("Black", "Чёрный", "#000000"),
    ("Red", "Красный", "#FF0000"),
    ("Orange", "Оранжевый", "#FF8C00"),
    ("Yellow", "Жёлтый", "#FFD700"),
    ("Green", "Зелёный", "#00AA00"),
    ("Blue", "Синий", "#0066FF"),
    ("Purple", "Фиолетовый", "#8B00FF"),
    ("Pink", "Розовый", "#FF69B4"),
    ("White", "Белый", "#FFFFFF"),
    ("Gray", "Серый", "#808080"),
]

DOT_STYLES_LIST = [
    ("Square", "Квадрат", "square"),
    ("Rounded", "Скруглённый", "rounded"),
    ("Circle", "Круглый", "circle"),
    ("Gapped", "С зазором", "gapped"),
]

RESOLUTIONS = [256, 512, 1024, 2048, 4096]

STYLES = {
    "success": "success",
    "danger": "danger",
    "primary": "primary",
}


def language_kb():
    b = InlineKeyboardBuilder()
    b.button(text="English", callback_data="lang_en", icon_custom_emoji_id=EID["flag_gb"])
    b.button(text="Русский", callback_data="lang_ru", icon_custom_emoji_id=EID["flag_ru"])
    b.adjust(2)
    return b.as_markup()


def main_menu_kb(lang: str = "en", is_admin: bool = False):
    b = InlineKeyboardBuilder()
    b.button(text=t("gen_btn", lang), callback_data="gen_start", icon_custom_emoji_id=EID["lightning"], style="primary")
    b.button(text=t("my_qr_btn", lang), callback_data="my_qr", icon_custom_emoji_id=EID["book"])
    b.button(text=t("lang_btn", lang), callback_data="change_lang", icon_custom_emoji_id=EID["globe"])
    if is_admin:
        b.button(text=t("admin_btn", lang), callback_data="admin_panel", icon_custom_emoji_id=EID["gear"], style="primary")
        b.adjust(2, 1, 1)
    else:
        b.adjust(2, 1)
    return b.as_markup()


def qr_type_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    eid_map = {
        "url": "link", "text": "text", "phone": "phone",
        "email": "mail", "wifi": "wifi", "vcard": "person", "sms": "sms",
    }
    for tp in ["url", "text", "phone", "email", "wifi", "vcard", "sms"]:
        b.button(text=t(f"type_{tp}", lang), callback_data=f"type_{tp}", icon_custom_emoji_id=EID[eid_map[tp]])
    b.button(text=t("back", lang), callback_data="back_main", icon_custom_emoji_id=EID["back"])
    b.adjust(2, 2, 2, 1, 1)
    return b.as_markup()


def customize_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("fill_color", lang), callback_data="cust_fill", icon_custom_emoji_id=EID["palette"])
    b.button(text=t("bg_color", lang), callback_data="cust_bg", icon_custom_emoji_id=EID["image"])
    b.button(text=t("gradient", lang), callback_data="cust_grad", icon_custom_emoji_id=EID["rainbow"])
    b.button(text=t("dot_style", lang), callback_data="cust_dot", icon_custom_emoji_id=EID["dot_black"])
    b.button(text=t("center_icon", lang), callback_data="cust_icon", icon_custom_emoji_id=EID["camera"])
    b.button(text=t("format", lang), callback_data="cust_fmt", icon_custom_emoji_id=EID["paperclip"])
    b.button(text=t("generate", lang), callback_data="cust_generate", icon_custom_emoji_id=EID["check"], style="success")
    b.button(text=t("cancel", lang), callback_data="back_main", icon_custom_emoji_id=EID["cross"], style="danger")
    b.adjust(3, 3, 1, 1)
    return b.as_markup()


def fill_color_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    eid_map = ["dot_black", "red", "orange", "yellow", "green", "blue", "purple", "pink", "dot_white", "gray"]
    for i, (en_name, ru_name, hex_val) in enumerate(COLOR_PRESETS):
        label = ru_name if lang == "ru" else en_name
        b.button(text=label, callback_data=f"fill_{hex_val}", icon_custom_emoji_id=EID[eid_map[i]])
    b.button(text=t("custom_hex", lang), callback_data="fill_custom", icon_custom_emoji_id=EID["palette"])
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    b.adjust(5, 5, 2)
    return b.as_markup()


def bg_color_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    eid_map = ["dot_black", "red", "orange", "yellow", "green", "blue", "purple", "pink", "dot_white", "gray"]
    for i, (en_name, ru_name, hex_val) in enumerate(COLOR_PRESETS):
        label = ru_name if lang == "ru" else en_name
        b.button(text=label, callback_data=f"bg_{hex_val}", icon_custom_emoji_id=EID[eid_map[i]])
    b.button(text=t("custom_hex", lang), callback_data="bg_custom", icon_custom_emoji_id=EID["palette"])
    b.button(text=t("transparent", lang), callback_data="bg_transparent", icon_custom_emoji_id=EID["monkey"])
    b.button(text=t("bg_gradient", lang), callback_data="bg_gradient", icon_custom_emoji_id=EID["rainbow"])
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    b.adjust(5, 5, 2, 1, 1)
    return b.as_markup()


def gradient_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("enable", lang), callback_data="grad_on", icon_custom_emoji_id=EID["check"], style="success")
    b.button(text=t("disable", lang), callback_data="grad_off", icon_custom_emoji_id=EID["cross"], style="danger")
    eid_map = ["dot_black", "red", "orange", "yellow", "green", "blue"]
    for i, (en_name, ru_name, hex_val) in enumerate(COLOR_PRESETS[:6]):
        label = (ru_name if lang == "ru" else en_name).split(" ", 1)[1] if " " in (ru_name if lang == "ru" else en_name) else (ru_name if lang == "ru" else en_name)
        b.button(text=f"▶ {label}", callback_data=f"grds_{hex_val}", icon_custom_emoji_id=EID[eid_map[i]])
    for i, (en_name, ru_name, hex_val) in enumerate(COLOR_PRESETS[:6]):
        label = (ru_name if lang == "ru" else en_name).split(" ", 1)[1] if " " in (ru_name if lang == "ru" else en_name) else (ru_name if lang == "ru" else en_name)
        b.button(text=f"◀ {label}", callback_data=f"grde_{hex_val}", icon_custom_emoji_id=EID[eid_map[i]])
    if lang == "ru":
        dirs = [("Гориз", "horizontal"), ("Верт", "vertical"), ("Диаг", "diagonal"), ("Рад", "radial")]
    else:
        dirs = [("Horiz", "horizontal"), ("Vert", "vertical"), ("Diag", "diagonal"), ("Radial", "radial")]
    for dn, dv in dirs:
        b.button(text=dn, callback_data=f"grdd_{dv}")
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    b.adjust(2, 3, 3, 4, 1)
    return b.as_markup()


def dot_style_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    eid_map = ["dot_black", "dot_round", "dot_circle", "dot_white"]
    for i, (en_name, ru_name, val) in enumerate(DOT_STYLES_LIST):
        label = ru_name if lang == "ru" else en_name
        b.button(text=label, callback_data=f"dot_{val}", icon_custom_emoji_id=EID[eid_map[i]])
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    b.adjust(2, 2, 1)
    return b.as_markup()


def format_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("png_raster", lang), callback_data="fmt_png", icon_custom_emoji_id=EID["image"], style="primary")
    b.button(text=t("svg_vector", lang), callback_data="fmt_svg", icon_custom_emoji_id=EID["paperclip"], style="primary")
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    b.adjust(2, 1)
    return b.as_markup()


def resolution_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    for res in RESOLUTIONS:
        b.button(text=f"{res}×{res}", callback_data=f"res_{res}", icon_custom_emoji_id=EID["resolution"])
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    b.adjust(3, 2, 1)
    return b.as_markup()


def icon_kb(lang: str = "en", has_icon: bool = False):
    b = InlineKeyboardBuilder()
    b.button(text=t("upload_icon", lang), callback_data="icon_upload", icon_custom_emoji_id=EID["camera"])
    if has_icon:
        b.button(text=t("remove_icon", lang), callback_data="icon_remove", icon_custom_emoji_id=EID["cross"], style="danger")
    b.button(text=t("back", lang), callback_data="cust_back", icon_custom_emoji_id=EID["back"])
    if has_icon:
        b.adjust(1, 2)
    else:
        b.adjust(1, 1)
    return b.as_markup()


def wifi_enc_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text="WPA/WPA2", callback_data="wifi_enc_wpa", icon_custom_emoji_id=EID["lock"])
    b.button(text="WEP", callback_data="wifi_enc_wep", icon_custom_emoji_id=EID["key"])
    if lang == "ru":
        b.button(text="Открытая", callback_data="wifi_enc_open", icon_custom_emoji_id=EID["unlock"])
    else:
        b.button(text="Open", callback_data="wifi_enc_open", icon_custom_emoji_id=EID["unlock"])
    b.adjust(3)
    return b.as_markup()


def admin_panel_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("admin_stats", lang), callback_data="admin_stats", icon_custom_emoji_id=EID["chart"], style="primary")
    b.button(text=t("admin_broadcast", lang), callback_data="admin_broadcast", icon_custom_emoji_id=EID["loudspeaker"], style="primary")
    b.button(text=t("admin_channels", lang), callback_data="admin_channels", icon_custom_emoji_id=EID["people"])
    b.button(text=t("back", lang), callback_data="back_main", icon_custom_emoji_id=EID["back"])
    b.adjust(2, 1, 1)
    return b.as_markup()


def admin_channels_kb(lang: str = "en", channels: list = None):
    channels = channels or []
    b = InlineKeyboardBuilder()
    for ch_id, ch_title, invite_link in channels:
        b.button(text=ch_title, callback_data=f"rmch_{ch_id}", icon_custom_emoji_id=EID["cross"], style="danger")
    b.button(text=t("ch_add", lang), callback_data="admin_add_channel", icon_custom_emoji_id=EID["plus"], style="success")
    b.button(text=t("back", lang), callback_data="admin_panel", icon_custom_emoji_id=EID["back"])
    if channels:
        b.adjust(1, 2)
    else:
        b.adjust(2)
    return b.as_markup()


def broadcast_confirm_kb(lang: str = "en"):
    b = InlineKeyboardBuilder()
    b.button(text=t("bc_confirm", lang), callback_data="bc_confirm", icon_custom_emoji_id=EID["check"], style="success")
    b.button(text=t("bc_cancel_btn", lang), callback_data="bc_cancel", icon_custom_emoji_id=EID["cross"], style="danger")
    b.adjust(2)
    return b.as_markup()


def subscription_kb(lang: str = "en", channels: list = None):
    channels = channels or []
    b = InlineKeyboardBuilder()
    for ch_id, ch_title, invite_link in channels:
        url = invite_link if invite_link else f"https://t.me/{ch_title}"
        b.button(text=ch_title, url=url, icon_custom_emoji_id=EID["loudspeaker"])
    b.button(text=t("sub_check", lang), callback_data="sub_check", icon_custom_emoji_id=EID["check"], style="success")
    b.adjust(1)
    return b.as_markup()


from .i18n import t
