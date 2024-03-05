import nextcord 
from nextcord.ext import commands, tasks
import json

import dir
# Prefix for bot commands
BOT_PREFIX = "~"
intents = nextcord.Intents.all()
# Create an instance of the bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX), intents=intents)


if BOT_PREFIX == "t!":
    print("TESTING MODE ACTIVE")


# Emoji to react with
reaction_emoji = "👍"

# JSON file to store counting channel and count data
from datetime import datetime
count_file = 'count.json'

counting_channels = {}
counts = {}
import os

bot.load_extension('cogs.moderation')
bot.load_extension('cogs.developer')
bot.load_extension('cogs.util')
bot.load_extension('cogs.fun')
bot.load_extension('cogs.giveaway')
bot.remove_command('help')

class CogDropdown(nextcord.ui.Select):
    def __init__(self, bot):
        cog_options = [nextcord.SelectOption(label=cog_name, value=cog_name) for cog_name in bot.cogs.keys()]
        super().__init__(
            placeholder="Select a command cog",
            options=cog_options
        )
        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        cog_name = self.values[0]
        cog = self.bot.get_cog(cog_name)
        if cog:
            embed = nextcord.Embed(title=f"{cog.qualified_name} Commands", color=nextcord.Color.blue())
            command_list = '\n'.join([f"`{cmd.name}` - {cmd.short_doc}" for cmd in cog.get_commands()])
            embed.description = command_list
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Cog not found.")



class HelpView(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(CogDropdown(bot))


bot.remove_command("help")
@bot.command(name='help', aliases=['commands'], help="Displays a list of commands in a selected cog")
async def help_command(ctx):
    embed = nextcord.Embed(title="Command List and Help", color=nextcord.Color.green())
    embed.set_footer(text=f"Use '{ctx.prefix}help [command]' for more information on a specific command.")
    
    view = HelpView(bot)
    await ctx.send("Select a command cog:", embed=embed, view=view)

@bot.event
async def on_message(message):
    if message.channel.type == nextcord.ChannelType.news:
          await message.publish()
    # List of keywords and phrases related to suicide
    suicide_keywords = ['suicide', 'suicidal', 'taking my own life', 'ending it all', 'self-harm', 'suicide attempt', 'kys', 'kms']
    
    # Check if any of the keywords are whole words in the message content
    if any(keyword in message.content.lower().split() for keyword in suicide_keywords) and not message.author.bot:
        # Replace this with the appropriate suicide prevention center number
        response = "**Remember: There are people who care about you, don't do it.** If you're struggling, please reach out to the Suicide Prevention Lifeline at 1-800-273-8255 \nOther Countries: Nepal 1166 | Argentina 911 / 5275-1135 | Australia 1800 55 1800 | Austria 142 | Canada 1-833-456-4566 | Chile *4141 | China 021-64387250 | Cuba 104 | Czech Republic 116 111 or 116 123 | Finland 09 2525 0113 | France 3114 | Germany 0800 111 0 111 | Greece 1018 | India 788-788-9882 | Korea 1588-9191 | Ukraine 7333 | UK 116 123 | USA 988 | South Africa 0800 567 567 | Other Countries 999, 112, 911, 190, 991"
        await message.channel.send(response)
    
    # It's important to let other event listeners process the message as well
    await bot.process_commands(message)

        

from nextcord import Forbidden

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(error)
        return

    if isinstance(error, commands.MissingRequiredArgument):
        missing_arg = error.param.name
        embed = nextcord.Embed(title="Error", description=f"Missing required argument: `{missing_arg}`", color=nextcord.Color.red())
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BadArgument):
        # Handle the case when a value is invalid
        await ctx.send(f'Error: Invalid argument. Please provide a valid argument for the command.')
        return

    if isinstance(error, commands.CommandInvokeError) and "bot.run" in str(error.original):
        return
    if isinstance(error, Forbidden):
            # Handle the case when the bot doesn't have the necessary permissions
            await ctx.send('Error: Missing permissions. The bot does not have the required permissions for this command.')
            return
    if isinstance(error, commands.CommandNotFound):
        # Send a pop-up or a message for invalid commands
        await ctx.send("Invalid command. Type ~help for a list of commands.")
        return

    




statuses = ["~help", "discord.projectlight.xyz", "Bot By jqm1e", "Sponsored By dsc.gg/binarybitlab"]
import random
@tasks.loop(minutes=2)
async def change_status():
    
    await bot.change_presence(activity=nextcord.Game(name=random.choice(statuses)))



@bot.event
async def on_ready():
    change_status.start()
    caa = bot.get_channel(1173092338210451586)
    




@bot.event
async def on_guild_join(guild):
    # Get the first available text channel in the server
    first_text_channel = next((channel for channel in guild.text_channels if isinstance(channel, nextcord.TextChannel)))

    if first_text_channel:
        # Send a welcome message to the first text channel
        a = nextcord.Embed(
            title="Thanks.",
            description="Thanks For Adding Me to your server!"
        )
        a.add_field(name="Support: ", value="[Support](https://discord.projectlight.xyz)")
        a.add_field(name="Developers: ", value="Owner : Papiertanne | Dev : .wuid | Dev : _samy123")
        a.add_field(name="Special Thanks To Our Server Boosters!", value="If you have Boosted Project Light At all, Just Know We Love You! :heart:")
        
        await first_text_channel.send(embed=a)

import random

@bot.slash_command()
async def truth(ctx):
    random_truth = random.choice(dir.truths)
    await ctx.send(random_truth)
@bot.slash_command()
async def dare(ctx):
    random_dare = random.choice(dir.dares)
    await ctx.send(random_dare)

main_bot = "YOUR TOKEN HERE ;)"

bot.run(main_bot)
