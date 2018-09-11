import discord
from discord.ext import commands


# setup
class Base:
    """
    Set of basic commands that provide basic commands to check if the bot is up, and to link
    to the GitHub repository.
    """

    def __init__(self, bot):
        self.bot = bot

    # ping command
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='ping')
    async def ping(self, ctx):
        """
        Replies with "Pong!"
        :param ctx: The command invocation context
        :return: None
        """

        await ctx.send(_test_example())

    # github command
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='github', description='Replies with a link to the bot\' GitHub repository.')
    async def github(self, ctx):
        """
        Replies with a link to the bot's GitHub repo.
        :param ctx: The command invocation context
        :return: None
        """
        await ctx.send(
            "I'm open source! You can contribute to ACMBot development at: https://github.com/UWB-ACM/ACMBot")


# add this cog to the bot
def setup(bot):
    bot.add_cog(Base(bot))


def _test_example():
    """
    Example of how to incorporate doctests for commands

    >>> _test_example()
    'Pong!'

    :return: 'Pong!'
    """

    return 'Pong!'


# optional, but helpful for testing via the shell
if __name__ == '__main__':
    import doctest

    doctest.testmod()
