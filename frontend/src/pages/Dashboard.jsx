import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { worldsAPI, progressAPI, engagementAPI, assignmentsAPI } from '../api/api';
import TiltCard from '../components/common/TiltCard';
import NotificationDropdown from '../components/notifications/NotificationDropdown';
import './Dashboard.css';

// World background image mapping
const getWorldBg = (title) => {
    const lower = title?.toLowerCase() || '';
    if (lower.includes('python')) return '/images/worlds/python_bg.jpg';
    if (lower.includes('javascript') || lower.includes('js')) return '/images/worlds/javascript_bg.jpg';
    if (lower.includes('sql')) return '/images/worlds/sql_bg.jpg';
    if (lower.includes('c++') || lower.includes('cpp')) return '/images/worlds/cpp_bg.jpg';
    if (lower.includes('java') && !lower.includes('script')) return '/images/worlds/java_bg.jpg';
    if (lower.includes('ai') || lower.includes('artificial')) return '/images/worlds/ai_bg.jpg';
    if (lower.includes('git')) return '/images/worlds/git_bg.jpg';
    return '/images/worlds/default_bg.jpg';
};

// Mage Card Mapping (Portrait)
const getMageCard = (title) => {
    const lower = title?.toLowerCase() || '';
    if (lower.includes('go')) return '/images/worlds/mage_go_card.png';
    if (lower.includes('rust')) return '/images/worlds/mage_rust_card.png';
    if (lower.includes('docker')) return '/images/worlds/mage_docker_card.png';
    if (lower.includes('kube')) return '/images/worlds/mage_kube_card.png';
    if (lower.includes('graph')) return '/images/worlds/mage_graph_card.png';
    if (lower.includes('cloud')) return '/images/worlds/mage_cloud_card.png';
    return null;
};

// World theme colors
const getWorldTheme = (title) => {
    const lowerTitle = title?.toLowerCase() || '';
    if (lowerTitle.includes('python')) return { primary: '#10b981', glow: 'rgba(16, 185, 129, 0.5)' };
    if (lowerTitle.includes('sql')) return { primary: '#3b82f6', glow: 'rgba(59, 130, 246, 0.5)' };
    if (lowerTitle.includes('git')) return { primary: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.5)' };
    if (lowerTitle.includes('javascript') || lowerTitle.includes('js')) return { primary: '#f59e0b', glow: 'rgba(245, 158, 11, 0.5)' };
    if (lowerTitle.includes('c++') || lowerTitle.includes('cpp')) return { primary: '#3178c6', glow: 'rgba(49, 120, 198, 0.5)' };
    if (lowerTitle.includes('java') && !lowerTitle.includes('script')) return { primary: '#f89820', glow: 'rgba(248, 152, 32, 0.5)' };
    if (lowerTitle.includes('ai') || lowerTitle.includes('artificial')) return { primary: '#ef4444', glow: 'rgba(239, 68, 68, 0.5)' };

    // Mage Worlds
    if (lowerTitle.includes('go')) return { primary: '#06b6d4', glow: 'rgba(6, 182, 212, 0.5)' }; // Cyan
    if (lowerTitle.includes('rust')) return { primary: '#f97316', glow: 'rgba(249, 115, 22, 0.5)' }; // Orange
    if (lowerTitle.includes('docker')) return { primary: '#0ea5e9', glow: 'rgba(14, 165, 233, 0.5)' }; // Sky Blue
    if (lowerTitle.includes('kube')) return { primary: '#3b82f6', glow: 'rgba(59, 130, 246, 0.5)' }; // Blue
    if (lowerTitle.includes('graph')) return { primary: '#ec4899', glow: 'rgba(236, 72, 153, 0.5)' }; // Pink
    if (lowerTitle.includes('cloud')) return { primary: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.5)' }; // Purple (keeping default-ish but explicit)

    return { primary: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.5)' };
};

