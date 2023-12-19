from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext


# i18n function
def _(text: str):
    def getargstranslation(**kwargs):
        return gettext(text).format(**kwargs)

    return getargstranslation


# create commands menu
async def set_user_commands(bot: Bot):
    commands = [
        BotCommand(
            command='help',
            description='help_command'
        ),
    ]

    await bot.set_my_commands(commands=commands)


async def set_none_commands(bot: Bot):
    await bot.set_my_commands(commands=[])
