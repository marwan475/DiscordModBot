import discord
from discord.ext import commands
from discord.utils import get

TOKEN = ""

whitelist = ["twisted", "Akz", "Rami", "Darren Hawkins"]

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

kicking = []

voted = []

count = 0


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def Vkick(ctx, member: discord.Member):
    if len(kicking) > 0:
        await ctx.channel.send("Wait for current vote kick to finish")
    else:
        kicking.append(member)
        await ctx.channel.send(f"Vote kick called on {str(member)} 4 votes needed to kick use !vote to vote")


@client.command()
async def vote(ctx, member: discord.Member):
    global count
    if ctx.author in voted:
        await ctx.channel.send("You Already voted!")
    else:
        count += 1
        await ctx.channel.send(f"{ctx.author} Voted to Kick")
        voted.append(ctx.author)
        if count >= 4:
            await ctx.channel.send(f"Max Votes reached for {str(member)} use !final to kick")


@client.command()
async def final(ctx, member: discord.Member):
    global count
    if member in kicking and count >= 4:
        kicking.clear()
        voted.clear()
        count = count - count
        try:
            await member.kick(reason="Vote Kick")
            await ctx.channel.send(f"{str(member)} has been kicked")
        except:
            await ctx.channel.send("Unable To Kick")
    else:
        await ctx.channel.send("Note enough votes to kick yet canceling vote")
        count = count - count
        kicking.clear()
        voted.clear()


@client.command()
async def mute(ctx, member: discord.Member):
    user = str(ctx.author).split("#")[0]
    channel = str(ctx.channel.name)
    muteRole = ctx.guild.get_role(936883976369475584)
    if channel == "bot-commands":
        if user in whitelist and channel == "bot-commands":
            await member.edit(roles=[muteRole])
            await ctx.send(str(member) + ' has been muted!')
        else:
            await ctx.channel.send(f"{ctx.author}, You dont have permission to do that ")


@client.command()
async def kick(ctx, member: discord.Member, *, why=None):
    user = str(ctx.author).split("#")[0]
    channel = str(ctx.channel.name)
    if channel == "bot-commands":
        if user in whitelist and channel == "bot-commands":
            await member.kick(reason=why)
            await ctx.channel.send(f"**{member} has been kicked from this server by {ctx.author}**")
        else:
            await ctx.channel.send(f"{ctx.author}, You dont have permission to do that ")


@client.command()
async def update(ctx, member: discord.Member):
    user = str(ctx.author).split("#")[0]
    channel = str(ctx.channel.name)
    muteRole = ctx.guild.get_role(696537427786858556)
    if channel == "bot-commands":
        if user in whitelist and channel == "bot-commands":
            await member.edit(roles=[muteRole])
            await ctx.send(str(member) + ' has been Upgraded to Causal!')
        else:
            await ctx.channel.send(f"{ctx.author}, You dont have permission to do that ")


@client.event
async def on_message(msg):
    user = str(msg.author).split("#")[0]
    user_msg = str(msg.content)
    channel = str(msg.channel.name)
    print(f'{user} : {user_msg} ({channel})')

    if msg.author == client.user:
        return

    if channel == "new-members" and user_msg == "":
        member = msg.author
        role = get(msg.guild.roles, name="Guests")
        await member.add_roles(role, atomic=True)
        await msg.channel.send(f"Welcome {user} You have been upgraded to Guests")

    if channel == "bot-commands":
        if "!add" in user_msg and user in whitelist:
            added = user_msg.split(",")[1]
            whitelist.append(added)
            await msg.channel.send(f"{added} was temp added to white list (Resets on reboot)")
            print(whitelist)

    await client.process_commands(msg)


client.run(TOKEN)
