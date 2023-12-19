from core.webhooks import app
from core.setup import local_register


local_register.register_main_bot(dp, app, bot, allowed_updates=dp.resolve_used_update_types())
