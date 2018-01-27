import io
import random

import discord
from discord.ext import commands


class Meta:
    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        """Posts a member's avatar."""

        member = member or ctx.author
        avatar_url = member.avatar_url_as(static_format='png')

        async with ctx.session.get(avatar_url) as r:
            if r.status != 200:
                return await ctx.send('Failed to download avatar.')

            filetype = r.headers.get('Content-Type').partition('/')[-1]
            filename = f'{member.name}.{filetype}'
            file = discord.File(io.BytesIO(await r.read()), filename)
            await ctx.send(file=file)

    @commands.command(aliases=['choose'])
    async def decide(self, ctx, *, choices : str):
        """Decides between things for you."""

        if ' or ' in choices:
            choices = choices.split(' or ')
        elif ', ' in choices:
            choices = choices.split(', ')
        else:
            choices = choices.split(',')
        await ctx.send('Obviously, the answer is {}.'.format(random.choice(choices)))


def setup(bot):
    bot.add_cog(Meta())