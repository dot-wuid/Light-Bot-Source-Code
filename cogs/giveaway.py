import nextcord
from nextcord.ext import commands, tasks
import datetime
import asyncio
import random

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ongoing_giveaways = {}
        self.check_giveaways.start()

    @tasks.loop(seconds=10)
    async def check_giveaways(self):
        current_time = datetime.datetime.utcnow()
        for giveaway_id, giveaway_data in list(self.ongoing_giveaways.items()):
            end_time = giveaway_data['end_time']
            if current_time > end_time:
                # Giveaway ended, determine and announce the winner
                participants = list(giveaway_data['participants'])  # Convert set to list
                if participants:
                    winner = random.choice(participants)
                    channel_id = giveaway_data['channel_id']
                    channel = self.bot.get_channel(channel_id)

                    if channel:
                        # Build an embed with giveaway information
                        embed = nextcord.Embed(
                            title=f"Giveaway Ended - {giveaway_data['item']}",
                            description=f"Winner: {winner.mention}\n"
                                        f"Giveaway ID: {giveaway_id}",
                            color=nextcord.Color.green()
                        )
                        embed.set_footer(text=f"Ended at {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                        await channel.send(f"Winner: {winner.mention}!", embed=embed)
                    else:
                        print(f"Unable to find channel with ID {channel_id} for giveaway {giveaway_id}")

                    # Remove the ended giveaway from the dictionary
                    del self.ongoing_giveaways[giveaway_id]
                else:
                    print(f"No participants in the giveaway {giveaway_id}, ending without a winner.")
                    # Remove the ended giveaway from the dictionary even if there are no participants
                    del self.ongoing_giveaways[giveaway_id]

    @commands.command(name='giveaway', aliases=['gwymake'], help="Giveaway Stuff! \n ~gwymake [Name] [time in seconds] [item to giveaway]")
    async def start_giveaway(self, ctx, name, duration, *, item):
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(duration))
        giveaway_id = str(ctx.message.id)  # Using the message ID as a unique identifier
        self.ongoing_giveaways[giveaway_id] = {'end_time': end_time, 'participants': set(), 'channel_id': ctx.channel.id, 'item': item}
        
        # Build an embed with giveaway information
        embed = nextcord.Embed(
            title=f"Giveaway Started - {item}",
            description=f"**Name:** {name}\n"
                        f"**Item:** {item}\n"
                        f"**Duration:** {duration} seconds\n"
                        f"React with 🎉 to participate!",
            color=nextcord.Color.blue()
        )
        embed.set_footer(text=f"Giveaway ID: {giveaway_id}")

        message = await ctx.send(embed=embed)

        # Add reaction to the giveaway message
        await message.add_reaction('🎉')

        def check(reaction, user):
            return not user.bot and str(reaction.message.id) == str(message.id) and str(reaction.emoji) == '🎉'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=int(duration), check=check)
            self.ongoing_giveaways[giveaway_id]['participants'].add(user)
        except asyncio.TimeoutError:
            print(f"No participants in the giveaway {giveaway_id}, ending without a winner.")
        else:
            print(f"Participants for giveaway {giveaway_id}: {self.ongoing_giveaways[giveaway_id]['participants']}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and str(reaction.message.id) in self.ongoing_giveaways:
            # User reacted to an ongoing giveaway
            giveaway_id = str(reaction.message.id)
            self.ongoing_giveaways[giveaway_id]['participants'].add(user)

def setup(bot):
    bot.add_cog(Giveaway(bot))
