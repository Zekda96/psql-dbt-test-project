CREATE TABLE web_events (
    id SERIAL PRIMARY KEY,
    clickstream_data JSONB,
    inserted_time TIMESTAMPTZ DEFAULT Now()
)
;