-- Пара 22. Состав заказа: один заказ → много позиций.
-- Таблица Заказ теперь хранит только номер, дату и клиента,
-- товары и количество переезжают в Состав_заказа.
-- Запуск: sqlite3 db_sklad18_N.db < migration_22_sostav_zakaza.sql

PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE IF NOT EXISTS Состав_заказа (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- Идентификатор позиции
    заказ_id    INTEGER NOT NULL,                   -- Ссылка на заказ
    товар_id    INTEGER NOT NULL,                   -- Ссылка на товар
    размер      INTEGER,                            -- Размер (если есть)
    количество  INTEGER NOT NULL,                   -- Количество единиц
    цена        REAL    NOT NULL,                   -- Цена за единицу на момент заказа
    FOREIGN KEY (заказ_id) REFERENCES Заказ(id) ON DELETE CASCADE,
    FOREIGN KEY (товар_id) REFERENCES Товар(id)
);

-- Старые заказы (одна позиция в каждом) переносим в состав
INSERT INTO Состав_заказа (заказ_id, товар_id, размер, количество, цена)
SELECT Заказ.id, Заказ.товар_id, NULL, Заказ.количество, Товар.цена
FROM Заказ
JOIN Товар ON Заказ.товар_id = Товар.id;

-- Пересоздаём Заказ без товар_id и количество
CREATE TABLE Заказ_новый (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,      -- Номер заказа
    дата    TEXT    NOT NULL,                       -- Дата оформления (YYYY-MM-DD)
    клиент  TEXT    NOT NULL                        -- ФИО клиента
);

INSERT INTO Заказ_новый (id, дата, клиент)
SELECT id, дата, клиент FROM Заказ;

DROP TABLE Заказ;
ALTER TABLE Заказ_новый RENAME TO Заказ;

COMMIT;
PRAGMA foreign_keys = ON;
