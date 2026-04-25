import hashlib
import logging
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
from ..emojis import pe

router = Router()
logger = logging.getLogger(__name__)

_cache: dict[str, str] = {}


@router.inline_query()
async def inline_qr(query: InlineQuery, bot: Bot):
    text = query.query.strip()
    if not text:
        await query.answer(
            [],
            cache_time=10,
            switch_pm_text=f"{pe('lightning')} QR Generator",
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

    img = qr_engine.generate(text, {"format": "png"})

    if STORAGE_CHANNEL_ID and STORAGE_CHANNEL_ID != 0:
        try:
            msg = await bot.send_photo(
                chat_id=STORAGE_CHANNEL_ID,
                photo=BufferedInputFile(img.getvalue(), "qr.png"),
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
        except Exception as e:
            logger.warning("Inline upload to storage channel failed: %s", e)

    results = [
        InlineQueryResultArticle(
            id=cache_key[:8],
            title=f"{pe('lightning')} QR Code",
            description=f"QR: {text[:50]}",
            input_message_content=InputTextMessageContent(
                message_text=f"{pe('lightning')} QR Code for: <code>{text}</code>",
                parse_mode="HTML",
            ),
        )
    ]
    await query.answer(results, cache_time=60)
