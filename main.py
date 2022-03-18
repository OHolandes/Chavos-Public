import asyncio
from datetime import datetime
import json

import discord

from segredin import __token__
import sql



client = discord.Client()


async def tic_tac(usuario, limit=1800, *, message=None):
    while limit >= 0:
        sql.sub_time(usuario.id, limit)
        await asyncio.sleep(1)
        limit -= 1
    sql._del_wasted(usuario.id)
    rol = discord.utils.get(message.guild.roles, name="Avisado")
    await usuario.remove_roles(rol)
    print(f"Usuário desculpado:{usuario.display_name}")  


@client.event
async def on_ready():
    print("Vigiarei com perfeição!")
    print(f"{client.user.id:.^30}")


@client.event
async def on_message(msg: discord.Message):
    ID_SERV = msg.guild.id
    if msg.content.startswith("&"):
        cmd = msg.content.split()
        roles = cmd[1:]
        if "add" in cmd[0]:
            try:
                # roles = map(lambda ids: int(ids), roles)
                sql.add_serv(ID_SERV, *roles)
            except Exception as error:
                print(error)
                await msg.channel.send("Um erro ocorreu...")
            else:
                await msg.channel.send("Cargos adicionados!")

        elif "show" in cmd[0]:
            try:
                sql.get_roles(ID_SERV)
            except Exception as error:
                print(error)
                await msg.channel.send("Um erro ocorreu...")
            else:
                temp_roles = [rol for rol in map(lambda ids: int(ids), 
                                                    sql.get_roles(ID_SERV)
                                                )]
                repr_roles = repr(temp_roles)
                embedshow = discord.Embed(
                    title="IDs dos cargos que não seram barrados",
                    description=temp_roles,
                    Colour=discord.Colour.green()
                    )
                await msg.channel.send(embed=embedshow)

        elif "change" in cmd[0]:
            try:
                sql.change_rols(ID_SERV, *roles)
            except Exception as error:
                print(error)
                await msg.channel.send("Um erro ocorreu...")
            else:
                await msg.channel.send("Cargos modificados!")
        
        elif "del" in cmd[0]:
            try:
                sql._del_serv(ID_SERV)
            except Exception as error:
                print(error)
                await msg.channel.send("Um erro ocorreu...")
            else:
                await msg.channel.send("Seu servidor parou de ser vigiado...")

        elif "help" in cmd[0]:
            text = """
                    **&add**: Adiciono IDs de cargos para não serem ||vigiados||.
                    **&change**: Trocos os cargos.
                    **&show**: Mostro os IDs salvos neste servidor.
                    **&del**: Apago seu servidor do meu relatório
                    **&help**: Exibo essa mensagem.

                    Separe um cargo nomeado "**Avisado**" para eu dar carteiradas.
                    Para adicionar ponha os IDs dos cargos em sequência:
                    `&add 0000000000 00000000000 0000000000 00000000000`
                    """
            embedhelp = discord.Embed(title="Comandos:", 
                                            description=text,
                                            color=discord.Colour.gold())
            await msg.channel.send(embed=embedhelp)
        else:
            return

    elif len(msg.content) > 300:
        ID_USER = msg.author.id
        for rol in msg.author.roles:
            if not rol.id in sql.get_roles(ID_SERV):
                if ID_USER in sql.get_wasteds(ID_USER):
                    await msg.channel.send("Ok eu avisei...")
                    rol = discord.utils.get(msg.guild.roles, name="Avisado")
                    await msg.author.add_roles(rol)
                    print(f"Usuário de castigo:{msg.author.display_name} às {datetime.now():%H:%M}")
                else:
                    await msg.channel.send(
                        "Você quer mandar uma mensagem ou um livro?, escreva pouco, '_calado você é um poéta_'."
                        " Na próxima te deixarei de **castigo** por **__30__ minutos** para você pensar sobre isso."
                    )
                    tic_tac(msg.author, message=msg)
    else:
        return


if __name__ == "__main__":
    client.run(__token__)
