import platform

import discord
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="help", description="List all commands.")
    async def help(self, context: Context) -> None:
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands_list = cog.get_commands()
            data = []
            for command in commands_list:
                description = command.description.partition("\n")[0]
                data.append(f"{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo", description="Get information about the bot."
    )
    async def botinfo(self, context: Context) -> None:
        embed = discord.Embed(title="Bot Information", color=0xBEBEFE)
        embed.add_field(
            name="Python Version:", value=platform.python_version(), inline=True
        )
        embed.add_field(name="Prefix:", value="/ or !", inline=True)
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo", description="Get information about the server."
    )
    async def serverinfo(self, context: Context) -> None:
        embed = discord.Embed(title=context.guild.name, color=0xBEBEFE)
        if context.guild.icon:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(name="Channels", value=len(context.guild.channels))
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(name="ping", description="Check if the bot is alive.")
    async def ping(self, context: Context) -> None:
        embed = discord.Embed(
            title="Pong!",
            description=f"Latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
