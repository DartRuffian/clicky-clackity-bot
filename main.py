"""Main Bot File"""
# Discord Imports
import discord
from discord.ext import commands

# Keep Bot Online
from webserver import keep_alive

# Other Imports
from datetime import datetime            # Get bot launch time
from os import listdir, getcwd, environ  # Load cogs/environment vars (token)
from utils import Utils                  # Utility functions


class DiscordBot:
    """Was originally just in separate functions, but I wanted to organize it into a class"""

    def __init__(self):
        """Set up the bot"""
        # Define the bot itself
        self.bot = commands.Bot(
            command_prefix=commands.when_mentioned_or("."),
            owner_id=400337254989430784,
            case_insensitive=True,
            intents=self.set_intents(),
        )

        # Custom Attributes
        self.bot.BASE_DIR = getcwd()
        self.bot.EMBED_COLOR = 0x0E151D
        self.bot.LAUNCH_TIME = datetime.utcnow()
        self.bot.utils = Utils(self.bot)
        self.load_all_cogs()

        @self.bot.event
        async def on_ready():
            # Called whenever the bot connects to Discord
            print("Logged in")
            print(f"Username: {self.bot.user.name}")
            print(f"User Id : {self.bot.user.id}")

    @staticmethod
    def set_intents() -> discord.Intents:
        """Set all the used intents for the bot"""
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.emojis = True

        return intents

    @staticmethod
    def get_token() -> str:
        """Load the bot's Token"""
        try:
            # If running locally
            with open("tokens.txt", "r") as f:
                token = f.read().split("\n")[0]
        except FileNotFoundError:
            # If running on server
            token = environ.get("DISCORD_BOT_SECRET")

        return token

    def load_all_cogs(self) -> None:
        # Load all cogs
        for filename in listdir("./cogs"):
            if filename.endswith(".py"):
                self.bot.load_extension(f"cogs.{filename[:-3]}")

    def start(self) -> None:
        keep_alive()
        self.bot.run(self.get_token())


def main() -> None:
    bot = DiscordBot()
    bot.start()


if __name__ == "__main__":
    main()
