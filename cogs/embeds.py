import discord
from discord.ext import commands


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # utility embeds
    # returns user avatar
    async def user_avatar(self, user):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name}\'s avatar'
        )
        embed.set_image(
            url=user.avatar_url
        )
        return embed

    # returns status changed embed
    async def status_changed(self, user, status):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} heeft status veranderd',
            icon_url=user.avatar_url
        )
        embed.add_field(
            name='Nieuwe status',
            value=status
        )
        return embed

    # returns short status changed embed
    async def status_changed_short(self):
        embed = discord.Embed(
            colour=discord.Colour.green()
        )
        embed.set_author(
            name='Mijn status is veranderd!'
        )
        return embed

    # returns loading embed
    async def loading(self):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name="Bereid wat dingen voor!",
            icon_url=self.bot.user.avatar_url
        )
        return embed

    # returns error embed
    async def error(self):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f"oops iets ging verkeerd..",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Weer dit bericht?",
            value="Meld het aan een moderator of aan het dev team!"
        )
        return embed

    # # warning embeds
    # returns give warning embed
    async def warning(self, user, warning, warner):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{user.name} is gewaarschuwd",
            icon_url=user.avatar_url
        )
        embed.add_field(
            name="Redenen",
            value=warning,
            inline=False
        )
        embed.add_field(
            name="Gegeven door",
            value=f"`{warner.name}#{warner.discriminator}`",
        )
        return embed

    # returns short give warning embed
    async def warning_short(self, user, warner):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is gewaarshuwd door {warner.name}',
            icon_url=user.avatar_url
        )
        return embed

    # returns warnings not found embed
    async def nowarning(self, user):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{user.name} heeft geen waarschuwingen",
            icon_url=user.avatar_url
        )
        return embed

    # returns pardon warning embed
    async def pardon(self, user, vergever):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is vergeven',
            icon_url=user.avatar_url
        )
        embed.add_field(
            name='Vergever',
            value=f'`{vergever.name}`'
        )
        return embed

    # returns short pardon warning embed
    async def pardon_short(self, user):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{user.name} is vergeven",
            icon_url=user.avatar_url
        )
        return embed

    # returns pardon not found embed
    async def nopardon(self):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name="Waarschuwing niet gevonden",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Nummer correct?",
            value="Zoek de warning met `warnings @hope`"
        )
        return embed

    # # ban embeds
    # returns ban embed
    async def ban(self, user, banner):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is verbannen',
            icon_url=user.avatar_url
        )
        embed.add_field(
            name='Banner',
            value=f'`{banner.name}`'
        )
        return embed

    # return short ban embed
    async def ban_short(self, user):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is verbannen',
            icon_url=user.avatar_url
        )
        return embed

    # # uitleg commands
    # algemene help command
    async def help(self):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name='Hier zijn alle commands!',
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name='Moderatie (Alleen voor moderators)',
            value=# '- !ban @gebruiker(s) redenen\n'
                  # '- !kick @gebruiker(s) redenen\n'
                  '- !warn @gebruiker(s) redenen\n'
                  '- !pardon @gebruiker(s) redenen\n'
                  '- !warnings @gebruiker',
            inline=False
        )
        embed.add_field(
            name='Bot aanpassen (Alleen voor moderators)',
            value='- !status [een status]',
            inline=False
        )
        return embed

    # command uitleg
    async def explain(self, command, uitleg):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name="Command mist iets",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name=f"Hoe werkt `{command}`",
            value=uitleg
        )
        return embed


def setup(bot):
    bot.add_cog(Embeds(bot))
