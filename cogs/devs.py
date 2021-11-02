from discord.ext import commands


async def is_mees(ctx):
    return ctx.author.id == 298890523454734336


class Devs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load cog
    @commands.command()
    @commands.check(is_mees)
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} loaded`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # Unload cog
    @commands.command()
    @commands.check(is_mees)
    async def unload(self, ctx, cog):
        if cog == 'devs':
            return await ctx.send('`devs cannot be unloaded only updated!`')

        try:
            self.bot.unload_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} unloaded`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # Update cog
    @commands.command()
    @commands.check(is_mees)
    async def update(self, ctx, cog):
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} updated`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # poke database
    @commands.command()
    @commands.check(is_mees)
    async def poke(self, ctx):
        db = self.bot.get_cog('Database')
        return await ctx.send(await db.poke())

    # drops all logs
    @commands.command()
    @commands.check(is_mees)
    async def drop(self, ctx):
        db = self.bot.get_cog('Database')
        return await ctx.send(await db.drop())


def setup(bot):
    bot.add_cog(Devs(bot))
