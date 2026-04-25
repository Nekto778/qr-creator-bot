from .emojis import pe, ec

TEXTS = {
    "welcome": {
        "en": f"{pe('wave')} Welcome to <b>QR Generator Bot</b>!\n\n"
             f"Create custom QR codes with advanced design:\n"
             f"• {pe('link')} Multiple types (URL, text, WiFi, etc.)\n"
             f"• {pe('palette')} Custom colors & gradients\n"
             f"• {pe('dot_round')} Rounded/dotted dot styles\n"
             f"• {pe('image')} Center icon support\n"
             f"• {pe('paperclip')} PNG & SVG export\n"
             f"• {pe('lightning')} Inline mode in any chat\n\n"
             f"Choose an option:",
        "ru": f"{pe('wave')} Добро пожаловать в <b>QR Генератор Бот</b>!\n\n"
             f"Создайте кастомные QR-коды с продвинутым дизайном:\n"
             f"• {pe('link')} Множество типов (URL, текст, WiFi и др.)\n"
             f"• {pe('palette')} Цвета и градиенты\n"
             f"• {pe('dot_round')} Скруглённые/круглые точки\n"
             f"• {pe('image')} Иконка в центре QR-кода\n"
             f"• {pe('paperclip')} Экспорт PNG и SVG\n"
             f"• {pe('lightning')} Инлайн-режим в любом чате\n\n"
             f"Выберите действие:",
    },
    "choose_lang": {
        "en": f"{pe('globe')} Choose your language:",
        "ru": f"{pe('globe')} Выберите язык:",
    },
    "lang_set": {
        "en": f"{pe('check')} Language set to English!",
        "ru": f"{pe('check')} Язык установлен: Русский!",
    },
    "main_menu": {
        "en": f"{pe('wave')} Main Menu",
        "ru": f"{pe('wave')} Главное меню",
    },
    "gen_start": {
        "en": f"{pe('lightning')} Select QR code type:",
        "ru": f"{pe('lightning')} Выберите тип QR-кода:",
    },
    "my_qr": {
        "en": f"{pe('book')} Your QR Codes\n\n{pe('chart')} Total generated: <b>{{count}}</b>\n\nGenerate a new one from the main menu!",
        "ru": f"{pe('book')} Ваши QR-коды\n\n{pe('chart')} Всего сгенерировано: <b>{{count}}</b>\n\nСоздайте новый из главного меню!",
    },
    "type_url": {"en": f"{pe('link')} Link", "ru": f"{pe('link')} Ссылка"},
    "type_text": {"en": f"{pe('text')} Text", "ru": f"{pe('text')} Текст"},
    "type_phone": {"en": f"{pe('phone')} Phone", "ru": f"{pe('phone')} Телефон"},
    "type_email": {"en": f"{pe('mail')} Email", "ru": f"{pe('mail')} Почта"},
    "type_wifi": {"en": f"{pe('wifi')} WiFi", "ru": f"{pe('wifi')} WiFi"},
    "type_vcard": {"en": f"{pe('person')} Contact", "ru": f"{pe('person')} Контакт"},
    "type_sms": {"en": f"{pe('sms')} SMS", "ru": f"{pe('sms')} SMS"},
    "back": {"en": f"{pe('back')} Back", "ru": f"{pe('back')} Назад"},
    "prompt_url": {
        "en": f"{pe('link')} Send me a URL (e.g., https://example.com):",
        "ru": f"{pe('link')} Пришлите ссылку (напр., https://example.com):",
    },
    "prompt_text": {
        "en": f"{pe('text')} Send me the text to encode:",
        "ru": f"{pe('text')} Пришлите текст для кодирования:",
    },
    "prompt_phone": {
        "en": f"{pe('phone')} Send me a phone number (e.g., +1234567890):",
        "ru": f"{pe('phone')} Пришлите номер телефона (напр., +79001234567):",
    },
    "prompt_email": {
        "en": f"{pe('mail')} Send me an email address:",
        "ru": f"{pe('mail')} Пришлите адрес электронной почты:",
    },
    "prompt_sms": {
        "en": f"{pe('sms')} Send phone:message (e.g., +1234567890:Hello):",
        "ru": f"{pe('sms')} Пришлите телефон:сообщение (напр., +79001234567:Привет):",
    },
    "wifi_ssid": {
        "en": f"{pe('wifi')} Send me the WiFi network name (SSID):",
        "ru": f"{pe('wifi')} Пришлите название сети WiFi (SSID):",
    },
    "wifi_password": {
        "en": f"{pe('key')} Send me the WiFi password (or '-' if open):",
        "ru": f"{pe('key')} Пришлите пароль WiFi (или '-' если открытая):",
    },
    "wifi_enc": {
        "en": f"{pe('lock')} Select encryption type:",
        "ru": f"{pe('lock')} Выберите тип шифрования:",
    },
    "vcard_name": {
        "en": f"{pe('person')} Send me the contact name:",
        "ru": f"{pe('person')} Пришлите имя контакта:",
    },
    "vcard_phone": {
        "en": f"{pe('phone')} Send me the contact phone number:",
        "ru": f"{pe('phone')} Пришлите номер телефона контакта:",
    },
    "vcard_email": {
        "en": f"{pe('mail')} Send me the email (or '-' to skip):",
        "ru": f"{pe('mail')} Пришлите email (или '-' чтобы пропустить):",
    },
    "qr_settings": {
        "en": f"{pe('palette')} {pe('gear')} QR Settings\n\n"
              f"Type: {{qr_type}}\n"
              f"Fill: <code>{{fill}}</code>\n"
              f"BG: <code>{{bg}}</code>\n"
              f"Gradient: {{grad}}  |  BG Grad: {{bg_grad}}\n"
              f"Dot: {{dot}}  |  Format: {{fmt}}\n"
              f"Icon: {{icon}}\n\n"
              f"{pe('lightning')} Customize or generate!",
        "ru": f"{pe('palette')} {pe('gear')} Настройки QR\n\n"
              f"Тип: {{qr_type}}\n"
              f"Цвет: <code>{{fill}}</code>\n"
              f"Фон: <code>{{bg}}</code>\n"
              f"Градиент: {{grad}}  |  Градиент фона: {{bg_grad}}\n"
              f"Точки: {{dot}}  |  Формат: {{fmt}}\n"
              f"Иконка: {{icon}}\n\n"
              f"{pe('lightning')} Настройте или генерируйте!",
    },
    "gen_btn": {"en": f"{pe('lightning')} Generate QR", "ru": f"{pe('lightning')} Генерировать QR"},
    "my_qr_btn": {"en": f"{pe('book')} My QR Codes", "ru": f"{pe('book')} Мои QR-коды"},
    "admin_btn": {"en": f"{pe('gear')} Admin Panel", "ru": f"{pe('gear')} Админка"},
    "lang_btn": {"en": f"{pe('globe')} Language", "ru": f"{pe('globe')} Язык"},
    "fill_color": {"en": f"{pe('palette')} Fill Color", "ru": f"{pe('palette')} Цвет заливки"},
    "bg_color": {"en": f"{pe('image')} Background", "ru": f"{pe('image')} Фон"},
    "gradient": {"en": f"{pe('rainbow')} Gradient", "ru": f"{pe('rainbow')} Градиент"},
    "dot_style": {"en": f"{pe('dot_black')} Dot Style", "ru": f"{pe('dot_black')} Стиль точек"},
    "center_icon": {"en": f"{pe('image')} Center Icon", "ru": f"{pe('image')} Иконка в центре"},
    "format": {"en": f"{pe('paperclip')} Format", "ru": f"{pe('paperclip')} Формат"},
    "resolution": {"en": f"{pe('image')} Resolution", "ru": f"{pe('image')} Разрешение"},
    "generate": {"en": f"{pe('check')} Generate!", "ru": f"{pe('check')} Генерировать!"},
    "cancel": {"en": f"{pe('cross')} Cancel", "ru": f"{pe('cross')} Отмена"},
    "custom_hex": {"en": f"{pe('palette')} Custom HEX", "ru": f"{pe('palette')} Свой HEX"},
    "transparent": {"en": f"{pe('monkey')} Transparent", "ru": f"{pe('monkey')} Прозрачный"},
    "bg_gradient": {"en": f"{pe('rainbow')} BG Gradient", "ru": f"{pe('rainbow')} Градиент фона"},
    "enable": {"en": f"{pe('check')} Enable", "ru": f"{pe('check')} Включить"},
    "disable": {"en": f"{pe('cross')} Disable", "ru": f"{pe('cross')} Выключить"},
    "png_raster": {"en": f"{pe('image')} PNG (Raster)", "ru": f"{pe('image')} PNG (Растр)"},
    "svg_vector": {"en": f"{pe('paperclip')} SVG (Vector)", "ru": f"{pe('paperclip')} SVG (Вектор)"},
    "upload_icon": {"en": f"{pe('camera')} Upload Icon", "ru": f"{pe('camera')} Загрузить иконку"},
    "remove_icon": {"en": f"{pe('cross')} Remove Icon", "ru": f"{pe('cross')} Убрать иконку"},
    "enter_hex_fill": {
        "en": f"{pe('palette')} Send me the fill color as HEX (e.g., #FF5500):",
        "ru": f"{pe('palette')} Пришлите цвет заливки в HEX (напр., #FF5500):",
    },
    "enter_hex_bg": {
        "en": f"{pe('palette')} Send me the background color as HEX (e.g., #FF5500):",
        "ru": f"{pe('palette')} Пришлите цвет фона в HEX (напр., #FF5500):",
    },
    "invalid_hex": {
        "en": f"{pe('cross')} Invalid HEX. Try again (e.g., #FF5500):",
        "ru": f"{pe('cross')} Неверный HEX. Попробуйте снова (напр., #FF5500):",
    },
    "upload_icon_prompt": {
        "en": f"{pe('camera')} Send me the icon image (PNG/JPG):",
        "ru": f"{pe('camera')} Пришлите изображение иконки (PNG/JPG):",
    },
    "generating": {"en": f"{pe('lightning')} Generating...", "ru": f"{pe('lightning')} Генерация..."},
    "qr_ready_png": {"en": f"{pe('check')} Your QR code!", "ru": f"{pe('check')} Ваш QR-код!"},
    "qr_ready_svg": {"en": f"{pe('check')} Your SVG QR code!", "ru": f"{pe('check')} Ваш SVG QR-код!"},
    "error_start_over": {"en": "Error. Start over.", "ru": "Ошибка. Начните заново."},
    "sub_required": {
        "en": f"{pe('shield')} Subscribe to all channels first:",
        "ru": f"{pe('shield')} Подпишитесь на все каналы:",
    },
    "sub_not_yet": {
        "en": "You haven't subscribed yet!",
        "ru": "Вы ещё не подписались!",
    },
    "sub_check": {
        "en": f"{pe('check')} I've subscribed!",
        "ru": f"{pe('check')} Я подписался!",
    },
    "admin_panel": {"en": f"{pe('gear')} Admin Panel", "ru": f"{pe('gear')} Админ-панель"},
    "admin_stats": {"en": f"{pe('chart')} Statistics", "ru": f"{pe('chart')} Статистика"},
    "admin_broadcast": {"en": f"{pe('loudspeaker')} Broadcast", "ru": f"{pe('loudspeaker')} Рассылка"},
    "admin_channels": {"en": f"{pe('people')} Channels", "ru": f"{pe('people')} Каналы"},
    "stats_text": {
        "en": f"{pe('chart')} Statistics\n\n{pe('people')} Total users: <b>{{total}}</b>\n{pe('new')} New today: <b>{{new}}</b>\n{pe('chart')} Total QR codes: <b>{{qr_total}}</b>\n{pe('up')} QR today: <b>{{qr_today}}</b>\n{pe('loudspeaker')} Required channels: <b>{{channels}}</b>",
        "ru": f"{pe('chart')} Статистика\n\n{pe('people')} Пользователей: <b>{{total}}</b>\n{pe('new')} Новых сегодня: <b>{{new}}</b>\n{pe('chart')} Всего QR-кодов: <b>{{qr_total}}</b>\n{pe('up')} QR сегодня: <b>{{qr_today}}</b>\n{pe('loudspeaker')} Каналов подписки: <b>{{channels}}</b>",
    },
    "bc_enter": {
        "en": f"{pe('loudspeaker')} Send me the broadcast message text:",
        "ru": f"{pe('loudspeaker')} Пришлите текст рассылки:",
    },
    "bc_preview": {
        "en": f"{pe('loudspeaker')} Preview:\n\n{{text}}\n\nSend this to all users?",
        "ru": f"{pe('loudspeaker')} Предпросмотр:\n\n{{text}}\n\nРазослать всем пользователям?",
    },
    "bc_confirm": {"en": f"{pe('check')} Confirm Send", "ru": f"{pe('check')} Подтвердить"},
    "bc_cancel_btn": {"en": f"{pe('cross')} Cancel", "ru": f"{pe('cross')} Отмена"},
    "bc_sending": {"en": f"{pe('loudspeaker')} Sending... 0/{{total}}", "ru": f"{pe('loudspeaker')} Отправка... 0/{{total}}"},
    "bc_done": {
        "en": f"{pe('check')} Broadcast complete!\n\n{pe('check')} Sent: {{sent}}\n{pe('cross')} Failed: {{failed}}\n{pe('chart')} Total: {{total}}",
        "ru": f"{pe('check')} Рассылка завершена!\n\n{pe('check')} Доставлено: {{sent}}\n{pe('cross')} Не удалось: {{failed}}\n{pe('chart')} Всего: {{total}}",
    },
    "bc_cancelled": {"en": f"{pe('cross')} Broadcast cancelled.", "ru": f"{pe('cross')} Рассылка отменена."},
    "ch_list": {"en": f"{pe('people')} Required Channels:\n\n", "ru": f"{pe('people')} Каналы подписки:\n\n"},
    "ch_none": {"en": f"{pe('people')} No required channels.\nAdd one below:", "ru": f"{pe('people')} Нет каналов подписки.\nДобавьте:"},
    "ch_add": {"en": f"{pe('plus')} Add Channel", "ru": f"{pe('plus')} Добавить канал"},
    "ch_prompt": {
        "en": "Send me the channel ID or @username\n(Bot must be admin in the channel):",
        "ru": "Пришлите ID канала или @юзернейм\n(Бот должен быть админом канала):",
    },
    "ch_added": {"en": f"{pe('check')} Channel added: {{title}}", "ru": f"{pe('check')} Канал добавлен: {{title}}"},
    "ch_failed": {
        "en": f"{pe('cross')} Failed. Make sure the bot is admin.\nError: {{err}}",
        "ru": f"{pe('cross')} Ошибка. Убедитесь, что бот — админ.\nОшибка: {{err}}",
    },
    "access_denied": {"en": "Access denied.", "ru": "Доступ запрещён."},
    "select_resolution": {
        "en": f"{pe('image')} Select PNG resolution:",
        "ru": f"{pe('image')} Выберите разрешение PNG:",
    },
}

