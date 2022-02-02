import discord

__token__ = "TOKEN AQUI"

client = discord.Client()


@client.event
async def on_ready():
    print("Vigiarei com perfeição!")
    print(f"{client.user.id:.^30}")


@client.event
async def on_message(msg):
    pass

client.run(__token__)
