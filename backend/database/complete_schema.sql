-- =====================================================
-- GAMIFIED LMS - COMPLETE DATABASE SCHEMA
-- RPG-Themed Learning Management System
-- PostgreSQL Compatible (pgAdmin 4)
-- =====================================================

-- =====================================================
-- CLEANUP: Drop existing tables and types
-- =====================================================
DROP TABLE IF EXISTS leaderboard_entries CASCADE;
DROP TABLE IF EXISTS user_achievements CASCADE;
DROP TABLE IF EXISTS achievements CASCADE;
DROP TABLE IF EXISTS user_inventory CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS submissions CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS user_progress CASCADE;
DROP TABLE IF EXISTS monsters CASCADE;
DROP TABLE IF EXISTS quests CASCADE;
DROP TABLE IF EXISTS zones CASCADE;
DROP TABLE IF EXISTS worlds CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

DROP TYPE IF EXISTS submission_status CASCADE;
DROP TYPE IF EXISTS item_type CASCADE;
DROP TYPE IF EXISTS item_rarity CASCADE;
DROP TYPE IF EXISTS achievement_type CASCADE;

-- =====================================================
-- ENUM TYPES
-- =====================================================
CREATE TYPE submission_status AS ENUM ('pending', 'approved', 'rejected');
CREATE TYPE item_type AS ENUM ('weapon', 'armor', 'consumable', 'cosmetic', 'boost');
CREATE TYPE item_rarity AS ENUM ('common', 'uncommon', 'rare', 'epic', 'legendary');
CREATE TYPE achievement_type AS ENUM ('quest', 'combat', 'social', 'collection', 'mastery');

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
    
    -- Profile
    avatar_url TEXT,
    title VARCHAR(100) DEFAULT 'Newcomer',
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TEACHERS TABLE (The Guild Masters)
-- =====================================================
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    bio TEXT,
    specialization VARCHAR(100),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- WORLDS TABLE (The Courses)
-- =====================================================
CREATE TABLE worlds (
    world_id SERIAL PRIMARY KEY,
    teacher_id INT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(50) NOT NULL DEFAULT 'Easy',
    theme_prompt TEXT,
    thumbnail_url TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_worlds_teacher
        FOREIGN KEY (teacher_id)
        REFERENCES teachers(teacher_id)
        ON DELETE CASCADE
);

