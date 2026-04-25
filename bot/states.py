from aiogram.fsm.state import State, StatesGroup


class QRGeneration(StatesGroup):
    choosing_type = State()
    entering_data = State()
    entering_wifi_ssid = State()
    entering_wifi_password = State()
    entering_wifi_encryption = State()
    entering_vcard_name = State()
    entering_vcard_phone = State()
    entering_vcard_email = State()
    customizing = State()
    choosing_fill_color = State()
    choosing_bg_color = State()
    entering_custom_color = State()
    waiting_icon_upload = State()


class AdminBroadcast(StatesGroup):
    entering_text = State()
    confirming = State()


class AdminChannels(StatesGroup):
    entering_channel = State()
