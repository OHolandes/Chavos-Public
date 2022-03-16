from numbers import Number
import sqlite3
from typing import List, AnyStr


def add_serv(_id, *roles) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO servers (id, id_roles) VALUES ({_id}, '{','.join(roles)}')"
        )
    conn.commit()
    conn.close()

def change_rols(_id, *roles) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(f"UPDATE servers SET id_roles='{','.join(roles)}' WHERE id={_id}")
    conn.commit()
    conn.close()

def _del_serv(_id) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM servers WHERE id={_id}")
    conn.commit()
    conn.close()

def get_roles(_id:int) -> List[AnyStr]:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(f"SELECT id_roles FROM servers WHERE id={_id}")
    roles = cur.fetchall()[0]
    conn.close()
    parse_int = [int(rol) for rol in roles[0].split(",")]
    return parse_int

def wasted(name:str, _id:int, t:int) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO wasteds (name, id, seconds) VALUES ('{name}', {_id}, {t})"
        )
    conn.commit()
    conn.close()

def get_wasteds(_id: int):
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM wasteds WHERE id={_id}")
    data = cur.fetchall()
    conn.close()
    return data[0]

def sub_time(_id:int, t:int) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute("SELECT seconds FROM wasteds WHERE id={_id}")
    last_time = cur.fetchall()[0]
    cur.execute(f"UPDATE wasteds SET seconds={t} WHERE id={_id}")
    conn.commit()
    conn.close()

def _del_wasted(_id) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM wasteds WHERE id={_id}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    serv = 386268259391111178
    print(get_roles(serv))

# &add 731333773781762139 481600846908358673 938556302383276053 441290194482888734 764623161203359825 438748528228171790