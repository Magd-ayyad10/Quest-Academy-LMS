import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { achievementsAPI } from '../api/api';
import './Achievements.css';

function Achievements() {
    const [achievements, setAchievements] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAchievements();
    }, []);

    const loadAchievements = async () => {
        try {
            const res = await achievementsAPI.getMy();
            setAchievements(res.data);
        } catch (error) {
            console.error(error);
        }
        setLoading(false);
    };

    if (loading) return <div className="page-centered"><div className="spinner" /></div>;

    return (
        <div className="achievements-page">
            <div className="page-header-simple">
                <h1>🏆 Trophy Case</h1>
                <p>Your legendary accomplishments</p>
            </div>

            <div className="achievements-list">
                {achievements.length > 0 ? (
                    achievements.map((entry, i) => (
                        <motion.div
                            key={entry.user_achievement_id}
                            className="achievement-card glass-card"
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <div className="achievement-icon">🏆</div>
                            <div className="achievement-details">
                                <h3>{entry.achievement.name}</h3>
                                <p>{entry.achievement.description}</p>
                                <span className="unlock-date">Unlocked: {new Date(entry.unlocked_at).toLocaleDateString()}</span>
                            </div>
                            <div className="achievement-rewards">
                                {entry.achievement.xp_reward > 0 && <span>+{entry.achievement.xp_reward} XP</span>}
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="empty-state">
                        <p>No trophies yet. Keep completing quests!</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Achievements;
