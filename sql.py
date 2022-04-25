from numbers import Number
import sqlite3
from typing import List, AnyStr


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
    cur.execute(f"SELECT * FROM wasteds WHERE id={_id}")
    data = cur.fetchall()
    conn.close()
    return data[0]

def sub_time(_id:int, t:int) -> None:
    conn = sqlite3.connect("chavo.db")
    cur = conn.cursor()
    # cur.execute(f"SELECT seconds FROM wasteds WHERE id={_id}")
    # last_time = cur.fetchall()[0]
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
    _del_wasted(931235385902776371)
