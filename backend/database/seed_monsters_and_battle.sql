-- Ensure quiz_questions table exists (in case previous step failed or skipped)
CREATE TABLE IF NOT EXISTS quiz_questions (
    question_id SERIAL PRIMARY KEY,
    monster_id INTEGER REFERENCES monsters(monster_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answers JSONB NOT NULL,
    xp_value INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

DO $$
DECLARE
    v_zone_id INT;
    v_boss_quest_id INT;
    v_monster_id INT;
BEGIN
    -- Get Zone 1 ID (Python - Entrance Hall)
    -- We assume World 1 is Python based on insert_roadmap_content.sql
    SELECT zone_id INTO v_zone_id FROM zones WHERE title LIKE 'The Entrance Hall%' LIMIT 1;
    
    IF v_zone_id IS NULL THEN
        RAISE NOTICE 'Zone 1 not found, defaulting to ID 1';
        v_zone_id := 1;
    END IF;

    -- Check if Boss Quest already exists to avoid duplicates
    SELECT quest_id INTO v_boss_quest_id FROM quests WHERE title = 'The Python Basilisk' AND zone_id = v_zone_id;

    IF v_boss_quest_id IS NULL THEN
        -- Insert Boss Quest
        INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt)
        VALUES (v_zone_id, 'The Python Basilisk', 'Defeat the guardian of syntax!', NULL, 500, 100, 'quiz', 5, 'The Basilisk demands proof of your knowledge.')
        RETURNING quest_id INTO v_boss_quest_id;
        
        RAISE NOTICE 'Created Boss Quest ID: %', v_boss_quest_id;
    ELSE
        RAISE NOTICE 'Boss Quest already exists ID: %', v_boss_quest_id;
    END IF;

    -- Check if Monster exists
    SELECT monster_id INTO v_monster_id FROM monsters WHERE quest_id = v_boss_quest_id;

    IF v_monster_id IS NULL THEN
        -- Insert Monster
        -- Note: monsters table has wrong_options as TEXT[], we pass empty array as we use quiz_questions now
        INSERT INTO monsters (quest_id, name, description, monster_hp, damage_per_wrong_answer, correct_answer, question_text, wrong_options)
        VALUES (v_boss_quest_id, 'Python Basilisk', 'A giant snake made of code.', 100, 15, 'unused', 'unused', ARRAY['unused'])
        RETURNING monster_id INTO v_monster_id;
        
        RAISE NOTICE 'Created Monster ID: %', v_monster_id;
    ELSE
        RAISE NOTICE 'Monster already exists ID: %', v_monster_id;
    END IF;

    -- Insert Questions (Clear old ones first to avoid dupes if re-running)
    DELETE FROM quiz_questions WHERE monster_id = v_monster_id;

    INSERT INTO quiz_questions (monster_id, question_text, correct_answer, wrong_answers, xp_value)
    VALUES
    (v_monster_id, 'How do you print in Python?', 'print()', '["echo()", "console.log()", "System.out.println()"]'::jsonb, 50),
    (v_monster_id, 'Which is an Integer?', '42', '["42.0", "fourty-two", "True"]'::jsonb, 50),
    (v_monster_id, 'What symbol starts a comment?', '#', '["//", "/*", "--"]'::jsonb, 50),
    (v_monster_id, 'Which keyword defines a function?', 'def', '["function", "fun", "define"]'::jsonb, 50),
    (v_monster_id, 'What is the boolean True?', 'True', '["true", "TRUE", "1"]'::jsonb, 50);

    RAISE NOTICE 'Seeded 5 questions for Monster ID: %', v_monster_id;

END $$;
