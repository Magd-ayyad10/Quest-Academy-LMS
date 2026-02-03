-- =====================================================
-- Gamified LMS Database Schema Update
-- Adding Teachers (Guild Masters) & Assignments (Bounties)
-- PostgreSQL Compatible (pgAdmin 4)
-- =====================================================

-- =====================================================
-- TEACHERS TABLE (The Guild Masters)
-- =====================================================
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    bio TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- UPDATE WORLDS TABLE
-- Add Foreign Key to link Worlds to Teachers
-- =====================================================
ALTER TABLE worlds
    ADD COLUMN teacher_id INT;

ALTER TABLE worlds
    ADD CONSTRAINT fk_worlds_teacher
        FOREIGN KEY (teacher_id)
        REFERENCES teachers(teacher_id)
        ON DELETE CASCADE;

-- Index for performance
CREATE INDEX idx_worlds_teacher_id ON worlds(teacher_id);

-- =====================================================
-- ASSIGNMENTS TABLE (The Bounties)
-- Manual tasks linked to Quests
-- Many-to-One relationship with Quests
-- =====================================================
CREATE TABLE assignments (
    assignment_id SERIAL PRIMARY KEY,
    quest_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    max_score INT NOT NULL DEFAULT 100,
    xp_reward INT NOT NULL DEFAULT 0,
    gold_reward INT NOT NULL DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_assignments_quest
        FOREIGN KEY (quest_id)
        REFERENCES quests(quest_id)
        ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX idx_assignments_quest_id ON assignments(quest_id);

-- =====================================================
-- SUBMISSION STATUS ENUM TYPE
-- =====================================================
CREATE TYPE submission_status AS ENUM ('pending', 'approved', 'rejected');

-- =====================================================
-- SUBMISSIONS TABLE (The Contract Fulfillment)
-- Links Assignments and Users
-- =====================================================
CREATE TABLE submissions (
    submission_id SERIAL PRIMARY KEY,
    assignment_id INT NOT NULL,
    user_id INT NOT NULL,
    submission_url TEXT,
    submission_text TEXT,
    status submission_status NOT NULL DEFAULT 'pending',
    teacher_feedback TEXT,
    grade_awarded INT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_submissions_assignment
        FOREIGN KEY (assignment_id)
        REFERENCES assignments(assignment_id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_submissions_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    
    -- Prevent duplicate submissions for same assignment by same user
    CONSTRAINT uq_user_assignment_submission
        UNIQUE (user_id, assignment_id)
);

-- Indexes for performance
CREATE INDEX idx_submissions_assignment_id ON submissions(assignment_id);
CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_status ON submissions(status);

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================
COMMENT ON TABLE teachers IS 'The Guild Masters - Instructors who create and manage Worlds';
COMMENT ON TABLE assignments IS 'The Bounties - Manual tasks that require submission and grading';
COMMENT ON TABLE submissions IS 'The Contract Fulfillment - Student submissions for assignments';
COMMENT ON COLUMN worlds.teacher_id IS 'The Guild Master who owns this World';
