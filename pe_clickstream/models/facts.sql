
WITH events AS (
    SELECT
        inserted_time::date AS web_server_day,
        clickstream_data ->> 'user_id' AS user_id,
        clickstream_data ->> 'event_name' AS event_name
    FROM web_events
)

SELECT *
FROM events
