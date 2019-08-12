import discord
from discord.ext import commands
from robot import queries


class FilterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parent_cog = self.bot.get_cog('DeepFakeBot')
        self.session = self.parent_cog.session

    async def cog_check(self, ctx):
        connection_ok = await self.parent_cog.cog_check(ctx)
        self.session = self.parent_cog.session
        return connection_ok

    @commands.group(name='filter')
    async def filter(self, ctx):
        """Text filter functions for removing bad data from your subject's chat history."""
        if ctx.invoked_subcommand is None:
            await ctx.send('')

    @filter.command()
    async def add(self, ctx, subject: discord.Member, word_to_add):
        queries.add_a_filter(self.session, ctx, subject, word_to_add)
        await ctx.send(f'Added text filter `{word_to_add}` to `{subject.name}` for this server.')

    @filter.command()
    async def remove(self, ctx, subject: discord.Member, word_to_drop):
        found_word = queries.remove_a_filter(self.session, ctx, subject, word_to_drop)
        if found_word:
            await ctx.send(f'Removed text filter `{word_to_drop}` to `{subject.name}` for this server.')
        else:
            await ctx.send(f'Text filter `{word_to_drop}` not found for `{subject.name}` on this server.')

    @filter.command()
    async def show(self, ctx, subject: discord.Member):
        found_filters = queries.find_filters(self.session, ctx, subject)
        if len(found_filters) > 0:
            n = '\n'
            await ctx.send(f'Filters applied to {subject.name} for this server:\n```{n}{n.join(found_filters)}{n}```')
        else:
            await ctx.send(f'No filters applied to {subject.name} for this server.')

    @filter.command()
    async def clear_all(self, ctx, subject: discord.Member):
        queries.clear_filters(self.session, ctx, subject)
        await ctx.send(f'Text filters removed for `{subject.name}` on this server.')