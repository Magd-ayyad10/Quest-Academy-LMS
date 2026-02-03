-- =====================================================
-- Gamified LMS Database Schema
-- RPG-Themed Learning Management System
-- PostgreSQL Compatible (pgAdmin 4)
-- =====================================================

-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS user_progress CASCADE;
DROP TABLE IF EXISTS monsters CASCADE;
DROP TABLE IF EXISTS quests CASCADE;
DROP TABLE IF EXISTS zones CASCADE;
DROP TABLE IF EXISTS worlds CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =====================================================
-- USERS TABLE (The Heroes)
-- =====================================================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    
    -- RPG Stats
    level INT NOT NULL DEFAULT 1,
    current_xp INT NOT NULL DEFAULT 0,
    hp_current INT NOT NULL DEFAULT 100,
    hp_max INT NOT NULL DEFAULT 100,
    gold INT NOT NULL DEFAULT 0,
    avatar_class VARCHAR(50) NOT NULL DEFAULT 'Novice',
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- WORLDS TABLE (The Courses)
-- =====================================================
CREATE TABLE worlds (
    world_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(50) NOT NULL DEFAULT 'Easy',
    theme_prompt TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ZONES TABLE (The Modules)
-- Many-to-One relationship with Worlds
-- =====================================================
CREATE TABLE zones (
    zone_id SERIAL PRIMARY KEY,
    world_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    order_index INT NOT NULL DEFAULT 0,
    is_locked BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_zones_world
        FOREIGN KEY (world_id)
        REFERENCES worlds(world_id)
        ON DELETE CASCADE
);

-- =====================================================
-- QUESTS TABLE (The Lessons)
-- Many-to-One relationship with Zones
-- =====================================================
CREATE TABLE quests (
    quest_id SERIAL PRIMARY KEY,
    zone_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content_url TEXT,
    xp_reward INT NOT NULL DEFAULT 0,
    gold_reward INT NOT NULL DEFAULT 0,
    ai_narrative_prompt TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_quests_zone
        FOREIGN KEY (zone_id)
        REFERENCES zones(zone_id)
        ON DELETE CASCADE
);

-- =====================================================
-- MONSTERS TABLE (The Quizzes)
-- Many-to-One relationship with Quests
-- =====================================================
CREATE TABLE monsters (
    monster_id SERIAL PRIMARY KEY,
    quest_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_options TEXT[] NOT NULL,
    damage_per_wrong_answer INT NOT NULL DEFAULT 10,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_monsters_quest
        FOREIGN KEY (quest_id)
        REFERENCES quests(quest_id)
        ON DELETE CASCADE
);

-- =====================================================
-- USER_PROGRESS TABLE (The Save File)
-- Links Users and Quests
-- =====================================================
CREATE TABLE user_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    quest_id INT NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    score INT DEFAULT 0,
    completed_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_progress_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_progress_quest
        FOREIGN KEY (quest_id)
        REFERENCES quests(quest_id)
        ON DELETE CASCADE,
    
    -- Unique constraint to prevent duplicate progress entries
    CONSTRAINT uq_user_quest_progress
        UNIQUE (user_id, quest_id)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================
CREATE INDEX idx_zones_world_id ON zones(world_id);
CREATE INDEX idx_quests_zone_id ON quests(zone_id);
CREATE INDEX idx_monsters_quest_id ON monsters(quest_id);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_quest_id ON user_progress(quest_id);

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================
COMMENT ON TABLE users IS 'The Heroes - Player accounts with RPG stats';
COMMENT ON TABLE worlds IS 'The Courses - Learning worlds to explore';
COMMENT ON TABLE zones IS 'The Modules - Areas within each world';
COMMENT ON TABLE quests IS 'The Lessons - Individual learning tasks';
COMMENT ON TABLE monsters IS 'The Quizzes - Challenges to defeat';
COMMENT ON TABLE user_progress IS 'The Save File - Tracks player progress through quests';
