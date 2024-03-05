from nextcord.ext import commands
import nextcord
import requests
import json
class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Utilites Cog Status : ✅")

    def load_config(self):
        try:
            with open('config.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_config(self, config):
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)

    @commands.command(name='set_welcome', help="Set up a welcomer for new members joining the server.")
    async def set_welcome(self, ctx, channel: nextcord.TextChannel):
        config = self.load_config()
        config[str(ctx.guild.id)] = {'welcome_channel': channel.id}
        self.save_config(config)
        await ctx.send(f'Welcome channel set to {channel.mention} for this server.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = self.load_config()
        guild_id = str(member.guild.id)

        if guild_id in config and 'welcome_channel' in config[guild_id]:
            welcome_channel_id = config[guild_id]['welcome_channel']
            welcome_channel = member.guild.get_channel(welcome_channel_id)

            if welcome_channel:
                emb = nextcord.Embed(
                    title=f"Welcome To {member.guild.name}",
                    description=f"{member.mention} We Hope You Enjoy Your Stay!"
                )
                emb.set_footer(text="© Project Light Productions | Enjoy Your Stay!")

                emb.set_thumbnail(url=member.avatar.url)
                await welcome_channel.send(embed=emb)
                await member.send(f"Enjoy Your Stay {member.mention}!")


    @commands.command(help=" Get a link to the support server.")
    async def support(self, ctx):
        await ctx.send("Need Help? Check out Our Support Server! [Click Me](https://discord.gg/NePhbtMDe9)")



    @commands.command(help="Create a poll for users to vote on. \n ~poll [Question] [answer1] [answer2]")
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, question, option1, option2):
        emb = nextcord.Embed(
            title=f"{question}",
            description=" "
            )
        emb.add_field(name=f"{option1} ", value=":one:")
        emb.add_field(name=f"{option2} ", value=":two:")
        stfu = await ctx.send(embed=emb)
        await stfu.add_reaction("1️⃣")
        await stfu.add_reaction("2️⃣")


    @commands.command(name='old', help="View Old Project Light Versions \n Only in our Official Server! dsc.gg/projectlight")
    async def old_command(self, ctx):
        if ctx.guild.id == 1122248853140291644:
            # Create and send an embed
            embed2 = nextcord.Embed(
                title='Old Project Light Versions',
                description='Download [V2](https://www.mediafire.com/file/0kb6y0ejqhimuvl/Project-Light-V2.mcpack/file) Or [V1](https://cdn.discordapp.com/attachments/979270162773581844/1110627922387157072/Light-Client-MCPE-1.19.mcpack)',
                color=nextcord.Color.green()
            )
            await ctx.send(embed=embed2)
            return
        # Check if the server ID matches the specified value
        if ctx.guild.id == 938248183878930514:
            # Create and send an embed
            embed = nextcord.Embed(
                title='Old Project Light Versions',
                description='Download [V2](https://www.mediafire.com/file/0kb6y0ejqhimuvl/Project-Light-V2.mcpack/file) Or [V1](https://cdn.discordapp.com/attachments/979270162773581844/1110627922387157072/Light-Client-MCPE-1.19.mcpack)',
                color=nextcord.Color.green()
            )
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send('This command is only available in a specific server.')



    
    
    @commands.command(name="pfp", aliases=["avatar", "icon"], help="Get the profile picture of a specified user.")
    async def avatarcmd(self, ctx, user: nextcord.Member):
        emb = nextcord.Embed(
            title=f"{user.name}'s profile Picture ",
            description=" ",
            color=nextcord.Color.teal()
        )
        emb.set_image(url=user.avatar.url)
        await ctx.send(embed=emb)
    @commands.command(name="membercount", aliases=["mc", "mem"], help="Display the current member count of the server. \n ~mc")
    async def membercountcmd(self, ctx):
        emv = nextcord.Embed(
            title="Member Count",
            description=f"{ctx.guild.member_count} Members in {ctx.guild.name}",
            color=nextcord.Color.blue()
        )
        await ctx.send(embed=emv)
    
    @commands.command(name="sinfo", aliases=["guildinfo", "ginfo", "serverinfo"], help="Display information about the server.")
    async def serverinfocmd(self, ctx):
        szz = ctx.guild.created_at
        emb = nextcord.Embed(
            title=ctx.guild.name,
            color=nextcord.Color.og_blurple(),
            description=f"Guild ID: {ctx.guild.id} \n Server Owner: {ctx.guild.owner.display_name} \n Member Count: {ctx.guild.member_count}"
        )
        emb.set_thumbnail(url=ctx.guild.icon.url)
        emb.add_field(name="Created At:", value=szz.strftime("%Y-%m-%d"))
        emb.set_footer(text="© jqm1e / Binary Bit Lab | 2023")

        await ctx.send(embed=emb)

    @commands.command(help="Display information about the bot.")
    async def about(self, ctx):
        me = nextcord.Embed(
            title="About Light Bot - Public",
            description=" "
        )
        ser=len(self.bot.guilds)
        me.add_field(name=f"Im Currently In ", value=f"{ser} Servers")
        me.add_field(name="Developed By ", value=".wuid And _samy123")
        me.set_footer(text="Hello, World And Love From Python / Nextcord!")
        await ctx.send(embed=me)


    @commands.command(help="Display information about servers Via Their ID's")
    async def info(self, ctx, guildid: int):
        aol = self.bot.get_guild(guildid)
        if aol is None:
            await ctx.send("Invaild Guild.")
        else:
            nsfw = aol.nsfw_level.name.replace("NSFWLevel.", "").replace("_", " ").capitalize()
            nsfw = "Default" if nsfw == "Default" else nsfw
            avam = aol.premium_tier
            if aol.icon:
                server_icon = aol.icon.url
            else:
                server_icon = "https://media.discordapp.net/attachments/1171661204494757929/1171886290359300116/image.png?ex=655e4f28&is=654bda28&hm=d952a0a2989b899aba7b4dda07c2827ea41f35c05ec2632c950fa027fb04ceea&="
            em = nextcord.Embed(
                title=f":bulb: Info About {aol.name}",
                description=" ",
                color=0xFFA500
            )
            szz = aol.created_at
            em.add_field(name="Guild ID : ", value=guildid)
            em.add_field(name="Server Owner <:light_crown:1171887250003464332> : ", value=aol.owner.name)
            em.add_field(name="Member Count <:light_members:1171716862078369803> : ", value=aol.member_count)
            em.add_field(name="Created At : ", value=szz.strftime("%Y-%m-%d"))
            em.add_field(name="Boost Level : ", value=avam)
            em.add_field(name="NSFW : ", value=nsfw)
            em.set_thumbnail(url=server_icon)
            em.set_footer(text="© Project Light Productions | dsc.gg/projectlight")

            await ctx.send(embed=em)
    @commands.command(help="Check the bot's latency. ")
    async def ping(self, ctx):
        latency = self.bot.latency * 1000  
        await ctx.send(f'Pong! Latency is {latency:.2f}ms')


def setup(bot):
    bot.add_cog(Util(bot))