PREMIUM_EMOJI = {
    "wave": "5886433441456591581",
    "shield": "5251203410396458957",
    "books": "5373098009640836781",
    "bell": "5458603043203327669",
    "alarm": "5413704112220949842",
    "check": "5821077289185578407",
    "calendar": "5433614043006903194",
    "book": "6021544101747366254",
    "person": "6021659919835469581",
    "paperclip": "6039451237743595514",
    "back": "5352759161945867747",
    "chart": "5231200819986047254",
    "gear": "6021637109264160908",
    "loudspeaker": "6021418126061605425",
    "people": "6021690418398239007",
    "hammer": "6023719726021090908",
    "lightning": "5456140674028019486",
    "cross": "5210952531676504517",
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    entry = TEXTS.get(key, {})
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


TYPE_NAMES = {
    "url": {"en": f"{pe('link')} Link", "ru": f"{pe('link')} Ссылка"},
    "text": {"en": f"{pe('text')} Text", "ru": f"{pe('text')} Текст"},
    "phone": {"en": f"{pe('phone')} Phone", "ru": f"{pe('phone')} Телефон"},
    "email": {"en": f"{pe('mail')} Email", "ru": f"{pe('mail')} Почта"},
    "wifi": {"en": f"{pe('wifi')} WiFi", "ru": f"{pe('wifi')} WiFi"},
    "vcard": {"en": f"{pe('person')} Contact", "ru": f"{pe('person')} Контакт"},
    "sms": {"en": f"{pe('sms')} SMS", "ru": f"{pe('sms')} SMS"},
}

TYPE_PROMPTS = {
    "url": "prompt_url",
    "text": "prompt_text",
    "phone": "prompt_phone",
    "email": "prompt_email",
    "sms": "prompt_sms",
}
