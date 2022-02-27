import asyncio
from datetime import datetime
import json

import discord

__token__ = "TOKEN AQUI"

client = discord.Client()

procurados = {}
roles_in = json.load(open("cover_up.json")) # id de cargos que nao teram a orelha puxada


async def tic_tac(usuario, limit=600, *, message=None):
    while limit >= 0:
        procurados[usuario] = limit
        await asyncio.sleep(1)
        limit -= 1
    procurados.pop(usuario)
    rol = discord.utils.get(message.guild.roles, name="Avisado")
    await usuario.remove_roles(rol)
    print(f"Usuário desculpado:{usuario.display_name}")  


@client.event
async def on_ready():
    print("Vigiarei com perfeição!")
    print(f"{client.user.id:.^30}")


@client.event
async def on_message(msg: discord.Message):
    ID_SERV = str(msg.guild.id)
    if msg.content.startswith("&"):
        cmd = msg.content.split()
        if "add" in cmd[0]:
            with open("cover_up.json", "w+") as cover_up:
                try:
                    roles_in[ID_SERV] = [int(rol) for rol in cmd[1:]]
                    cover_up.write(json.dumps(roles_in))
                except Exception as error:
                    print(error)
                    await msg.channel.send("Um erro ocorreu...")
                else:
                    await msg.channel.send("Cargos adicionados!")
        elif "show" in cmd[0]:
            with open("cover_up.json") as cover_up:
                try:
                    if roles_in[ID_SERV]:
                        embed = discord.Embed(title="ID dos cargos que não serão barrados:", 
                                                description=f"{roles_in[ID_SERV]}",
                                                color=discord.Colour.dark_red())
                        await msg.channel.send(embed=embed)
                    else:
                        await msg.channel.send("Servidor não encontrado")
                except Exception as error:
                    print(error)
                    await msg.channel.send("Um erro ocorreu...")
        elif "help" in cmd[0]:
            text = """
                    Comandos:
                    **&add**: Adiciono IDs de cargos para não serem ||vigiados||.
                    **&show**: Mostro os IDs salvos neste servidor.
                    **&help**: Exibo essa mensagem.
                    """
            embedhelp = discord.Embed(title="Comandos:", 
                                            description=text,
                                            color=discord.Colour.gold())
            await msg.channel.send(embed=embedhelp)
        else:
            return

    elif len(msg.content) > 300:
        if not msg.author.top_role.id in roles_in[ID_SERV]:
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
    else:
        return

client.run(__token__)
