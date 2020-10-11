# kafka-webinar-2020-10
В этом репозитории лежит код, необходимый для воспроизведения практического примера вебинара по Managed Solution for Apache Kafka в Яндекс Облаке.

Далее будут описаны основные шаги примера:

- Создаем кластер Apache Kafka в одоной зоне доступности с одним брокером
- Создаем топик в кластере (в нашем примере *test-topic*)
- Создаем двух пользователей, один с правами consumer, другой - producer в топике, полученном на предыдущем шаге
- Создаем инстанс в той же подсети что и ваш кластер, код для работы с kafka, будем запускать оттуда
- Проверяем подключение к кластеру при помощи kafkacat или удобного для вас языка программирования
- Наполняем топик тестовыми данными (файл *generate.py*)
- Создаем кластер ClickHouse в той же подсети что и кластер Apache Kafka. В настройках необходимо указать настройки для подключения к Kafka
```
Sasl mechanism: SCRAM-SHA-512
Sasl username: consumer
Sasl password: <consumer-password>
Security protocol: SASL_PLAINTEXT
```
- Создадим таблицы для получения данных из Apache Kafka в ClickHouse (файл ingestion.sql)
- Убедимся, что данные есть в ClickHouse при помощи SQL консоли кластера:
```
SELECT
   geo,
   count() * 100 / ( SELECT count() from db1.events ) as percent_to_total
FROM db1.events
GROUP BY geo;
```
- Создадим кластер PostgreSQL со стандартными настройками в подсети с уже созданными кластерами.
- Создадим там таблицу пользователей с данными (файл users.sql)
- Подключим словарь с данными из PostgreSQL, указав хост, базы данных и пользователя. Также необходимо указать колонки, которые мы будем использовать в ClickHouse и идентификатор, по которому осуществляется поиск.
- Проверим, что мы можем сделать запрос, используя данные из словаря:
```
SELECT
   geo,
   dictGet('pgusers', 'gender', toUInt64(user_id)) as gender,
   count(*)
FROM db1.events
GROUP BY geo, dictGet('pgusers', 'gender', toUInt64(user_id));
```
