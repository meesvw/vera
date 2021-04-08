import discord
from discord.ext import commands


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # utility embeds
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

    # returns warnings explanation
    async def explain_warning(self):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name="warnings mist iets"
        )
        embed.add_field(
            name="uitleg `warnings`",
            value="Het warnings command heeft een gebruiker nodig, voorbeeld: `warnings @mvw`"
        )
        return embed

    # returns pardon warning embed
    async def pardon(self, user):
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
            value="Voorbeeld: Tim heeft 3 warns, 1 is al verwijderd. "
                  "Dan blijven warning 2 en 3 staan. Dan vul je voor warning 2 dus 2 in en voor warning 3, 3."
        )
        return embed

    # # ban embeds

    # # uitleg commands
    # command uitleg
    async def explain(self, command, uitleg):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{command} mist iets",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name=f"uitleg `{command}`",
            value=uitleg
        )
        return embed


def setup(bot):
    bot.add_cog(Embeds(bot))
