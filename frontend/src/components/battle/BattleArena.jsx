import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { battleAPI } from '../../api/api';
import './BattleArena.css';

function BattleArena({ monsterId, onBattleComplete }) {
    const [gameState, setGameState] = useState(null);
    const [loading, setLoading] = useState(true);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [message, setMessage] = useState(null); // { text, type: 'hit' | 'miss' }
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        loadBattle();
    }, [monsterId]);

    const loadBattle = async () => {
        try {
            const res = await battleAPI.getState(monsterId);
            setGameState(res.data);
            // Check if already won
            if (res.data.monster_hp_pct <= 0) {
                setTimeout(() => onBattleComplete(true), 1500);
            }
        } catch (error) {
            console.error("Failed to load battle:", error);
        }
        setLoading(false);
    };

    const handleAttack = async (answer) => {
        if (processing) return;
        setProcessing(true);
        setMessage(null);

        const currentQuestion = gameState.questions[currentQuestionIndex];

        try {
            const res = await battleAPI.attack({
                question_id: currentQuestion.question_id,
                answer: answer
            });

            const result = res.data;

            // Update HP visually
            setGameState(prev => ({
                ...prev,
                player_hp: result.player_hp,
                monster_hp_pct: result.monster_hp_pct
            }));

            // Show Feedback
            const isHit = result.is_correct;

            setMessage({
                text: result.message,
                type: isHit ? 'hit' : 'miss'
            });

            if (!isHit) {
                // Trigger shake
                document.body.classList.add('shake-screen');
                setTimeout(() => document.body.classList.remove('shake-screen'), 500);
            }

            // Handle outcome
            setTimeout(() => {
                setMessage(null);
                setProcessing(false);

                if (result.monster_defeated) {
                    onBattleComplete(true, result);
                } else if (result.player_hp <= 0) {
                    setMessage({
                        text: "SYSTEM CRITICAL",
                        type: 'miss'
                    });
                    setTimeout(() => onBattleComplete(false), 2000);
                } else {
                    // Next Question
                    setCurrentQuestionIndex(prev => (prev + 1) % gameState.questions.length);
                }
            }, 2000); // Wait 2s to read message

        } catch (error) {
            console.error("Attack failed:", error);
            setProcessing(false);
        }
    };

    if (loading) return <div className="spinner"></div>;
    if (!gameState) return <div className="text-white">Failed to load arena.</div>;

    const currentQuestion = gameState.questions[currentQuestionIndex];

    return (
        <div className="battle-arena">
            {/* Header / HUD */}
            <div className="battle-header">
                {/* Player HUD */}
                <div className="combatant-hud">
                    <div className="combatant-avatar player-avatar shake-on-hit">
                        🧙‍♂️
                    </div>
                    <div className="combatant-name">Hero</div>
                    <div className="hp-bar-container">
                        <div
                            className="hp-fill player"
                            style={{ width: `${(gameState.player_hp / 100) * 100}%` }} // dynamic if max_hp known
                        />
                        <div className="hp-text">{gameState.player_hp} HP</div>
                    </div>
                </div>

                <div className="vs-badge">VS</div>

                {/* Monster HUD */}
                <div className="combatant-hud">
                    <div className="combatant-avatar monster-avatar">
                        🐍
                    </div>
                    <div className="combatant-name">{gameState.monster_name}</div>
                    <div className="hp-bar-container">
                        <div
                            className="hp-fill monster"
                            style={{ width: `${gameState.monster_hp_pct}%` }}
                        />
                        <div className="hp-text">{gameState.monster_hp_pct}%</div>
                    </div>
                </div>
            </div>

            {/* Battle Area */}
            <AnimatePresence mode="wait">
                {currentQuestion && (
                    <motion.div
                        key={currentQuestion.question_id}
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        exit={{ y: -20, opacity: 0 }}
                        className="question-card"
                    >
                        <h3 className="question-text">{currentQuestion.question_text}</h3>

                        <div className="options-grid">
                            {currentQuestion.options.map((opt, idx) => (
                                <button
                                    key={idx}
                                    className="battle-option-btn"
                                    onClick={() => handleAttack(opt)}
                                    disabled={processing}
                                >
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Overlay Messages */}
            <AnimatePresence>
                {message && (
                    <motion.div
                        className={`battle-message ${message.type}`}
                        initial={{ scale: 0.5, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 1.5, opacity: 0 }}
                    >
                        {message.text}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default BattleArena;
