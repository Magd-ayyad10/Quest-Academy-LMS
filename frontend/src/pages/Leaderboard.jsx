import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { leaderboardAPI } from '../api/api';
import { useAuth } from '../context/AuthContext';
import './Leaderboard.css';

function Leaderboard() {
    const { user } = useAuth();
    const [entries, setEntries] = useState([]);
    const [myRank, setMyRank] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadLeaderboard();
    }, []);

    const loadLeaderboard = async () => {
        try {
            const [entriesRes, rankRes] = await Promise.all([
                leaderboardAPI.getGlobal(20),
                leaderboardAPI.getMyRank(),
            ]);
            setEntries(entriesRes.data);
            setMyRank(rankRes.data);
        } catch (error) {
            console.error('Failed to load leaderboard:', error);
        }
        setLoading(false);
    };

    const getRankIcon = (position) => {
        if (position === 1) return '🥇';
        if (position === 2) return '🥈';
        if (position === 3) return '🥉';
        return `#${position}`;
    };

    if (loading) {
        return (
            <div className="page-centered">
                <div className="spinner" />
            </div>
        );
    }

    return (
        <div className="leaderboard-page">
            <div className="content-wrapper">
                <motion.div
                    className="page-header"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h1>🏆 Hall of Fame</h1>
                    <p className="text-muted">Top heroes of Quest Academy</p>
                </motion.div>

                {/* My Rank Card */}
                {myRank && (
                    <motion.div
                        className="my-rank-card glass-card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                    >
                        <div className="rank-info">
                            <span className="rank-position">{getRankIcon(myRank.rank)}</span>
                            <div className="rank-details">
                                <span className="rank-label">Your Rank</span>
                                <span className="rank-value">#{myRank.rank}</span>
                            </div>
                        </div>
                        <div className="rank-stats">
                            <div className="rank-stat">
                                <span className="stat-icon">⭐</span>
                                <span>{myRank.total_xp?.toLocaleString()} XP</span>
                            </div>
                            <div className="rank-stat">
                                <span className="stat-icon">🪙</span>
                                <span>{myRank.total_gold?.toLocaleString()} Gold</span>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* Leaderboard Table */}
                <motion.div
                    className="leaderboard-table glass-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="table-header">
                        <span className="col-rank">Rank</span>
                        <span className="col-hero">Hero</span>
                        <span className="col-level">Level</span>
                        <span className="col-xp">Total XP</span>
                        <span className="col-gold">Gold</span>
                    </div>

                    <div className="table-body">
                        {entries.length > 0 ? (
                            entries.map((entry, index) => (
                                <motion.div
                                    key={entry.entry_id || index}
                                    className={`table-row ${entry.user_id === user?.user_id ? 'highlight' : ''}`}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.03 }}
                                >
                                    <span className="col-rank">
                                        <span className={`rank-badge rank-${index + 1}`}>
                                            {getRankIcon(index + 1)}
                                        </span>
                                    </span>
                                    <span className="col-hero">
                                        <span className="hero-avatar">
                                            {entry.avatar_class === 'Warrior' && '⚔️'}
                                            {entry.avatar_class === 'Mage' && '🔮'}
                                            {entry.avatar_class === 'Ranger' && '🏹'}
                                            {entry.avatar_class === 'Paladin' && '🛡️'}
                                            {!['Warrior', 'Mage', 'Ranger', 'Paladin'].includes(entry.avatar_class) && '👤'}
                                        </span>
                                        <span className="hero-name">{entry.username}</span>
                                    </span>
                                    <span className="col-level">
                                        <span className="level-badge-small">{Math.floor((entry.total_xp || 0) / 1000) + 1}</span>
                                    </span>
                                    <span className="col-xp text-primary">
                                        {(entry.total_xp || 0).toLocaleString()}
                                    </span>
                                    <span className="col-gold text-gold">
                                        {(entry.total_gold || 0).toLocaleString()}
                                    </span>
                                </motion.div>
                            ))
                        ) : (
                            <div className="empty-row">
                                <p>No rankings yet. Be the first to claim your spot!</p>
                            </div>
                        )}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}

export default Leaderboard;
