from nextcord.ext import commands
import nextcord
class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Developer Cog Status : ✅")
    
    @commands.command(name='repair-roles', help="Developer Only Commands.")
    async def repair_roles(self, ctx):
        # Get all roles in the server
        roles = ctx.guild.roles

        # Filter roles that are only composed of numbers
        number_roles = [role for role in roles if role.name.isdigit()]

        if number_roles:
            # Delete the roles
            for role in number_roles:
                await role.delete()

            await ctx.send(f"Deleted roles: {', '.join(role.name for role in number_roles)}")
        else:
            await ctx.send("No roles found that are only composed of numbers.")

    @commands.command(help="Developer Only Commands.")
    async def devtest(self, ctx):
        if ctx.author.id == 895788406347558922:
            raise Exception("This is a test error!")
        else:
            await ctx.send("Invaild Command. Type l!commandz for a list of commands.")
    
    @commands.command(help="Developer Only Commands.")
    async def notes(self, ctx):
        if ctx.author.id == 1019465100681285707:
            await ctx.send("Notes : Dont update 'datetime' | Reason : DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC). \n current_time = datetime.datetime.utcnow()")



def setup(bot):
    bot.add_cog(Development(bot))