-- =====================================================
-- ZONES TABLE (The Modules)
-- =====================================================
CREATE TABLE zones (
    zone_id SERIAL PRIMARY KEY,
    world_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INT NOT NULL DEFAULT 0,
    is_locked BOOLEAN NOT NULL DEFAULT TRUE,
    unlock_requirement_xp INT DEFAULT 0,
    
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
-- =====================================================
CREATE TABLE quests (
    quest_id SERIAL PRIMARY KEY,
    zone_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content_url TEXT,
    xp_reward INT NOT NULL DEFAULT 0,
    gold_reward INT NOT NULL DEFAULT 0,
    ai_narrative_prompt TEXT,
    order_index INT DEFAULT 0,
    
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
-- =====================================================
CREATE TABLE monsters (
    monster_id SERIAL PRIMARY KEY,
    quest_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_options TEXT[] NOT NULL,
    damage_per_wrong_answer INT NOT NULL DEFAULT 10,
    monster_hp INT DEFAULT 100,
    monster_image_url TEXT,
    
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
-- ASSIGNMENTS TABLE (The Bounties)
-- =====================================================
CREATE TABLE assignments (
    assignment_id SERIAL PRIMARY KEY,
    quest_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    max_score INT NOT NULL DEFAULT 100,
    xp_reward INT NOT NULL DEFAULT 0,
    gold_reward INT NOT NULL DEFAULT 0,
    due_date TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    CONSTRAINT fk_assignments_quest
        FOREIGN KEY (quest_id)
        REFERENCES quests(quest_id)
        ON DELETE CASCADE
);

-- =====================================================
-- SUBMISSIONS TABLE (The Contract Fulfillment)
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
    graded_at TIMESTAMP,
    
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
    
    -- Unique constraint
    CONSTRAINT uq_user_assignment_submission
        UNIQUE (user_id, assignment_id)
);

-- =====================================================
-- USER_PROGRESS TABLE (The Save File)
-- =====================================================
CREATE TABLE user_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    quest_id INT NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    score INT DEFAULT 0,
    attempts INT DEFAULT 0,
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
    
    -- Unique constraint
    CONSTRAINT uq_user_quest_progress
        UNIQUE (user_id, quest_id)
);

-- =====================================================
-- ITEMS TABLE (The Loot)
-- =====================================================
CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    item_type item_type NOT NULL,
    rarity item_rarity NOT NULL DEFAULT 'common',
    price INT NOT NULL DEFAULT 0,
    
    -- Effects
    hp_bonus INT DEFAULT 0,
    xp_multiplier DECIMAL(3,2) DEFAULT 1.00,
    gold_multiplier DECIMAL(3,2) DEFAULT 1.00,
    
    -- Visual
    icon_url TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USER_INVENTORY TABLE (The Backpack)
-- =====================================================
CREATE TABLE user_inventory (
    inventory_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    is_equipped BOOLEAN DEFAULT FALSE,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_inventory_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_inventory_item
        FOREIGN KEY (item_id)
        REFERENCES items(item_id)
        ON DELETE CASCADE,
    
    -- Unique constraint (one entry per item per user)
    CONSTRAINT uq_user_item
        UNIQUE (user_id, item_id)
);

-- =====================================================
-- ACHIEVEMENTS TABLE (The Trophies)
-- =====================================================
CREATE TABLE achievements (
    achievement_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    achievement_type achievement_type NOT NULL,
    icon_url TEXT,
    
    -- Requirements
    requirement_value INT DEFAULT 1,
    requirement_description TEXT,
    
    -- Rewards
    xp_reward INT DEFAULT 0,
    gold_reward INT DEFAULT 0,
    title_reward VARCHAR(100),
    
    -- Rarity
    rarity item_rarity DEFAULT 'common',
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USER_ACHIEVEMENTS TABLE (The Trophy Case)
-- =====================================================
CREATE TABLE user_achievements (
    user_achievement_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    achievement_id INT NOT NULL,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_user_achievement_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_user_achievement_achievement
        FOREIGN KEY (achievement_id)
        REFERENCES achievements(achievement_id)
        ON DELETE CASCADE,
    
    -- Unique constraint
    CONSTRAINT uq_user_achievement
        UNIQUE (user_id, achievement_id)
);

-- =====================================================
-- LEADERBOARD_ENTRIES TABLE (The Hall of Fame)
-- =====================================================
CREATE TABLE leaderboard_entries (
    entry_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    world_id INT,
    
    -- Scores
    total_xp INT NOT NULL DEFAULT 0,
    total_gold INT NOT NULL DEFAULT 0,
    quests_completed INT NOT NULL DEFAULT 0,
    monsters_defeated INT NOT NULL DEFAULT 0,
    achievements_unlocked INT NOT NULL DEFAULT 0,
    
    -- Ranking
    rank_position INT,
    
    -- Time period (for weekly/monthly boards)
    period_start DATE,
    period_end DATE,
    
    -- Metadata
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_leaderboard_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_leaderboard_world
        FOREIGN KEY (world_id)
        REFERENCES worlds(world_id)
        ON DELETE CASCADE
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================
CREATE INDEX idx_worlds_teacher_id ON worlds(teacher_id);
CREATE INDEX idx_zones_world_id ON zones(world_id);
CREATE INDEX idx_zones_order ON zones(world_id, order_index);
CREATE INDEX idx_quests_zone_id ON quests(zone_id);
CREATE INDEX idx_quests_order ON quests(zone_id, order_index);
CREATE INDEX idx_monsters_quest_id ON monsters(quest_id);
CREATE INDEX idx_assignments_quest_id ON assignments(quest_id);
CREATE INDEX idx_submissions_assignment_id ON submissions(assignment_id);
CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_quest_id ON user_progress(quest_id);
CREATE INDEX idx_user_inventory_user_id ON user_inventory(user_id);
CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX idx_leaderboard_user_id ON leaderboard_entries(user_id);
CREATE INDEX idx_leaderboard_world_id ON leaderboard_entries(world_id);
CREATE INDEX idx_leaderboard_xp ON leaderboard_entries(total_xp DESC);

-- =====================================================
-- TABLE COMMENTS
-- =====================================================
COMMENT ON TABLE users IS 'The Heroes - Player accounts with RPG stats';
COMMENT ON TABLE teachers IS 'The Guild Masters - Instructors who create and manage Worlds';
COMMENT ON TABLE worlds IS 'The Courses - Learning worlds to explore';
COMMENT ON TABLE zones IS 'The Modules - Areas within each world';
COMMENT ON TABLE quests IS 'The Lessons - Individual learning tasks';
COMMENT ON TABLE monsters IS 'The Quizzes - Challenges to defeat with questions';
COMMENT ON TABLE assignments IS 'The Bounties - Manual tasks requiring submission';
COMMENT ON TABLE submissions IS 'The Contract Fulfillment - Student submissions for grading';
COMMENT ON TABLE user_progress IS 'The Save File - Tracks player progress through quests';
COMMENT ON TABLE items IS 'The Loot - Items available in the game shop';
COMMENT ON TABLE user_inventory IS 'The Backpack - Items owned by each player';
COMMENT ON TABLE achievements IS 'The Trophies - Unlockable achievements';
COMMENT ON TABLE user_achievements IS 'The Trophy Case - Achievements earned by players';
COMMENT ON TABLE leaderboard_entries IS 'The Hall of Fame - Player rankings and scores';

-- =====================================================
-- =====================================================
-- SEED DATA
-- =====================================================
-- =====================================================

-- =====================================================
-- SEED: Teachers (Guild Masters)
-- =====================================================
INSERT INTO teachers (username, email, password_hash, bio, specialization) VALUES
('master_aldric', 'aldric@questacademy.edu', '$2b$12$hashedpassword1', 'A wise sage with 20 years of experience in the arcane arts of programming.', 'Backend Sorcery'),
('lady_miranda', 'miranda@questacademy.edu', '$2b$12$hashedpassword2', 'Former adventurer turned teacher, specializing in visual enchantments.', 'Frontend Wizardry'),
('professor_thorne', 'thorne@questacademy.edu', '$2b$12$hashedpassword3', 'Master of data dungeons and keeper of ancient databases.', 'Database Necromancy');

-- =====================================================
-- SEED: Users (Heroes)
-- =====================================================
INSERT INTO users (username, email, password_hash, level, current_xp, hp_current, hp_max, gold, avatar_class, title) VALUES
('shadow_blade', 'shadow@heroes.net', '$2b$12$userpass1', 5, 2500, 100, 100, 350, 'Warrior', 'Quest Seeker'),
('mystic_luna', 'luna@heroes.net', '$2b$12$userpass2', 8, 5200, 95, 120, 890, 'Mage', 'Dragon Slayer'),
('iron_forge', 'forge@heroes.net', '$2b$12$userpass3', 3, 1100, 100, 100, 150, 'Paladin', 'Newcomer'),
('swift_arrow', 'arrow@heroes.net', '$2b$12$userpass4', 12, 9800, 140, 140, 2100, 'Ranger', 'Legendary Scholar'),
('crystal_wave', 'crystal@heroes.net', '$2b$12$userpass5', 1, 0, 100, 100, 0, 'Novice', 'Newcomer');

-- =====================================================
-- SEED: Worlds (Courses)
-- =====================================================
INSERT INTO worlds (teacher_id, title, description, difficulty_level, theme_prompt, is_published) VALUES
(1, 'The Python Caverns', 'Descend into the depths of Python programming, where serpentine code slithers through ancient tunnels.', 'Easy', 'A mysterious underground cave system filled with glowing crystals and ancient Python scripts carved into walls.', TRUE),
(2, 'The JavaScript Jungle', 'Navigate the wild and unpredictable jungle of JavaScript, where async creatures roam free.', 'Medium', 'A lush, vibrant jungle with neon-lit trees representing DOM nodes and callback waterfalls.', TRUE),
(3, 'The SQL Sanctum', 'Enter the sacred halls where data is stored in crystalline tables of immense power.', 'Hard', 'A grand cathedral-like structure made of pure data crystals, with tables floating in mystical chambers.', TRUE),
(1, 'The Git Graveyard', 'Master version control in this haunted repository where lost commits wander eternally.', 'Medium', 'A spooky graveyard where tombstones are commit messages and ghosts are reverted changes.', FALSE);

-- =====================================================
-- SEED: Zones (Modules)
-- =====================================================
INSERT INTO zones (world_id, title, description, order_index, is_locked, unlock_requirement_xp) VALUES
-- Python Caverns Zones
(1, 'The Entrance Hall - Variables', 'Learn the basics of storing magical values in mystical containers.', 1, FALSE, 0),
(1, 'The Loop Labyrinth', 'Master the art of repetition through endless corridors.', 2, TRUE, 100),
(1, 'The Function Forge', 'Craft reusable spells in the ancient forge.', 3, TRUE, 300),
(1, 'The Class Catacombs', 'Discover object-oriented secrets in the deepest chambers.', 4, TRUE, 600),

-- JavaScript Jungle Zones
(2, 'The DOM Thicket', 'Learn to manipulate the living document tree.', 1, FALSE, 0),
(2, 'The Async Swamp', 'Navigate the treacherous waters of asynchronous code.', 2, TRUE, 200),
(2, 'The Framework Forest', 'Explore the diverse ecosystem of JavaScript frameworks.', 3, TRUE, 500),

-- SQL Sanctum Zones
(3, 'The SELECT Shrine', 'Begin your journey by learning to query the sacred tables.', 1, FALSE, 0),
(3, 'The JOIN Junction', 'Master the art of combining data from multiple sources.', 2, TRUE, 250),
(3, 'The Optimization Oracle', 'Seek wisdom in query performance and indexing.', 3, TRUE, 700);

-- =====================================================
-- SEED: Quests (Lessons)
-- =====================================================
INSERT INTO quests (zone_id, title, content_url, xp_reward, gold_reward, ai_narrative_prompt, order_index) VALUES
-- Python Variables Zone
(1, 'The First Incantation', 'https://videos.questacademy.edu/python/variables-intro', 50, 10, 'The hero discovers their first magical variable, a glowing orb that can hold any value.', 1),
(1, 'Types of Magic', 'https://videos.questacademy.edu/python/data-types', 75, 15, 'Different types of magical containers are revealed - strings shimmer with text, integers pulse with numbers.', 2),
(1, 'The String Spell', 'https://videos.questacademy.edu/python/string-methods', 100, 25, 'Learning to manipulate text like a true wordsmith wizard.', 3),

-- Loop Labyrinth Zone
(2, 'The For Loop Path', 'https://videos.questacademy.edu/python/for-loops', 100, 30, 'The hero must traverse the same corridor multiple times, each iteration revealing new secrets.', 1),
(2, 'While Loop Wandering', 'https://videos.questacademy.edu/python/while-loops', 120, 35, 'A corridor that continues until a condition is met - be careful not to loop forever!', 2),

-- DOM Thicket Zone
(5, 'Selecting Elements', 'https://videos.questacademy.edu/js/dom-selectors', 80, 20, 'The hero learns to identify and grab elements from the living document tree.', 1),
(5, 'Event Listeners', 'https://videos.questacademy.edu/js/events', 100, 30, 'Setting magical traps that trigger when users interact with the page.', 2),

-- SQL SELECT Shrine Zone
(8, 'Your First Query', 'https://videos.questacademy.edu/sql/select-basics', 60, 15, 'The initiate speaks their first words of power: SELECT * FROM knowledge.', 1),
(8, 'Filtering with WHERE', 'https://videos.questacademy.edu/sql/where-clause', 80, 20, 'Learning to filter the vast ocean of data to find exactly what you seek.', 2);

-- =====================================================
-- SEED: Monsters (Quizzes)
-- =====================================================
INSERT INTO monsters (quest_id, name, description, question_text, correct_answer, wrong_options, damage_per_wrong_answer, monster_hp) VALUES
(1, 'The Syntax Goblin', 'A small but tricky creature that loves to confuse new programmers.', 'What is the correct way to assign a value to a variable in Python?', 'x = 5', ARRAY['x := 5', 'var x = 5', 'let x = 5'], 10, 50),
(2, 'The Type Troll', 'A hulking beast that guards the bridge between data types.', 'Which of these is a valid string in Python?', '"Hello World"', ARRAY['Hello World', '123', 'True'], 15, 75),
(3, 'The Method Mimic', 'A shapeshifter that takes the form of various string methods.', 'Which method converts a string to uppercase?', '.upper()', ARRAY['.uppercase()', '.toUpper()', '.UP()'], 12, 60),
(4, 'The Infinite Loop Dragon', 'A fearsome dragon that can trap adventurers in endless cycles.', 'What will "for i in range(3): print(i)" output?', '0, 1, 2', ARRAY['1, 2, 3', '0, 1, 2, 3', '1, 2'], 20, 100),
(6, 'The DOM Demon', 'A creature that haunts the document tree, hiding elements.', 'Which method selects an element by its ID?', 'document.getElementById()', ARRAY['document.getElement()', 'document.selectById()', 'document.findId()'], 15, 80),
(8, 'The Query Phantom', 'A ghostly figure that speaks only in SQL.', 'What SQL keyword retrieves data from a table?', 'SELECT', ARRAY['GET', 'RETRIEVE', 'FETCH'], 10, 60);

-- =====================================================
-- SEED: Assignments (Bounties)
-- =====================================================
INSERT INTO assignments (quest_id, title, description, max_score, xp_reward, gold_reward, due_date) VALUES
(3, 'String Manipulation Challenge', 'Create a Python script that takes a user''s name and outputs creative variations using string methods.', 100, 150, 50, '2026-02-01 23:59:59'),
(5, 'Loop Art Gallery', 'Use loops to create ASCII art patterns. Submit your most creative design!', 100, 200, 75, '2026-02-15 23:59:59'),
(7, 'Interactive Button Quest', 'Build an HTML page with 3 buttons that change the page content when clicked.', 100, 180, 60, '2026-02-10 23:59:59');

-- =====================================================
-- SEED: Items (Loot)
-- =====================================================
INSERT INTO items (name, description, item_type, rarity, price, hp_bonus, xp_multiplier, gold_multiplier, icon_url) VALUES
-- Weapons
('Wooden Training Sword', 'A basic sword for beginners. Not very powerful, but reliable.', 'weapon', 'common', 50, 0, 1.00, 1.00, '/icons/items/wooden_sword.png'),
('Steel Blade of Focus', 'A well-crafted blade that helps maintain concentration.', 'weapon', 'uncommon', 200, 0, 1.10, 1.00, '/icons/items/steel_blade.png'),
('Enchanted Code Staff', 'A magical staff that channels the power of clean code.', 'weapon', 'rare', 500, 10, 1.25, 1.10, '/icons/items/code_staff.png'),
('Legendary Debugger', 'The ultimate weapon against bugs and errors.', 'weapon', 'legendary', 2000, 25, 1.50, 1.25, '/icons/items/debugger.png'),

-- Armor
('Novice Robes', 'Simple cloth robes worn by all beginners.', 'armor', 'common', 30, 10, 1.00, 1.00, '/icons/items/novice_robes.png'),
('Leather Coding Vest', 'Comfortable and practical for long coding sessions.', 'armor', 'uncommon', 150, 25, 1.05, 1.00, '/icons/items/leather_vest.png'),
('Mithril Developer Armor', 'Lightweight yet incredibly resilient armor.', 'armor', 'epic', 1000, 50, 1.20, 1.15, '/icons/items/mithril_armor.png'),

-- Consumables
('Health Potion', 'Restores 25 HP instantly.', 'consumable', 'common', 20, 25, 1.00, 1.00, '/icons/items/health_potion.png'),
('XP Elixir', 'Doubles XP gain for the next quest.', 'consumable', 'rare', 300, 0, 2.00, 1.00, '/icons/items/xp_elixir.png'),
('Golden Goblet', 'Increases gold rewards for the next quest.', 'consumable', 'uncommon', 150, 0, 1.00, 2.00, '/icons/items/golden_goblet.png'),

-- Cosmetics
('Flame Aura', 'Surrounds your avatar with mystical flames.', 'cosmetic', 'rare', 400, 0, 1.00, 1.00, '/icons/items/flame_aura.png'),
('Shadow Cloak', 'A mysterious cloak that flows like darkness.', 'cosmetic', 'epic', 800, 0, 1.00, 1.00, '/icons/items/shadow_cloak.png'),

-- Boosts
('Weekend Warrior Pass', 'Earn 50% more XP on weekends.', 'boost', 'uncommon', 250, 0, 1.50, 1.00, '/icons/items/weekend_pass.png');

-- =====================================================
-- SEED: User Inventory
-- =====================================================
INSERT INTO user_inventory (user_id, item_id, quantity, is_equipped) VALUES
(1, 2, 1, TRUE),   -- shadow_blade has Steel Blade equipped
(1, 6, 1, TRUE),   -- shadow_blade has Leather Vest equipped
(1, 8, 3, FALSE),  -- shadow_blade has 3 health potions
(2, 3, 1, TRUE),   -- mystic_luna has Code Staff equipped
(2, 7, 1, TRUE),   -- mystic_luna has Mithril Armor equipped
(2, 9, 2, FALSE),  -- mystic_luna has 2 XP elixirs
(2, 11, 1, FALSE), -- mystic_luna has Flame Aura
(4, 4, 1, TRUE),   -- swift_arrow has Legendary Debugger!
(4, 7, 1, TRUE),   -- swift_arrow has Mithril Armor
(4, 12, 1, FALSE); -- swift_arrow has Shadow Cloak

-- =====================================================
-- SEED: Achievements
-- =====================================================
INSERT INTO achievements (name, description, achievement_type, requirement_value, requirement_description, xp_reward, gold_reward, title_reward, rarity) VALUES
-- Quest Achievements
('First Steps', 'Complete your first quest.', 'quest', 1, 'Complete 1 quest', 50, 25, NULL, 'common'),
('Quest Apprentice', 'Complete 10 quests.', 'quest', 10, 'Complete 10 quests', 200, 100, 'Quest Seeker', 'uncommon'),
('Quest Master', 'Complete 50 quests.', 'quest', 50, 'Complete 50 quests', 500, 300, 'Quest Master', 'rare'),
('Legendary Adventurer', 'Complete 100 quests.', 'quest', 100, 'Complete 100 quests', 1000, 750, 'Legendary Adventurer', 'legendary'),

-- Combat Achievements
('Monster Slayer', 'Defeat your first monster.', 'combat', 1, 'Defeat 1 monster', 75, 30, NULL, 'common'),
('Dragon Hunter', 'Defeat 25 monsters.', 'combat', 25, 'Defeat 25 monsters', 300, 150, 'Dragon Slayer', 'rare'),
('Perfect Victory', 'Defeat a monster without taking damage.', 'combat', 1, 'Get 100% on a quiz', 150, 75, NULL, 'uncommon'),
('Unstoppable', 'Achieve 10 perfect victories.', 'combat', 10, 'Get 100% on 10 quizzes', 500, 250, 'The Unstoppable', 'epic'),

-- Collection Achievements
('Collector', 'Own 5 different items.', 'collection', 5, 'Collect 5 unique items', 100, 50, NULL, 'common'),
('Treasure Hunter', 'Own 20 different items.', 'collection', 20, 'Collect 20 unique items', 400, 200, 'Treasure Hunter', 'rare'),
('Wealthy', 'Accumulate 1000 gold.', 'collection', 1000, 'Have 1000 gold total', 200, 0, 'The Wealthy', 'uncommon'),

-- Mastery Achievements
('Python Initiate', 'Complete all quests in The Python Caverns.', 'mastery', 1, 'Complete Python Caverns world', 500, 300, 'Python Initiate', 'rare'),
('JavaScript Journeyman', 'Complete all quests in The JavaScript Jungle.', 'mastery', 1, 'Complete JavaScript Jungle world', 500, 300, 'JS Journeyman', 'rare'),
('SQL Sage', 'Complete all quests in The SQL Sanctum.', 'mastery', 1, 'Complete SQL Sanctum world', 500, 300, 'SQL Sage', 'rare'),
('Scholar Supreme', 'Complete all available worlds.', 'mastery', 1, 'Complete all worlds', 2000, 1000, 'Scholar Supreme', 'legendary'),

-- Social Achievements
('Helpful Hero', 'Help 5 other players.', 'social', 5, 'Assist 5 players in discussions', 150, 75, 'Helpful Hero', 'uncommon'),
('Community Champion', 'Be in the top 10 on the leaderboard.', 'social', 1, 'Reach top 10 ranking', 300, 150, 'Champion', 'epic');

-- =====================================================
-- SEED: User Achievements
-- =====================================================
INSERT INTO user_achievements (user_id, achievement_id, unlocked_at) VALUES
(1, 1, '2026-01-01 10:30:00'),  -- shadow_blade: First Steps
(1, 2, '2026-01-10 15:45:00'),  -- shadow_blade: Quest Apprentice
(1, 5, '2026-01-02 11:00:00'),  -- shadow_blade: Monster Slayer
(2, 1, '2025-12-15 09:00:00'),  -- mystic_luna: First Steps
(2, 2, '2025-12-20 14:30:00'),  -- mystic_luna: Quest Apprentice
(2, 3, '2026-01-05 16:00:00'),  -- mystic_luna: Quest Master
(2, 5, '2025-12-15 10:00:00'),  -- mystic_luna: Monster Slayer
(2, 6, '2026-01-08 12:00:00'),  -- mystic_luna: Dragon Hunter
(2, 7, '2025-12-18 11:30:00'),  -- mystic_luna: Perfect Victory
(4, 1, '2025-11-01 08:00:00'),  -- swift_arrow: First Steps
(4, 2, '2025-11-10 10:00:00'),  -- swift_arrow: Quest Apprentice
(4, 3, '2025-12-01 14:00:00'),  -- swift_arrow: Quest Master
(4, 4, '2026-01-15 18:00:00'),  -- swift_arrow: Legendary Adventurer
(4, 5, '2025-11-01 09:00:00'),  -- swift_arrow: Monster Slayer
(4, 6, '2025-11-20 13:00:00'),  -- swift_arrow: Dragon Hunter
(4, 8, '2026-01-10 15:00:00'),  -- swift_arrow: Unstoppable
(4, 12, '2026-01-12 17:00:00'); -- swift_arrow: Python Initiate

-- =====================================================
-- SEED: User Progress
-- =====================================================
INSERT INTO user_progress (user_id, quest_id, is_completed, score, attempts, completed_at) VALUES
(1, 1, TRUE, 100, 1, '2026-01-01 10:30:00'),
(1, 2, TRUE, 85, 2, '2026-01-02 14:00:00'),
(1, 3, TRUE, 90, 1, '2026-01-03 11:00:00'),
(1, 4, FALSE, 0, 0, NULL),
(2, 1, TRUE, 100, 1, '2025-12-15 09:00:00'),
(2, 2, TRUE, 100, 1, '2025-12-15 10:30:00'),
(2, 3, TRUE, 95, 1, '2025-12-16 09:00:00'),
(2, 4, TRUE, 100, 1, '2025-12-17 14:00:00'),
(2, 5, TRUE, 90, 2, '2025-12-18 16:00:00'),
(4, 1, TRUE, 100, 1, '2025-11-01 08:00:00'),
(4, 2, TRUE, 100, 1, '2025-11-01 09:00:00'),
(4, 3, TRUE, 100, 1, '2025-11-02 10:00:00'),
(4, 4, TRUE, 100, 1, '2025-11-03 11:00:00'),
(4, 5, TRUE, 100, 1, '2025-11-04 12:00:00'),
(4, 6, TRUE, 100, 1, '2025-11-05 13:00:00'),
(4, 7, TRUE, 95, 1, '2025-11-06 14:00:00'),
(4, 8, TRUE, 100, 1, '2025-11-07 15:00:00'),
(4, 9, TRUE, 100, 1, '2025-11-08 16:00:00');

-- =====================================================
-- SEED: Submissions
-- =====================================================
INSERT INTO submissions (assignment_id, user_id, submission_url, submission_text, status, teacher_feedback, grade_awarded, submitted_at, graded_at) VALUES
(1, 1, 'https://github.com/shadow_blade/string-challenge', 'Used upper(), lower(), title(), and custom formatting to create name variations.', 'approved', 'Excellent work! Creative use of string methods. Consider adding more edge case handling.', 92, '2026-01-18 20:30:00', '2026-01-19 10:00:00'),
(1, 2, 'https://github.com/mystic_luna/string-magic', 'Implemented all required methods plus added regex patterns for advanced manipulation.', 'approved', 'Outstanding! Going above and beyond with regex. Perfect implementation.', 100, '2026-01-17 18:00:00', '2026-01-18 09:30:00'),
(2, 2, 'https://github.com/mystic_luna/loop-art', NULL, 'pending', NULL, NULL, '2026-01-19 22:00:00', NULL),
(3, 4, 'https://github.com/swift_arrow/interactive-buttons', 'Created a theme switcher with 3 buttons for light, dark, and neon modes.', 'approved', 'Brilliant execution! The neon theme is particularly impressive.', 98, '2026-01-15 14:00:00', '2026-01-16 11:00:00');

-- =====================================================
-- SEED: Leaderboard Entries
-- =====================================================
INSERT INTO leaderboard_entries (user_id, world_id, total_xp, total_gold, quests_completed, monsters_defeated, achievements_unlocked, rank_position, period_start, period_end) VALUES
-- Global leaderboard (world_id NULL = all worlds)
(4, NULL, 9800, 2100, 45, 42, 8, 1, '2026-01-01', '2026-01-31'),
(2, NULL, 5200, 890, 28, 25, 7, 2, '2026-01-01', '2026-01-31'),
(1, NULL, 2500, 350, 12, 10, 3, 3, '2026-01-01', '2026-01-31'),
(3, NULL, 1100, 150, 5, 4, 0, 4, '2026-01-01', '2026-01-31'),
(5, NULL, 0, 0, 0, 0, 0, 5, '2026-01-01', '2026-01-31'),

-- Python Caverns leaderboard
(4, 1, 3500, 800, 15, 15, 1, 1, '2026-01-01', '2026-01-31'),
(2, 1, 2000, 400, 10, 10, 0, 2, '2026-01-01', '2026-01-31'),
(1, 1, 1200, 200, 6, 5, 0, 3, '2026-01-01', '2026-01-31'),

-- JavaScript Jungle leaderboard
(4, 2, 2800, 600, 12, 12, 0, 1, '2026-01-01', '2026-01-31'),
(2, 2, 1500, 300, 8, 7, 0, 2, '2026-01-01', '2026-01-31');

-- =====================================================
-- VERIFICATION QUERY
-- =====================================================
SELECT 
    'Schema created successfully!' AS status,
    (SELECT COUNT(*) FROM teachers) AS teachers_count,
    (SELECT COUNT(*) FROM users) AS users_count,
    (SELECT COUNT(*) FROM worlds) AS worlds_count,
    (SELECT COUNT(*) FROM zones) AS zones_count,
    (SELECT COUNT(*) FROM quests) AS quests_count,
    (SELECT COUNT(*) FROM monsters) AS monsters_count,
    (SELECT COUNT(*) FROM assignments) AS assignments_count,
    (SELECT COUNT(*) FROM items) AS items_count,
    (SELECT COUNT(*) FROM achievements) AS achievements_count;
