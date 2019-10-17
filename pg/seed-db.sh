#!/bin/bash

export PGPASSWORD=password;
psql --host=127.0.0.1 --port=5433 --dbname=postgres --username=admin << EOF

DROP TABLE IF EXISTS reminders;

CREATE TABLE reminders(
id SERIAL PRIMARY KEY,
fb_id bigint UNIQUE NOT NULL,
leetcode_username VARCHAR (255),
daily_goal smallint,
reminder_time TIMESTAMP,
created TIMESTAMP DEFAULT now() NOT NULL,
modified TIMESTAMP DEFAULT now() NOT NULL
);

EOF

echo "Database has been seeded."
