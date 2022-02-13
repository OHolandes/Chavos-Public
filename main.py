import discord
import asyncio
from datetime import datetime

__token__ = "TOKEN AQUI"

client = discord.Client()

procurados = {}


async def tic_tac(usuario, limit=600, *, message=None):
    while True:
        if limit <= 0:
            procurados.pop(usuario)
            rol = discord.utils.get(message.guild.roles, name="Avisado")
            await usuario.remove_roles(rol)
            print(f"Usuário desculpado:{usuario.display_name}")
            break
        procurados[usuario] = limit
        await asyncio.sleep(1)
        limit -= 1


@client.event
async def on_ready():
    print("Vigiarei com perfeição!")
    print(f"{client.user.id:.^30}")


@client.event
async def on_message(msg: discord.Message):
    if len(msg.content) > 400:
        if msg.author in procurados:
            await msg.channel.send("Ok eu avisei...")
            rol = discord.utils.get(msg.guild.roles, name="Avisado")
            await msg.author.add_roles(rol)
            print(f"Usuário de castigo:{msg.author.display_name} às {datetime.now():%H:%M}")
        else:
            await msg.channel.send(
                "Você quer mandar uma mensagem ou um livro?, escreva pouco, '_calado você é um poéta_'."
                " Te darei __10 minutos__ para você pensar sobre isso, se insistir te deixarei de **castigo**."
            )
            procurados[msg.author] = tic_tac(msg.author, message=msg)


client.run(__token__)
