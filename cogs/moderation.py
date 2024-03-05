from nextcord.ext import commands
import nextcord
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Moderation Cog Status : ✅")
    
    @commands.command(help="Delete a specified number of messages from the current channel. \n Manage Message Permissions Required")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):

        # Check if the amount is within a valid range
        if amount < 1 or amount > 100:
            await ctx.send("Please specify a number of messages to delete between 1 and 100.")
            return

        # Check if the amount is greater than 100
        if amount > 100:
            await ctx.send("You can't delete more than 100 messages at once.")
            return

        # Delete the specified number of messages
        deleted = await ctx.channel.purge(limit=amount + 1)
        em = nextcord.Embed(
                title=f"Deleted {len(deleted) - 1} messages.",
                description=" "
                )
        await ctx.send(embed=em)


    @commands.command(help="Unban a user from the server by providing their user ID. \n ex. ~unban 2929294979435")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        idee = self.bot.get_user(id)
        
        if idee is not None:
            try:
                await ctx.guild.unban(idee)
                em = nextcord.Embed(
                    title=f"Unbanned {idee.name}",
                    description=" "
                )
                em.set_footer(text=f"Moderator | {ctx.author.name}")
                await ctx.send(embed=em)
            except nextcord.NotFound:
                await ctx.send('User not banned.')
            except nextcord.Forbidden:
                await ctx.send("I don't have the necessary permissions to unban users.")
        else:
            await ctx.send("ERROR Contact Staff @ Project Light")

    async def add_role(self, user, role):
        try:
            await user.add_roles(role)
        except nextcord.Forbidden:
            return "I don't have permission to add this role."
        except nextcord.HTTPException:
            return "An error occurred while adding the role."
        return f"Added the {role.name} role to {user.mention}."


    @commands.command(help="Add a role to a user. \n Admin required")
    @commands.has_permissions(administrator=True)
    async def roleadd(self, ctx, user: nextcord.Member, role: nextcord.Role):
        if role not in user.roles:
            result = await self.add_role(user, role)
            await ctx.send(result)
        else:
            await ctx.send(f"{user.mention} has the {role.name} role.")

    @commands.command(help="Ban a user from the server, preventing them from rejoining. \n ban members Required")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: nextcord.Member, reason):
        await user.send(f"You Have Been Banned In {ctx.guild.name} By {ctx.author.name} For {reason}")
        await user.ban(reason=reason)
        emb = nextcord.Embed(
            title=f"Banned {user.name}",
            description=f"For {reason}",
        )
        emb.set_footer(text=f"Moderator | {ctx.author.name}")
        
        await ctx.send(embed=emb)
    
    

    @commands.command(name='roleremove', help="Remove a role from a user. \n Admin Required")
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx, member: nextcord.Member, role: nextcord.Role):
        await member.remove_roles(role)
        await ctx.send(f'Removed the role {role.name} from {member.display_name}.')


    @commands.command(name="webhook_info", help="Display information about a webhook. \n DONT DO IN A PUBLIC CHANNEL")
    @commands.has_permissions(administrator=True)
    async def webhook_info(self, ctx, channel: nextcord.TextChannel = None):
        # If no channel is specified, use the current channel
        if channel is None:
            channel = ctx.channel

        # Fetch all webhooks in the specified channel
        webhooks = await channel.webhooks()

        # Display information for each webhook in an embed
        for webhook in webhooks:
            embed = nextcord.Embed(title=f"Webhook Information for {channel.name}", color=0x00ff00)
            embed.add_field(name="Webhook ID", value=webhook.id, inline=False)
            embed.add_field(name="Webhook Token", value=webhook.token, inline=False)
            embed.add_field(name="Webhook URL", value=webhook.url, inline=False)
            embed.add_field(name="Webhook Channel", value=webhook.channel.name, inline=False)
            embed.add_field(name="Webhook Created At", value=webhook.created_at, inline=False)

            # Check if the webhook has a user
            if webhook.user:
                embed.add_field(name="Webhook Name", value=webhook.name, inline=False)
            else:
                embed.add_field(name="Webhook Name", value="Unknown", inline=False)

            await ctx.send(embed=embed)

    @commands.command(help="Kick a user from the server. \n Kick Members Permissions Requried")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: nextcord.Member, reason=None):
        if user is not None:
            await ctx.guild.kick(user)

            embed = nextcord.Embed(description=f"{user.mention} was kicked by {ctx.author.mention}\r\nReason: {reason}")
            embed.set_footer(text="© Project Light Productions | dsc.gg/projectlight")
            await ctx.send(embed=embed)    
    

    @commands.command(name='createrole', help="Create a new role in the server. \n (Manage role Permissions Required)")
    async def make_role(self, ctx, name, color):
        # Check if the user has the necessary permissions to create roles
        if ctx.author.guild_permissions.manage_roles:
            # Convert the color argument to a Discord Color object
            role_color = nextcord.Colour(int(color, 16))
            
            # Create the role
            new_role = await ctx.guild.create_role(name=name, color=role_color)
            
            # Send a confirmation message
            await ctx.send(f"Role '{new_role.name}' created with color {role_color}")
        else:
            # Send an error message if the user doesn't have the required permissions
            await ctx.send("You don't have the necessary permissions to create roles.")

    


def setup(bot):
    bot.add_cog(Moderation(bot))