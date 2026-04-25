from aiogram import Dispatcher
from .start import router as start_router
from .generator import router as generator_router
from .inline import router as inline_router
from .admin import router as admin_router


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(generator_router)
    dp.include_router(inline_router)
    dp.include_router(admin_router)
