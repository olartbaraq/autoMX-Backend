-- Drop tables if they exist
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "media" CASCADE;

-- Create "user" table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create "media" table
CREATE TABLE "media" (
    id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL,
    song_name TEXT NOT NULL,
    movie_name TEXT NOT NULL,
    ai_prompt TEXT NOT NULL
);