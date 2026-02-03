-- Update Rewards to match new economy
-- Lessons = 1 Gold
-- Quizzes = 3 Gold

UPDATE quests 
SET gold_reward = 1, xp_reward = 10 
WHERE quest_type = 'lesson';

UPDATE quests 
SET gold_reward = 3, xp_reward = 50 
WHERE quest_type = 'quiz';

-- Verify
-- SELECT * FROM quests;