function Dashboard() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [worlds, setWorlds] = useState([]);
    const [stats, setStats] = useState(null);
    const [engagement, setEngagement] = useState(null);
    const [miniLeaderboard, setMiniLeaderboard] = useState(null);
    const [pendingAssignments, setPendingAssignments] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            const [worldsRes, statsRes, engagementRes, leaderboardRes, assignmentsRes] = await Promise.all([
                worldsAPI.getAll(),
                progressAPI.getStats(),
                engagementAPI.getDashboard().catch(() => ({ data: null })),
                engagementAPI.getMiniLeaderboard().catch(() => ({ data: null })),
                assignmentsAPI.getUserPending().catch(() => ({ data: [] })),
            ]);
            setWorlds(worldsRes.data);
            setStats(statsRes.data);
            setEngagement(engagementRes.data);
            setPendingAssignments(assignmentsRes.data || []);
            setMiniLeaderboard(leaderboardRes.data);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
        setLoading(false);
    };

    if (loading) {
        return (
            <div className="page-centered">
                <div className="spinner" />
            </div>
        );
    }

    const xpForLevel = 1000;
    const currentLevelXP = (user?.current_xp || 0) % xpForLevel;
    const levelProgress = (currentLevelXP / xpForLevel) * 100;
    const hpPercent = (user?.hp_current / user?.hp_max) * 100 || 100;

    return (
        <div className="dashboard-8ball">
            {/* Background Effects */}
            <div className="bg-gradient" />
            <div className="bg-particles" />

            {/* TOP BAR - Currency & Profile */}
            <div className="top-bar">
                <div className="currency-section">
                    <div className="currency-item gold">
                        <span className="currency-icon">🪙</span>
                        <span className="currency-value">{user?.gold?.toLocaleString() || 0}</span>
                        <button className="add-btn">+</button>
                    </div>
                    <div className="currency-item xp">
                        <span className="currency-icon">⭐</span>
                        <span className="currency-value">{user?.current_xp?.toLocaleString() || 0}</span>
                    </div>
                </div>

                <div className="profile-section">
                    <Link to="/profile" className="profile-card">
                        <div className="avatar-container">
                            <div className="avatar-ring" style={{ '--progress': `${levelProgress}%` }}>
                                <div className="avatar">
                                    {user?.avatar_class === 'Warrior' && '⚔️'}
                                    {user?.avatar_class === 'Mage' && '🧙'}
                                    {user?.avatar_class === 'Rogue' && '🗡️'}
                                    {user?.avatar_class === 'Healer' && '💚'}
                                    {(!user?.avatar_class || user?.avatar_class === 'Novice') && '🎮'}
                                </div>
                            </div>
                            <div className="level-badge">{user?.level || 1}</div>
                        </div>
                        <div className="profile-info">
                            <span className="username">{user?.username}</span>
                            <span className="title">{user?.avatar_class || 'Novice'}</span>
                        </div>
                    </Link>
                </div>

                <div className="right-actions">
                    <div className="streak-display">
                        <span className="streak-icon">🔥</span>
                        <span className="streak-value">{engagement?.streak?.current_streak || 0}</span>
                    </div>

                    <NotificationDropdown />
                </div>
            </div>

            {/* HEALTH BAR */}
            <div className="health-bar-container">
                <div className="health-bar">
                    <div className="health-fill" style={{ width: `${hpPercent}%` }} />
                    <span className="health-text">❤️ {user?.hp_current}/{user?.hp_max}</span>
                </div>
            </div>

            {/* MAIN PLAY SECTION */}
            <div className="main-section">
                <motion.div
                    className="play-section"
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                >
                    <h2 className="section-title">Choose Your Quest</h2>

                    {/* Worlds Horizontal Scroll */}
                    <div className="worlds-carousel">
                        {worlds
                            .filter(w => !w.required_class || w.required_class === 'All' || w.required_class === user.avatar_class)
                            .map((world, index) => {
                                const theme = getWorldTheme(world.title);
                                // Prefer specific Mage card if available and user is Mage (or if we just want to force it for these worlds)
                                const mageCard = getMageCard(world.title);
                                const bgImage = (user?.avatar_class === 'Mage' && mageCard) ? mageCard : (world.thumbnail_url || getWorldBg(world.title));

                                return (
                                    <motion.div
                                        key={world.world_id}
                                        initial={{ opacity: 0, x: 50 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                        style={{ height: '100%' }}
                                    >
                                        <Link to={`/worlds/${world.world_id}`} style={{ textDecoration: 'none', display: 'block', height: '100%' }}>
                                            <TiltCard className="world-card-wrapper">
                                                <div
                                                    className="world-card-8ball"
                                                    style={{
                                                        '--world-primary': theme.primary,
                                                        '--world-glow': theme.glow,
                                                        backgroundImage: `url(${bgImage})`,
                                                        transform: 'none' // Override existing CSS transform
                                                    }}
                                                >
                                                    <div className="world-overlay" />
                                                    <div className="world-content">
                                                        <h3>{world.title}</h3>
                                                        <span className="world-level">Level: {world.difficulty_level || 'Easy'}</span>
                                                    </div>
                                                    <div className="play-indicator">
                                                        <span>▶</span>
                                                    </div>
                                                </div>
                                            </TiltCard>
                                        </Link>
                                    </motion.div>
                                );
                            })}
                    </div>
                </motion.div>
            </div>

            {/* UPCOMING ASSIGNMENTS SECTION */}
            {pendingAssignments.length > 0 && (
                <div className="assignments-section">
                    <div className="section-header">
                        <h3>📝 Upcoming Assignments</h3>
                        <span className="badge">{pendingAssignments.filter(a => a.status === 'not_submitted').length} pending</span>
                    </div>
                    <div className="assignments-scroll">
                        {pendingAssignments.slice(0, 5).map((assignment, index) => (
                            <motion.div
                                key={assignment.assignment_id}
                                initial={{ opacity: 0, scale: 0.9, y: 10 }}
                                animate={{ opacity: 1, scale: 1, y: 0 }}
                                transition={{ delay: index * 0.05 }}
                            >
                                <div className="assignment-dashboard-wrapper">
                                    <TiltCard className="assignment-tilt-wrapper" scale={1.03} max={10}>
                                        <div
                                            className={`assignment-card glass-card ${assignment.is_overdue ? 'overdue' : ''} ${assignment.status}`}
                                            style={{ transform: 'none', height: '100%', marginBottom: 0 }}
                                        >
                                            <div className="assignment-icon">
                                                {assignment.status === 'completed' && '✅'}
                                                {assignment.status === 'pending_review' && '⏳'}
                                                {assignment.status === 'not_submitted' && (assignment.is_overdue ? '⚠️' : '📝')}
                                                {assignment.status === 'rejected' && '❌'}
                                            </div>
                                            <div className="assignment-info">
                                                <span className="assignment-title">{assignment.title}</span>
                                                <span className="assignment-world">{assignment.world_title} • {assignment.quest_title}</span>
                                            </div>
                                            <div className="assignment-meta">
                                                <span className="assignment-reward">+{assignment.xp_reward} XP</span>
                                                {assignment.status !== 'not_submitted' && (
                                                    <span className={`status-badge ${assignment.status}`}>
                                                        {assignment.status === 'pending_review' ? 'In Review' : assignment.status}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </TiltCard>

                                    {assignment.status === 'not_submitted' && (
                                        <div className="assignment-dashboard-action">
                                            <Link
                                                className="assignment-action btn-block"
                                                to={`/assignment/${assignment.assignment_id}`}
                                            >
                                                Start
                                            </Link>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            )}

            {/* BOTTOM SECTION - Daily & Quick Actions */}
            <div className="bottom-section">
                {/* Daily Rewards */}
                <div className="daily-section">
                    <div className="section-header">
                        <h3>📋 Daily Quests</h3>
                    </div>
                    <div className="daily-quests-row">
                        {engagement?.daily_quests?.slice(0, 3).map((quest) => (
                            <div key={quest.quest_id} className={`daily-quest-chip ${quest.is_completed ? 'completed' : ''}`}>
                                <span className="dq-icon">{quest.icon}</span>
                                <div className="dq-info">
                                    <span className="dq-name">{quest.title}</span>
                                    <span className="dq-reward">+{quest.xp_reward} XP</span>
                                </div>
                                {quest.is_completed && <span className="check">✓</span>}
                            </div>
                        )) || (
                                <p className="no-quests-msg">Complete lessons to unlock!</p>
                            )}
                    </div>
                </div>

                {/* Quick Actions Grid */}
                <div className="quick-actions-grid">
                    <Link to="/shop" className="quick-action-card shop">
                        <span className="qa-icon">🛒</span>
                        <span className="qa-label">Shop</span>
                    </Link>
                    <Link to="/inventory" className="quick-action-card inventory">
                        <span className="qa-icon">🎒</span>
                        <span className="qa-label">Inventory</span>
                    </Link>
                    <Link to="/leaderboard" className="quick-action-card leaderboard">
                        <span className="qa-icon">🏆</span>
                        <span className="qa-label">Rankings</span>
                    </Link>
                    <Link to="/achievements" className="quick-action-card achievements">
                        <span className="qa-icon">🎖️</span>
                        <span className="qa-label">Trophies</span>
                    </Link>
                </div>

                {/* Mini Leaderboard */}
                <div className="mini-lb-section">
                    <div className="section-header">
                        <h3>🏆 Top Heroes</h3>
                        <Link to="/leaderboard" className="see-all">See All →</Link>
                    </div>
                    <div className="mini-lb-list">
                        {miniLeaderboard?.top_5?.slice(0, 3).map((entry, i) => (
                            <div key={i} className={`mini-lb-item ${entry.is_current_user ? 'is-me' : ''}`}>
                                <span className="rank">
                                    {i === 0 && '🥇'}
                                    {i === 1 && '🥈'}
                                    {i === 2 && '🥉'}
                                </span>
                                <span className="lb-name">{entry.username}</span>
                                <span className="lb-xp">{entry.total_xp} XP</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* WEEKLY PROGRESS */}
            <div className="weekly-progress-bar">
                <div className="wp-header">
                    <span>📊 Weekly XP</span>
                    <span>{engagement?.weekly_goals?.xp_earned || 0} / {engagement?.weekly_goals?.xp_target || 500}</span>
                </div>
                <div className="wp-bar">
                    <div className="wp-fill" style={{ width: `${engagement?.weekly_goals?.xp_percent || 0}%` }} />
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
