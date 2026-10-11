"""Пользователи и роли."""
import sqlite3
from config import DB_PATH


def get_user_by_login(login):
    """
    Ищет пользователя по логину.

    :param login: логин
    :return: кортеж (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row


def get_all_users():
    """
    Список всех пользователей (для админ-панели).

    :return: список кортежей (id, ФИО, логин, роль)
    """
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id,
               Пользователь.фамилия || ' ' || Пользователь.имя || ' ' ||
               IFNULL(Пользователь.отчество, ''),
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        ORDER BY Роль.id DESC, Пользователь.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_fio(user):
    """
    ФИО пользователя одной строкой.

    :param user: кортеж из get_user_by_login
    :return: «Фамилия Имя Отчество»
    """
    return f"{user[1]} {user[2]} {user[3] or ''}".strip()
