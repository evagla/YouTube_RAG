CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    video_id TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    video_id TEXT NOT NULL,
    chunk_index INT NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.sessions(
    id SERIAL PRIMARY KEY, 
    session_id TEXT NOT NULL, 
    user_message TEXT NOT NULL, 
    assistant_message TEXT NOT NULL, 
    created_at TIMESTAMP default NOW()
);
