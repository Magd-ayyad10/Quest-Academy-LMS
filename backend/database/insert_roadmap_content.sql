-- Clear existing quests to avoid duplicates/conflicts (optional, but safer for dev)
TRUNCATE TABLE quests RESTART IDENTITY CASCADE;

-- ==========================================
-- WORLD 1: PYTHON (Zones 1, 2, 3, 4)
-- ==========================================

-- Zone 1: The Entrance Hall - Variables
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(1, 'The Vessel of Names', 'Learn how to name your magical containers (Variables).', 'https://video.link/python/vars', 100, 10, 'lesson', 1, 'You encounter a shapeless spirit who needs a name to manifest.'),
(1, 'The Type Crystal', 'Distinguish between the elemental types: Integers, Strings, and Floats.', 'https://video.link/python/types', 100, 15, 'lesson', 2, 'Crystals of different colors hum with energy. You must sort them by their resonance.'),
(1, 'The Arithmetic Altar', 'Perform basic incantations (Math operations) to alter reality.', 'https://video.link/python/math', 100, 15, 'lesson', 3, 'The altar demands a numerical sacrifice. Calculate the sum of the stars.'),
(1, 'The String Weavers', 'Concatenate and manipulate text strings to forge messages.', 'https://video.link/python/strings', 100, 20, 'lesson', 4, 'Ancient tapestries are torn. You must weave the threads of story back together.'); 
-- Quiz Boss implicitly handled by UI after 4th quest

-- Zone 2: The Loop Labyrinth
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(2, 'The While Wisp', 'Follow the Wisp as long as the condition is true.', 'https://video.link/python/while', 150, 20, 'lesson', 1, 'A wisp beckons you. "I only fade when you stop believing," it whispers.'),
(2, 'The For-est Path', 'Iterate through the trees of the forest one by one.', 'https://video.link/python/for', 150, 20, 'lesson', 2, 'The path is lined with ancient sentinels. You must greet each one to pass.'),
(2, 'The Range Riddle', 'Master the range() spell to count your steps.', 'https://video.link/python/range', 150, 25, 'lesson', 3, 'The bridgekeeper asks: "How many steps to the other side?"'),
(2, 'The Nested Nightmare', 'Survive the loop within a loop.', 'https://video.link/python/nested', 200, 30, 'lesson', 4, 'Reality folds upon itself. To escape, you must solve the puzzle within the puzzle.');

-- Zone 3: The Function Forge
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(3, 'The Blueprint', 'Define your first function spell.', 'https://video.link/python/def', 200, 30, 'lesson', 1, 'The blacksmith hands you a blank scroll. "Draw the shape of your power," he grunts.'),
(3, 'The Parameter Gate', 'Pass arguments to your functions to customize them.', 'https://video.link/python/params', 200, 35, 'lesson', 2, 'The gate only opens if you speak the correct words of power.'),
(3, 'The Return Rune', 'Learn to return values from your functions.', 'https://video.link/python/return', 200, 35, 'lesson', 3, 'You cast a spell into the void. What comes back depends on your offering.'),
(3, 'The Scope Spectrum', 'Understand local vs global variables.', 'https://video.link/python/scope', 250, 40, 'lesson', 4, 'Some magic is bound to this room; other magic flows through the entire world.');

-- ==========================================
-- WORLD 2: JAVASCRIPT (Zones 5, 6, 7) (Assuming World 2 is JS based on prev analysis)
-- ==========================================

-- Zone 5: The DOM Thicket
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(5, 'The Selector Sight', 'Use querySelector to find elements in the thicket.', 'https://video.link/js/select', 100, 10, 'lesson', 1, 'The forest is dense. Use your sight to reveal the hidden creatures.'),
(5, 'The Event Echo', 'Listen for clicks and keypresses.', 'https://video.link/js/events', 100, 15, 'lesson', 2, 'The trees whisper when touched. Listen closely to their secrets.'),
(5, 'The Style Shifter', 'Change the appearance of elements with JS.', 'https://video.link/js/style', 100, 20, 'lesson', 3, 'Reality is malleable here. Paint the leaves with the colors of your mind.'),
(5, 'The Element Seed', 'Create and append new elements to the DOM.', 'https://video.link/js/create', 100, 25, 'lesson', 4, 'Plant a seed of code and watch a new structure grow instantly.');

-- Zone 6: The Async Swamp
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(6, 'The Callback Call', 'Understand the dangers of callback hell.', 'https://video.link/js/callback', 150, 20, 'lesson', 1, 'You shout into the fog. The echo returns... eventually.'),
(6, 'The Promise Pact', 'Make a pact with the swamp spirits (Promises).', 'https://video.link/js/promise', 150, 25, 'lesson', 2, 'The spirit agrees to aid you, but only in the future. Do you trust it?'),
(6, 'The Async Await', 'Master the timeline with async/await.', 'https://video.link/js/async', 150, 30, 'lesson', 3, 'Time flows differently for the master chronomancer. Pause the world while you work.'),
(6, 'The Fetch Ferry', 'Retrieve data across the misty waters.', 'https://video.link/js/fetch', 200, 35, 'lesson', 4, 'The ferryman brings goods from distant lands. You must wait for his arrival.');

-- ==========================================
-- WORLD 3: SQL (Zones 8, 9, 10)
-- ==========================================

-- Zone 8: The SELECT Shrine
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(8, 'The Query Scroll', 'Write your first SELECT statement.', 'https://video.link/sql/select', 100, 10, 'lesson', 1, 'The ancient scroll reveals all truth, but only if you ask the right question.'),
(8, 'The Where Ward', 'Filter results with the WHERE clause.', 'https://video.link/sql/where', 100, 15, 'lesson', 2, 'The library is vast. You must narrow your search to find the forbidden tome.'),
(8, 'The Order Orb', 'Sort your findings with ORDER BY.', 'https://video.link/sql/order', 100, 20, 'lesson', 3, 'Chaos reigns in the archives. Bring order to the records.'),
(8, 'The Limit Lock', 'Restrict the number of rows returned.', 'https://video.link/sql/limit', 100, 25, 'lesson', 4, 'You can only carry so much knowledge. Choose the top 5 scrolls.');

-- Zone 9: The JOIN Junction
INSERT INTO quests (zone_id, title, description, content_url, xp_reward, gold_reward, quest_type, order_index, ai_narrative_prompt) VALUES
(9, 'The Inner Bond', 'Connect two tables with INNER JOIN.', 'https://video.link/sql/inner', 150, 20, 'lesson', 1, 'Two paths converge. Where they meet, the truth is strongest.'),
(9, 'The Left Path', 'Keep all records from the left table with LEFT JOIN.', 'https://video.link/sql/left', 150, 25, 'lesson', 2, 'Walk the left path, but look to the right. Take what matches, leave the rest.'),
(9, 'The Right Path', 'Keep all records from the right table with RIGHT JOIN.', 'https://video.link/sql/right', 150, 25, 'lesson', 3, 'The right path holds its own secrets. Do not ignore them.'),
(9, 'The Full Union', 'Combine everything with FULL OUTER JOIN.', 'https://video.link/sql/full', 200, 35, 'lesson', 4, 'The junction is complete. All paths are now one.');
