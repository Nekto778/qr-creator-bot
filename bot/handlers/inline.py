import hashlib
from aiogram import Router, F, Bot
from aiogram.types import (
    InlineQuery,
    InlineQueryResultCachedPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
    BufferedInputFile,
)
from ..config import STORAGE_CHANNEL_ID
from ..services.qr_engine import qr_engine

router = Router()

_cache: dict[str, str] = {}


@router.inline_query()
async def inline_qr(query: InlineQuery, bot: Bot):
    text = query.query.strip()
    if not text:
        await query.answer(
            [],
            cache_time=10,
            switch_pm_text="⚡ Open bot to generate QR",
            switch_pm_parameter="start",
        )
        return

    cache_key = hashlib.md5(text.encode()).hexdigest()

    if cache_key in _cache:
        results = [
            InlineQueryResultCachedPhoto(
                id=cache_key[:8],
                photo_file_id=_cache[cache_key],
            )
        ]
        await query.answer(results, cache_time=300)
        return

    img = qr_engine.generate(text)

    if STORAGE_CHANNEL_ID:
        try:
            msg = await bot.send_photo(
                STORAGE_CHANNEL_ID,
                BufferedInputFile(img.getvalue(), "qr.png"),
            )
            file_id = msg.photo[-1].file_id
            _cache[cache_key] = file_id

            results = [
                InlineQueryResultCachedPhoto(
                    id=cache_key[:8],
                    photo_file_id=file_id,
                )
            ]
            await query.answer(results, cache_time=300)

            try:
                await bot.delete_message(STORAGE_CHANNEL_ID, msg.message_id)
            except Exception:
                pass
            return
        except Exception:
            pass

    results = [
        InlineQueryResultArticle(
            id=cache_key[:8],
            title="⚡ QR Code",
            description=f"Generate QR for: {text[:50]}",
            input_message_content=InputTextMessageContent(
                message_text=f"⚡ QR Code for: <code>{text}</code>",
                parse_mode="HTML",
            ),
        )
    ]
    await query.answer(results, cache_time=60)
