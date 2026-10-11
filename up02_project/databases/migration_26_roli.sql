-- Пара 26. Роли и пользователи.
-- Было: Пользователь (id, логин, фио, роль TEXT).
-- Стало: Роль (id, название) + Пользователь (фамилия, имя, отчество, логин, роль_id).
-- Запуск: sqlite3 db_sklad18_N.db < migration_26_roli.sql

PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE IF NOT EXISTS Роль (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- Идентификатор роли
    название    TEXT    NOT NULL UNIQUE             -- Клиент / Менеджер / Администратор
);

INSERT INTO Роль (название) VALUES ('Клиент');
INSERT INTO Роль (название) VALUES ('Менеджер');
INSERT INTO Роль (название) VALUES ('Администратор');

CREATE TABLE Пользователь_новый (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- Идентификатор пользователя
    фамилия     TEXT    NOT NULL,
    имя         TEXT    NOT NULL,
    отчество    TEXT,
    логин       TEXT    NOT NULL UNIQUE,            -- Логин для входа (без пароля)
    роль_id     INTEGER NOT NULL,                   -- Ссылка на роль
    FOREIGN KEY (роль_id) REFERENCES Роль(id)
);

-- Переносим старых пользователей: «Фамилия Имя Отчество» → три поля
INSERT INTO Пользователь_новый (id, фамилия, имя, отчество, логин, роль_id)
SELECT п.id,
       substr(п.фио, 1, instr(п.фио, ' ') - 1),
       substr(п.остаток, 1, instr(п.остаток || ' ', ' ') - 1),
       nullif(substr(п.остаток, instr(п.остаток || ' ', ' ') + 1), ''),
       п.логин,
       Роль.id
FROM (
    SELECT id, логин, фио, роль,
           substr(фио, instr(фио, ' ') + 1) AS остаток
    FROM Пользователь
) AS п
JOIN Роль ON Роль.название = п.роль;

DROP TABLE Пользователь;
ALTER TABLE Пользователь_новый RENAME TO Пользователь;

-- Тестовые пользователи из рабочей тетради
INSERT INTO Пользователь (фамилия, имя, отчество, логин, роль_id)
VALUES ('Иванов', 'Иван', 'Иванович', 'client1', 1);
INSERT INTO Пользователь (фамилия, имя, отчество, логин, роль_id)
VALUES ('Петров', 'Петр', 'Петрович', 'manager1', 2);
INSERT INTO Пользователь (фамилия, имя, отчество, логин, роль_id)
VALUES ('Сидоров', 'Сидор', 'Сидорович', 'admin1', 3);

COMMIT;
PRAGMA foreign_keys = ON;
