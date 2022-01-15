# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from random import randint


def roll_dice(num_dice: int, num_sides: int) -> tuple:
    """Takes the number of dice to roll and the number of sides on those dice as arguments.
Returns a tuple of the total and the list of all results rolled."""
    results = [randint(1, num_sides) for _ in range(num_dice)]
    return sum(results), results


class DiceRoller(commands.Cog, name="Dice Roller"):
    """For all your die rolling needs"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Generates a set of random numbers based on user input.",
        description="""Takes a user input in the form of \"1d20\".
Where 1 is the number of dice to roll and 20 is the number of sides of that die.
The number of sides can be any number and doesn't match a standard die (4, 6, 8, etc.).""",
        aliases=["r"]
    )
    async def roll(self, ctx, die: str):
        # Die should formatted as "1d20"
        # Where 20 is the number of sides of the die and 1 is the number of times it should be rolled
        num_dice, num_sides = die.lower().split("d")

        if not num_dice:
            # Assume user wanted to roll one die if a number was not specified
            num_dice = 1
            num_sides = int(die.replace("d", ""))

        else:
            num_dice = int(num_dice)
            num_sides = int(num_sides)

        total, results = roll_dice(num_dice, num_sides)
        ordered_results: list[str] = []

        for i, result in enumerate(results):
            extra_spaces = " " * (len(str(num_dice)) - len(str(i+1)))
            ordered_results.append(f"`{str(i+1)}{extra_spaces}.` {result}")
        message = [f"You rolled **{die}** and got: **{total}**!"] + ordered_results
        await ctx.reply("\n".join(message), mention_author=False)


def setup(bot):
    bot.add_cog(DiceRoller(bot))
