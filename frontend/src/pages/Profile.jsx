import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { progressAPI, userAPI } from '../api/api';
import './Profile.css';

function Profile() {
    const [profile, setProfile] = useState(null);
    const [transcript, setTranscript] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [userRes, transRes] = await Promise.all([
                userAPI.getMe(),
                progressAPI.getTranscript()
            ]);
            setProfile(userRes.data);
            setTranscript(transRes.data);
        } catch (error) {
            console.error(error);
        }
        setLoading(false);
    };

    if (loading) return <div className="spinner"></div>;

    return (
        <div className="profile-page">
            <div className="profile-header glass-card">
                <div className="profile-avatar">
                    <span>
                        {profile?.avatar_class === 'Warrior' && '⚔️'}
                        {profile?.avatar_class === 'Mage' && '🔮'}
                        {profile?.avatar_class === 'Ranger' && '🏹'}
                        {!['Warrior', 'Mage', 'Ranger'].includes(profile?.avatar_class) && '👤'}
                    </span>
                </div>
                <div className="profile-identity">
                    <h1>{profile.username}</h1>
                    <p className="profile-title">{profile.title || "Novice Adventurer"}</p>
                    <div className="profile-level">
                        Level {profile.level} {profile.avatar_class}
                    </div>
                </div>
            </div>

            <div className="scroll-of-deeds">
                <h2>📜 Scroll of Deeds (Transcript)</h2>
                {transcript.length === 0 ? (
                    <p>No deeds recorded yet. Go adventure!</p>
                ) : (
                    <div className="transcript-grid">
                        {transcript.map(record => (
                            <motion.div
                                key={record.world_id}
                                className="deed-card glass-card"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                            >
                                <div className="deed-header">
                                    <h3>{record.title}</h3>
                                    {record.certificate_eligible && <span className="cert-badge">🎖️ CERTIFIED</span>}
                                </div>

                                <div className="progress-section">
                                    <div className="progress-label">
                                        <span>Completion</span>
                                        <span>{record.progress_percent}%</span>
                                    </div>
                                    <div className="progress-bar-bg">
                                        <div
                                            className="progress-bar-fill"
                                            style={{ width: `${record.progress_percent}%`, background: record.progress_percent === 100 ? '#fbbf24' : '#3b82f6' }}
                                        />
                                    </div>
                                </div>

                                <div className="deed-stats">
                                    <div className="stat">
                                        <label>Avg Grade</label>
                                        <span>{record.average_grade}%</span>
                                    </div>
                                    <div className="stat">
                                        <label>Quests</label>
                                        <span>{record.completed_quests}/{record.total_quests}</span>
                                    </div>
                                </div>

                                {record.certificate_eligible ? (
                                    <a href="#" className="btn btn-gold btn-block" onClick={(e) => { e.preventDefault(); alert("Downloading Certificate..."); }}>
                                        Download Certificate
                                    </a>
                                ) : (
                                    <button className="btn btn-ghost btn-block" disabled>
                                        In Progress
                                    </button>
                                )}
                            </motion.div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Profile;
