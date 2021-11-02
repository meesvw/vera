import asyncio
import discord
from datetime import datetime
from discord.ext import commands


def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = self.bot.get_channel(734365925620580402)

    # # utility
    # clear messages command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def clear(self, ctx, amount: int):
        if amount < 1:
            return await ctx.send(f'Hey {ctx.author.mention} ik heb een positief getal nodig!')

        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Ik heb {amount} bericht(en) verwijderd!')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f'Hey {ctx.author.mention} je kan alleen nummers gebruiken!')

    # clear lobby command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def lobby(self, ctx, amount: int):
        if ctx.channel.id != 696859692684541983:
            return await ctx.send(f'Hey {ctx.author.mention} dit is niet de lobby!')

        if amount < 1:
            return await ctx.send(f'Hey {ctx.author.mention} ik heb een positief getal nodig!')

        embeds = self.bot.get_cog('Embeds')

        await ctx.channel.purge(limit=amount+1)
        message = await ctx.channel.send('**Waarom zie ik zo weinig kanalen ?**\n'
                               'Dat komt omdat je momenteel niet geverifieerd bent. '
                               'Toegang tot de rest van de server / kanalen wordt verleend na ontvangst van de '
                               'geverifieerde rol, die handmatig wordt toegewezen door een moderator bij voltooien '
                               'van het verificatieproces.\n\n'
                               '**Waarom ben ik niet toegelaten?**\n'
                               'Dat zou kunnen omdat je niet je rollen hebt geselecteerd of je hebt niet gezegd waarom'
                               ' je de server bent gejoined.\n\n'
                               '**Hoe kan ik geverifieerd worden?**\n'
                               'Wanneer je de server joined dan moet je even je rollen selecteren en aan een moderator '
                               'vertellen waarom je de server bent gejoined! Als een moderator vindt dat jij niet past '
                               'bij onze server dan heeft de moderator het recht om jou te weigeren.')
        await message.pin()
        await self.log_channel.send(embed=await embeds.lobby_cleared(ctx.author))

    # show avatar command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def avatar(self, ctx, user: discord.User):
        embeds = self.bot.get_cog('Embeds')
        return await ctx.send(embed=await embeds.user_avatar(user))

    # # welcome commands
    # welcome command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def welkom(self, ctx, user: discord.User):
        add_role = ctx.guild.get_role(668825700798693377)
        remove_role = ctx.guild.get_role(685607372428804104)

        if add_role in user.roles:
            return await ctx.send(f'Hey {ctx.author.mention} deze gebruiker is al toegelaten!')

        await user.remove_roles(
            remove_role,
            reason='Toegelaten tot de server'
        )

        await user.add_roles(
            add_role,
            reason='Toegelaten tot de server'
        )

        introductie_channel = self.bot.get_channel(670218992211853344)

        embeds = self.bot.get_cog('Embeds')

        await user.send(embed=await embeds.join_dm(user, ctx.author, introductie_channel))

        welcome_role = ctx.guild.get_role(701713402745323542)
        general_channel = self.bot.get_channel(671066993792647191)

        await self.log_channel.send(embed=await embeds.toegang_gegeven(ctx.author, user))
        await general_channel.send(f'{welcome_role.mention} Hiep hiep hoera, er is een nieuw lid bij genaamd {user.mention} 🎉')

    # weiger command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def weiger(self, ctx, user: discord.User):
        role = ctx.guild.get_role(668825700798693377)

        if ctx.author == user:
            return await ctx.send(f'Hey {ctx.author.mention} je kan jezelf niet weigeren')

        if role not in user.roles and not user.bot:
            await user.send(f'**Je bent uit Cosplayers From NL gezet {user.mention}.**\n'
                            f'Dit kwam doordat je niet geverifieerd was of ongeschikt was voor de server. '
                            f'Denk je dat dit een fout was of wil je het opnieuw proberen kan je via deze link joinen: '
                            f'\nhttps://discord.gg/AjHwdycCkh')
            await user.kick(reason='Geweigerd voor de server')
        else:
            await ctx.send(f'Hey {ctx.author.mention} ik kan deze gebruiker niet weigeren')

        embeds = self.bot.get_cog('Embeds')
        await self.log_channel.send(embed=await embeds.toegang_geweigerd(ctx.author, user))

    # # warning commands
    # warn command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def warn(self, ctx, users: commands.Greedy[discord.User], *, warning=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        for user in users:
            output = await db.warn(user, warning, ctx.author)
            if output == "error":
                await ctx.send(embed=await embeds.error())
                break
            channel = self.bot.get_channel(719263750426984538)
            await ctx.send(embed=await embeds.warning_short(user, ctx.author))
            await channel.send(embed=await embeds.warning(user, warning, ctx.author))

    # show warnings command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def warnings(self, ctx, warnings_user: discord.User=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        if warnings_user:
            user_warnings = await db.warnings(warnings_user)
        else:
            return await ctx.send(embed=await embeds.explain(
                "warnings",
                f"`warnings @hope`"))
        try:
            if user_warnings["warnings"]:
                message = await ctx.send(embed=await embeds.loading())

                dict_list = []
                for warning in user_warnings["warnings"]:
                    dict_list.append(warning)

                emoji_list = ["◀", "▶"]
                menu_number = 0
                for emoji in emoji_list:
                    await message.add_reaction(emoji=emoji)
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in emoji_list and reaction.message.id == \
                           message.id
                def create_embed(number):
                    embed = discord.Embed(
                        colour=discord.Colour.blue()
                    )
                    embed.set_author(
                        name=f"{warnings_user.name}'s waarschuwing {number}",
                        icon_url=warnings_user.avatar_url
                    )
                    embed.add_field(
                        name="Redenen",
                        value=user_warnings["warnings"][number]["warning"]
                    )
                    embed.set_footer(
                        text=f'Door: {user_warnings["warnings"][number]["warner"]} - {user_warnings["warnings"][number]["time"]}'
                    )
                    return embed

                await message.edit(embed=create_embed(dict_list[menu_number]))

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=check)
                        await message.remove_reaction(str(reaction.emoji), ctx.author)

                        if str(reaction.emoji) == "◀" and menu_number > 0:
                            menu_number -= 1
                        if str(reaction.emoji) == "▶" and menu_number != len(dict_list)-1:
                            menu_number += 1
                        await message.edit(embed=create_embed(dict_list[menu_number]))
                    except asyncio.TimeoutError:
                        await message.delete()
                        break
            else:
                return await ctx.send(embed=await embeds.nowarning(warnings_user))
        except TypeError:
            return await ctx.send(embed=await embeds.nowarning(warnings_user))

    # pardon command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def pardon(self, ctx, user: discord.User, warning=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        output = await db.pardon(ctx.author, warning)
        if warning is None:
            return await ctx.send(embed=await embeds.explain(
                "pardon",
                "|`!pardon @hope 1`| De 1 is de waarschuwing die je kan vinden door `!warnings @hope` te doen"))
        if output:
            channel = self.bot.get_channel(719263750426984538)
            await channel.send(embed=await embeds.pardon(user, ctx.author))
            return await ctx.send(embed=await embeds.pardon_short(user))
        elif not output:
            return await ctx.send(embed=await embeds.nopardon())
        else:
            return await ctx.send(embed=await embeds.error())

    # # mute commands
    # mute command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def mute(self, ctx, users: commands.Greedy[discord.User]):
        embeds = self.bot.get_cog('Embeds')
        add_role = ctx.guild.get_role(671073771246845960)
        for user in users:
            await user.add_roles(add_role, reason=f'Muted door {ctx.author.name}')
            await self.log_channel.send(embed=await embeds.user_muted(user, ctx.author))

    # unmute command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def unmute(self, ctx, user: discord.User):
        embeds = self.bot.get_cog('Embeds')
        remove_role = ctx.guild.get_role(671073771246845960)
        await user.remove_roles(remove_role, reason=f'Unmuted door {ctx.author.name}')
        await self.log_channel.send(embed=await embeds.user_unmuted(user, ctx.author))

    # # kick commands
    # kick command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def kick(self, ctx, users: commands.Greedy[discord.User], *, reason=None):
        embeds = self.bot.get_cog('Embeds')
        for user in users:
            if reason is None:
                reason = 'Geen redenen opgegeven'
            await user.kick(reason=reason)
            await self.log_channel.send(embed=await embeds.kick(user, ctx.author, reason))
            await ctx.send(embed=await embeds.kick_short(user))

    # # ban commands
    # ban command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Dev Team')
    async def ban(self, ctx, users: commands.Greedy[discord.User], *, reason=None):
        embeds = self.bot.get_cog('Embeds')
        channel = self.bot.get_channel(829743018953277480)
        community_channel = self.bot.get_channel(717814933705982083)

        for user in users:
            if reason is None:
                reason = 'Geen redenen opgegeven'
            await user.ban(reason=reason)
            await channel.send(embed=await embeds.ban(user, ctx.author, reason))
            await ctx.send(embed=await embeds.ban_short(user))
            await community_channel.send(f'{user.name}{user.discriminator}')


def setup(bot):
    bot.add_cog(Moderation(bot))
