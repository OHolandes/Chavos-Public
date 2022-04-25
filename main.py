import asyncio
from datetime import datetime
from random import choice, uniform

import discord

from segredin import __token__
import sql



client = discord.Client()

intents = discord.Intents.default()
intents.messages = True


async def tic_tac(usuario, limit=1800, *, message=None):
    while limit >= 0:
        sql.sub_time(usuario.id, limit)
        await asyncio.sleep(1)
        limit -= 1
    sql._del_wasted(usuario.id)
    rol = discord.utils.get(message.guild.roles, name="Avisado")
    await usuario.remove_roles(rol)
    print(f"Usuário desculpado:{usuario.display_name}")
    await message.channel.send(message.author.mention, "Foram terminados seus anos de cárcere.")


@client.event
async def on_ready():
    print("Vigiarei com perfeição!")
    print(f"{client.user.id:.^30}")


@client.event
async def on_message(msg: discord.Message):
    ID_SERV = msg.guild.id
    if len(msg.content) > 300:
        ID_USER = msg.author.id
        cargos_privilegiados = [555187871498108937, 438748528228171790]
        declaraçoes = [
            "posto na jaula", 
            "aprisionado sem direito a água e comida", 
            "amarrado e jogado morro abaixo",
            "**enjaulado**"
            ]
        if not msg.author.bot:
            cargos_do_meliante = [cracha.id for cracha in msg.author.roles]
            if not cargos_privilegiados in cargos_do_meliante:
                try:
                    sql.get_wasteds(ID_USER)
                except IndexError:
                    await msg.channel.send(
                    f'{msg.author.mention} Você quer mandar uma mensagem ou um livro?, escreva pouco... "_calado você é um poéta_".'
                    ' Na próxima te deixarei de **castigo** por **__30__ minutos** para você pensar sobre isso.'
                    )
                    sql.wasted(msg.author.display_name, ID_USER, 1800)
                else:
                    await msg.channel.send("Ok, eu avisei...")

                    rol = discord.utils.get(msg.guild.roles, name="Avisado")
                    await msg.author.add_roles(rol)

                    carcere = datetime.now()
                    await msg.channel.send(f"{msg.author.mention} foi {choice(declaraçoes)} às {carcere:%H:%M}.")
                    # async with msg.channel.typing():
                    #     type_time = uniform(0.5, 2)
                    #     await asyncio.sleep(type_time)
                    # carcere._minute += 30
                    # await msg.channel.send(
                    #     f"O cumprimento do seu mandado de prisão foi estipulado para {carcere:%H:%M}."
                    # )
                    await tic_tac(msg.author, message=msg)
    else:
        return


if __name__ == "__main__":
    client.run(__token__)
