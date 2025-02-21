from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, Message, WebAppInfo
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def command_start(msg: Message, bot: Bot, base_url: str):
    await bot.set_chat_menu_button(
        chat_id=msg.chat.id,
        menu_button=MenuButtonWebApp(text="Start Tapping!", web_app=WebAppInfo(url=f"{base_url}/index")),
    )
    
    await msg.answer(
        "Hi and welcome to PavloCoin😎\n"
        "It is time to tap!👆 Tap anytime and anywhere!⌚\n"
        "Become the most powerful pavlik, PavloCoin tapper!😈",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Open PavloCoin",
                    web_app=WebAppInfo(url=f"{base_url}/index")
                )
            ]]
        )
    )
