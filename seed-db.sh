#!/bin/bash

export PGPASSWORD=password;
psql --host=127.0.0.1 --port=5433 --dbname=postgres --username=admin << EOF

CREATE TABLE reminders(
id SERIAL PRIMARY KEY,
fb_id VARCHAR (255) UNIQUE NOT NULL,
leetcode_username VARCHAR (255) UNIQUE NOT NULL,
trigger TIMESTAMP NOT NULL,
created TIMESTAMP DEFAULT now() NOT NULL,
modified TIMESTAMP DEFAULT now() NOT NULL
);

EOF

echo "Database has been seeded."
