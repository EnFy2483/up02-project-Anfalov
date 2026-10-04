SELECT название, цена FROM Товар ORDER BY цена DESC LIMIT 1;

SELECT название, цена FROM Товар ORDER BY цена ASC LIMIT 1;

SELECT название, цена FROM Товар WHERE категория = 'Электроника';

SELECT * FROM Товар WHERE название LIKE '%о%';

SELECT * FROM Заказ WHERE клиент = 'Иванов Иван Иванович';

FROM Заказ JOIN Товар ON Заказ.товар_id = Товар.id;

SELECT SUM(Товар.цена * Заказ.количество) AS итого_сумма
FROM Заказ
    JOIN Товар ON Заказ.товар_id = Товар.id;

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