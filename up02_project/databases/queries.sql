SELECT название, цена FROM Товар ORDER BY цена DESC LIMIT 1;

SELECT название, цена FROM Товар ORDER BY цена ASC LIMIT 1;

SELECT название, цена FROM Товар WHERE категория = 'Электроника';

SELECT * FROM Товар WHERE название LIKE '%о%';

SELECT * FROM Заказ WHERE клиент = 'Иванов Иван Иванович';

SELECT Заказ.id, Заказ.дата, Заказ.клиент, Товар.название, Состав_заказа.количество
FROM Заказ
    JOIN Состав_заказа ON Заказ.id = Состав_заказа.заказ_id
    JOIN Товар ON Состав_заказа.товар_id = Товар.id;

SELECT SUM(Состав_заказа.цена * Состав_заказа.количество) AS итого_сумма
FROM Состав_заказа;

SELECT клиент, COUNT(*) AS количество_заказов
FROM Заказ
GROUP BY
    клиент;

SELECT название, цена, количество
FROM Товар
WHERE
    цена > 1000
    AND количество > 0
ORDER BY цена DESC;
