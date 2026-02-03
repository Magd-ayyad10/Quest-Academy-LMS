-- Add quiz_questions table for Monster Battles
CREATE TABLE IF NOT EXISTS quiz_questions (
    question_id SERIAL PRIMARY KEY,
    monster_id INTEGER REFERENCES monsters(monster_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answers JSONB NOT NULL, -- Array of strings e.g. ["Wrong 1", "Wrong 2", "Wrong 3"]
    xp_value INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed data for Monster 1 (Assume it exists, if not we skip)
-- We'll use a DO block to find the monster by name if ID varies, or just insert if we know ID.
-- Based on previous SELECT, we'll verify IDs. For now, let's assume we want to attach to the first monster "Python Syntax Snake" or similar.

-- Let's specificially target the monster for Zone 1 (Entrance Hall).
-- In insert_roadmap_content.sql, it was likely 'Syntax Snake' or 'Bugbear'.

-- Example Seed for a Python question
INSERT INTO quiz_questions (monster_id, question_text, correct_answer, wrong_answers, xp_value)
SELECT monster_id, 'What is the correct way to output "Hello" in Python?', 'print("Hello")', '["echo \"Hello\"", "console.log(\"Hello\")", "System.out.println(\"Hello\")"]'::jsonb, 50
FROM monsters WHERE name LIKE '%Snake%' OR name LIKE '%Basilisk%' OR name LIKE '%Bug%' LIMIT 1;

INSERT INTO quiz_questions (monster_id, question_text, correct_answer, wrong_answers, xp_value)
SELECT monster_id, 'Which of these is a valid variable name?', 'my_var', '["2var", "my-var", "class"]'::jsonb, 50
FROM monsters WHERE name LIKE '%Snake%' OR name LIKE '%Basilisk%' OR name LIKE '%Bug%' LIMIT 1;

INSERT INTO quiz_questions (monster_id, question_text, correct_answer, wrong_answers, xp_value)
SELECT monster_id, 'What data type is "True"?', 'Boolean', '["String", "Integer", "Float"]'::jsonb, 50
FROM monsters WHERE name LIKE '%Snake%' OR name LIKE '%Basilisk%' OR name LIKE '%Bug%' LIMIT 1;
