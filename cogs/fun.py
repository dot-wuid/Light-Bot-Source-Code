from nextcord.ext import commands
import nextcord
import random
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Fun Cog Status : ✅")

    @commands.command(name='rps', help="Rock, Paper, Scissors.")
    async def rock_paper_scissors(self, ctx, choice):
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)

        # Check if the user's choice is valid
        if choice.lower() not in choices:
            await ctx.send("Invalid choice. Please choose rock, paper, or scissors.")
            return

        # Determine the winner
        result = self.determine_winner(choice.lower(), bot_choice)

        # Send the result
        await ctx.send(f"You chose {choice.capitalize()} and I chose {bot_choice.capitalize()}. {result}!")

    def determine_winner(self, player_choice, bot_choice):
        if player_choice == bot_choice:
            return "It's a tie!"
        elif (
            (player_choice == 'rock' and bot_choice == 'scissors') or
            (player_choice == 'paper' and bot_choice == 'rock') or
            (player_choice == 'scissors' and bot_choice == 'paper')
        ):
            return "You win!"
        else:
            return "I win!"

    @commands.command(name='ur', aliases=['userroulette'], help="Need a Random User? This Should Help!")
    async def user_roulette(self, ctx):
        # Get the list of all members in the server
        members = ctx.guild.members
        
        # Filter out bots and the command invoker
        members = [member for member in members if not member.bot and member != ctx.author]
        
        # Check if there are eligible members
        if members:
            # Select a random member
            selected_member = random.choice(members)
        
            # Ping the selected member
            await ctx.send(f"{ctx.author.mention} has selected {selected_member.mention} for User Roulette!")
        else:
            await ctx.send("Not enough eligible members for User Roulette.")

    @commands.command(name='gtn', help='Guess the Number Game! Try to guess the number.')
    async def guess_the_number(self, ctx):
        # Generate a random number between 1 and 100
        secret_number = random.randint(1, 100)

        await ctx.send("Welcome to Guess the Number Game! I've picked a number between 1 and 100. Try to guess it!")

        attempts = 0

        while True:
            try:
                # Get user's guess
                guess = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit(), timeout=30.0)

                # Increment attempts
                attempts += 1

                # Convert the guess to an integer
                user_guess = int(guess.content)

                # Check if the guess is correct
                if user_guess == secret_number:
                    await ctx.send(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
                    break
                elif user_guess < secret_number:
                    await ctx.send("Too low! Try again.")
                else:
                    await ctx.send("Too high! Try again.")

            except TimeoutError:
                await ctx.send("Time's up! The game is over.")
                break
            except ValueError:
                await ctx.send("Invalid input. Please enter a valid number.")


def setup(bot):
    bot.add_cog(Fun(bot))