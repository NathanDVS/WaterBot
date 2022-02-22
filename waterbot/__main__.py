import hikari
from lightbulb import BotApp
from waterbot.utils import Utils

bot = BotApp(token=Utils.get_bot_token(), intents=hikari.Intents.ALL, prefix=Utils.get_prefix(), owner_ids=[755514224637378571])
bot.load_extensions_from("./waterbot/plugins")

if __name__ == "__main__":
    bot.run()
