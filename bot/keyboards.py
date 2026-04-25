from aiogram.utils.keyboard import InlineKeyboardBuilder
from . import emojis as em

COLOR_PRESETS = [
    ("⬛ Black", "#000000"),
    ("🟥 Red", "#FF0000"),
    ("🟧 Orange", "#FF8C00"),
    ("🟨 Yellow", "#FFD700"),
    ("🟩 Green", "#00AA00"),
    ("🟦 Blue", "#0066FF"),
    ("🟪 Purple", "#8B00FF"),
    ("🩷 Pink", "#FF69B4"),
    ("⬜ White", "#FFFFFF"),
    ("🩶 Gray", "#808080"),
]

DOT_STYLES = [
    ("⬛ Square", "square"),
    ("🔲 Rounded", "rounded"),
    ("⚫ Circle", "circle"),
    ("⬜ Gapped", "gapped"),
]


def main_menu_kb(is_admin: bool = False):
    b = InlineKeyboardBuilder()
    b.button(text=f"{ec('lightning')} Generate QR", callback_data="gen_start")
    b.button(text=f"{ec('book')} My QR Codes", callback_data="my_qr")
    if is_admin:
        b.button(text=f"{ec('gear')} Admin Panel", callback_data="admin_panel")
        b.adjust(2, 1)
    else:
        b.adjust(1, 1)
    return b.as_markup()


def qr_type_kb():
    b = InlineKeyboardBuilder()
    items = [
        ("🔗 Link", "type_url"),
        ("📝 Text", "type_text"),
        ("📞 Phone", "type_phone"),
        ("📧 Email", "type_email"),
        ("📶 WiFi", "type_wifi"),
        ("👤 Contact", "type_vcard"),
        ("💬 SMS", "type_sms"),
        (f"{ec('back')} Back", "back_main"),
    ]
    for text, data in items:
        b.button(text=text, callback_data=data)
    b.adjust(2, 2, 2, 1, 1)
    return b.as_markup()


def customize_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🎨 Fill Color", callback_data="cust_fill")
    b.button(text="🖼 Background", callback_data="cust_bg")
    b.button(text="🌈 Gradient", callback_data="cust_grad")
    b.button(text="⬛ Dot Style", callback_data="cust_dot")
    b.button(text="🖼 Center Icon", callback_data="cust_icon")
    b.button(text="📄 Format", callback_data="cust_fmt")
    b.button(text=f"{ec('check')} Generate!", callback_data="cust_generate")
    b.button(text=f"{ec('back')} Cancel", callback_data="back_main")
    b.adjust(3, 3, 1, 1)
    return b.as_markup()


def fill_color_kb():
    b = InlineKeyboardBuilder()
    for name, hex_val in COLOR_PRESETS:
        b.button(text=name, callback_data=f"fill_{hex_val}")
    b.button(text="🎨 Custom HEX", callback_data="fill_custom")
    b.button(text=f"{ec('back')} Back", callback_data="cust_back")
    b.adjust(5, 5, 2)
    return b.as_markup()


def bg_color_kb():
    b = InlineKeyboardBuilder()
    for name, hex_val in COLOR_PRESETS:
        b.button(text=name, callback_data=f"bg_{hex_val}")
    b.button(text="🎨 Custom HEX", callback_data="bg_custom")
    b.button(text="🙈 Transparent", callback_data="bg_transparent")
    b.button(text="🌈 BG Gradient", callback_data="bg_gradient")
    b.button(text=f"{ec('back')} Back", callback_data="cust_back")
    b.adjust(5, 5, 2, 1, 1)
    return b.as_markup()


def gradient_kb():
    b = InlineKeyboardBuilder()
    b.button(text="✅ Enable", callback_data="grad_on")
    b.button(text="❌ Disable", callback_data="grad_off")
    for name, hex_val in COLOR_PRESETS[:6]:
        label = name.split(" ", 1)[1]
        b.button(text=f"Start {label}", callback_data=f"grds_{hex_val}")
    for name, hex_val in COLOR_PRESETS[:6]:
        label = name.split(" ", 1)[1]
        b.button(text=f"End {label}", callback_data=f"grde_{hex_val}")
    for dname, dval in [("➡️ Horiz", "horizontal"), ("⬇️ Vert", "vertical"), ("↗️ Diag", "diagonal"), ("⭕ Radial", "radial")]:
        b.button(text=dname, callback_data=f"grdd_{dval}")
    b.button(text=f"{ec('back')} Back", callback_data="cust_back")
    b.adjust(2, 3, 3, 4, 1)
    return b.as_markup()


def dot_style_kb():
    b = InlineKeyboardBuilder()
    for name, val in DOT_STYLES:
        b.button(text=name, callback_data=f"dot_{val}")
    b.button(text=f"{ec('back')} Back", callback_data="cust_back")
    b.adjust(2, 2, 1)
    return b.as_markup()


def format_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🖼 PNG (Raster)", callback_data="fmt_png")
    b.button(text="📐 SVG (Vector)", callback_data="fmt_svg")
    b.button(text=f"{ec('back')} Back", callback_data="cust_back")
    b.adjust(2, 1)
    return b.as_markup()


def icon_kb(has_icon: bool = False):
    b = InlineKeyboardBuilder()
    b.button(text="📷 Upload Icon", callback_data="icon_upload")
    if has_icon:
        b.button(text="❌ Remove Icon", callback_data="icon_remove")
    b.button(text=f"{ec('back')} Back", callback_data="cust_back")
    b.adjust(1, 1 if has_icon else 0, 1)
    return b.as_markup()


def wifi_enc_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🔒 WPA/WPA2", callback_data="wifi_enc_wpa")
    b.button(text="🔑 WEP", callback_data="wifi_enc_wep")
    b.button(text="🔓 Open", callback_data="wifi_enc_open")
    b.adjust(3)
    return b.as_markup()


def admin_panel_kb():
    b = InlineKeyboardBuilder()
    b.button(text=f"{ec('chart')} Statistics", callback_data="admin_stats")
    b.button(text=f"{ec('loudspeaker')} Broadcast", callback_data="admin_broadcast")
    b.button(text=f"{ec('people')} Channels", callback_data="admin_channels")
    b.button(text=f"{ec('back')} Back", callback_data="back_main")
    b.adjust(2, 1, 1)
    return b.as_markup()


def admin_channels_kb(channels: list):
    b = InlineKeyboardBuilder()
    for ch_id, ch_title, invite_link in channels:
        b.button(text=f"❌ {ch_title}", callback_data=f"rmch_{ch_id}")
    b.button(text="➕ Add Channel", callback_data="admin_add_channel")
    b.button(text=f"{ec('back')} Back", callback_data="admin_panel")
    b.adjust(1, 2)
    return b.as_markup()


def broadcast_confirm_kb():
    b = InlineKeyboardBuilder()
    b.button(text=f"{ec('check')} Confirm Send", callback_data="bc_confirm")
    b.button(text=f"{ec('cross')} Cancel", callback_data="bc_cancel")
    b.adjust(2)
    return b.as_markup()


def subscription_kb(channels: list):
    b = InlineKeyboardBuilder()
    for ch_id, ch_title, invite_link in channels:
        url = invite_link if invite_link else f"https://t.me/{ch_title}"
        b.button(text=f"📢 {ch_title}", url=url)
    b.button(text=f"{ec('check')} I've subscribed!", callback_data="sub_check")
    b.adjust(1)
    return b.as_markup()


def ec(name: str) -> str:
    return em.EMOJI_IDS[name][0]
