import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { questsAPI, assignmentsAPI } from '../api/api';
import { useAuth } from '../context/AuthContext';
import BattleArena from '../components/battle/BattleArena';
import './QuestDetail.css';

// Get placeholder video URL based on lesson topic
const getPlaceholderVideo = (title) => {
    const lower = title?.toLowerCase() || '';

    // Map topics to educational placeholder videos (YouTube embeds)
    if (lower.includes('python')) return 'https://www.youtube.com/embed/kqtD5dpn9C8'; // Python basics
    if (lower.includes('javascript') || lower.includes('js')) return 'https://www.youtube.com/embed/W6NZfCO5SIk'; // JS tutorial
    if (lower.includes('react')) return 'https://www.youtube.com/embed/Ke90Tje7VS0'; // React intro
    if (lower.includes('sql') || lower.includes('database')) return 'https://www.youtube.com/embed/HXV3zeQKqGY'; // SQL basics
    if (lower.includes('c++') || lower.includes('cpp')) return 'https://www.youtube.com/embed/vLnPwxZdW4Y'; // C++ intro
    if (lower.includes('java') && !lower.includes('script')) return 'https://www.youtube.com/embed/eIrMbAQSU34'; // Java intro
    if (lower.includes('algorithm')) return 'https://www.youtube.com/embed/8hly31xKli0'; // Algorithms
    if (lower.includes('data structure')) return 'https://www.youtube.com/embed/RBSGKlAvoiM'; // Data structures
    if (lower.includes('go') || lower.includes('golang')) return 'https://www.youtube.com/embed/YS4e4q9oBaU'; // Go tutorial
    if (lower.includes('rust')) return 'https://www.youtube.com/embed/5C_HPTJg5ek'; // Rust tutorial
    if (lower.includes('docker')) return 'https://www.youtube.com/embed/fqMOX6JJhGo'; // Docker basics
    if (lower.includes('kube')) return 'https://www.youtube.com/embed/X48VuDVv0do'; // Kubernetes
    if (lower.includes('ai') || lower.includes('machine')) return 'https://www.youtube.com/embed/JMUxmLyrhSk'; // ML basics
    if (lower.includes('git')) return 'https://www.youtube.com/embed/8JJ101D3knE'; // Git tutorial
    if (lower.includes('css') || lower.includes('style')) return 'https://www.youtube.com/embed/1Rs2ND1ryYc'; // CSS basics
    if (lower.includes('html')) return 'https://www.youtube.com/embed/UB1O30fR-EE'; // HTML basics
    if (lower.includes('typescript') || lower.includes('type')) return 'https://www.youtube.com/embed/BwuLxPH8IDs'; // TypeScript
    if (lower.includes('flutter')) return 'https://www.youtube.com/embed/pTJJsmejUOQ'; // Flutter
    if (lower.includes('next') || lower.includes('nextjs')) return 'https://www.youtube.com/embed/mTz0GXj8NN0'; // Next.js
    if (lower.includes('three') || lower.includes('3d')) return 'https://www.youtube.com/embed/Q7AOvWpIVHU'; // Three.js

    // Default: General programming intro
    return 'https://www.youtube.com/embed/zOjov-2OZ0E'; // Learn to code
};



export default function QuestDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { refreshUser } = useAuth();

    const [quest, setQuest] = useState(null);
    const [assignments, setAssignments] = useState([]); // List of assignments

    const [loading, setLoading] = useState(true);
    const [completing, setCompleting] = useState(false);
    const [result, setResult] = useState(null);
    const [nextQuestId, setNextQuestId] = useState(null);

    useEffect(() => {
        loadQuest();
    }, [id]);

    const loadQuest = async () => {
        setLoading(true);
        setResult(null);
        setAssignments([]);

        try {
            const res = await questsAPI.getOne(id);
            setQuest(res.data);

            // Check for assignments
            if (res.data.assignments && res.data.assignments.length > 0) {
                setAssignments(res.data.assignments);
            } else {
                // Fallback: Fetch explicitly
                try {
                    const assignRes = await assignmentsAPI.getQuest(id);
                    setAssignments(assignRes.data);
                } catch (e) {
                    // No assignments or error, ignore
                }
            }

            // Next Quest Logic
            const zoneRes = await questsAPI.getByZone(res.data.zone_id);
            const zoneQuests = zoneRes.data.sort((a, b) => a.order_index - b.order_index);
            const currentIndex = zoneQuests.findIndex(q => q.quest_id === res.data.quest_id);
            if (currentIndex !== -1 && currentIndex < zoneQuests.length - 1) {
                setNextQuestId(zoneQuests[currentIndex + 1].quest_id);
            }
        } catch (error) {
            console.error("Load failed", error);
        }
        setLoading(false);
    };

    const handleStandardComplete = async () => {
        if (completing) return;
        setCompleting(true);
        try {
            const res = await questsAPI.complete(id);
            setResult(res.data);

            // Refresh user stats
            setTimeout(async () => {
                await refreshUser();
            }, 100);

            // Re-calculate next quest logic manually to be sure
            // (Standard logic in useEffect handles it, but we double check)
        } catch (e) {
            console.error("Completion Error:", e);
            alert("Failed to complete quest. Please check console or try again.");
        }
        setCompleting(false);
    };

    if (loading) return <div className="page-centered"><div className="spinner" /></div>;
    if (!quest) return <div className="page-centered">Quest not found</div>;

    // Detect Mode
    const isQuiz = (quest.quest_type === 'quiz' || (quest.monsters && quest.monsters.length > 0));
    // Fix: Prioritise checking explicit monster array or type

    const activeAssignment = assignments && assignments.length > 0 ? assignments[0] : null;

    // RENDER: BATTLE
    if (isQuiz && quest.monsters.length > 0) {
        return (
            <div className="quest-page">
                <div className="quest-header-section">
                    <Link to={`/zones/${quest.zone_id}`} className="back-link">← Back to Zone</Link>
                </div>
                <div className="quest-container glass-card" style={{ maxWidth: '1200px', padding: '0' }}>
                    <BattleArena
                        monsterId={quest.monsters[0].monster_id}
                        onBattleComplete={(victory, battleResult) => {
                            if (victory) {
                                setResult(battleResult || { xp_earned: quest.xp_reward, gold_earned: quest.gold_reward });
                                refreshUser();
                            } else {
                                navigate(`/zones/${quest.zone_id}`);
                            }
                        }}
                    />
                    {result && <VictoryModal result={result} navigate={navigate} zoneId={quest.zone_id} />}
                </div>
            </div>
        );
    }

    // RENDER: STANDARD LESSON (with optional assignment section)
    return (
        <div className="quest-page">
            <div className="quest-container glass-card">
                <div className="quest-header-section">
                    <Link to={`/zones/${quest.zone_id}`} className="back-link">← Back to Zone</Link>
                    <div className="quest-title-row">
                        <h1>{quest.title}</h1>
                        <span className="quest-reward-badge">🏆 +{quest.xp_reward} XP | 🪙 +{quest.gold_reward} Gold</span>
                    </div>
                </div>

                <div className="quest-content">
                    {/* AI Video Placeholder Section */}
                    <div className="video-section">
                        <div className="video-container">
                            <iframe
                                src={getPlaceholderVideo(quest.title)}
                                title={`Lesson: ${quest.title}`}
                                frameBorder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            />
                        </div>
                        <div className="video-placeholder-notice">
                            <span className="ai-badge">🤖 AI Generated</span>
                            <span className="notice-text">Placeholder content - Real lesson coming soon!</span>
                        </div>
                    </div>

                    {/* Lesson Content Section */}
                    <p className="quest-description">{quest.description}</p>
                    {quest.content_url && (
                        <div className="content-viewer">
                            <a href={quest.content_url} target="_blank" rel="noopener noreferrer" className="external-content-link">
                                📚 View Additional Resources
                            </a>
                        </div>
                    )}
                    {quest.ai_narrative_prompt && (
                        <div className="ai-narrative">
                            <strong>🧙‍♂️ Mentor says:</strong> "{quest.ai_narrative_prompt}"
                        </div>
                    )}

                    {/* Action Area: Complete Lesson + Next Lesson */}
                    <div className="action-area">
                        {result ? (
                            <VictoryModal
                                result={result}
                                navigate={navigate}
                                zoneId={quest.zone_id}
                                nextQuestId={nextQuestId}
                            />
                        ) : (
                            <div className="completion-controls">
                                <button className="btn btn-primary btn-large" onClick={handleStandardComplete} disabled={completing}>
                                    {completing ? 'Completing...' : '✅ Complete Lesson'}
                                </button>
                                {quest.is_completed && nextQuestId && (
                                    <button className="btn btn-gold btn-large" onClick={() => navigate(`/quests/${nextQuestId}`)}>
                                        Next Lesson →
                                    </button>
                                )}
                            </div>
                        )}
                    </div>

                    {/* Optional Assignment Section (shown below lesson content) */}
                    {activeAssignment && (
                        <div className="assignment-section">
                            <div className="assignment-divider">
                                <span>📋 Assignment</span>
                            </div>
                            <div className="assignment-details">
                                <h3>📋 Mission Brief: {activeAssignment.title}</h3>
                                <p>{activeAssignment.description}</p>
                                <p className="rewards-info">
                                    Max Score: {activeAssignment.max_score} | Power: {activeAssignment.xp_reward}XP | Bounty: {activeAssignment.gold_reward}g
                                </p>
                            </div>
                            <div className="assignment-actions" style={{ marginTop: '20px' }}>
                                <Link
                                    to={`/assignment/${activeAssignment.assignment_id}`}
                                    className="btn btn-primary btn-block"
                                    style={{ textAlign: 'center', display: 'block', padding: '12px' }}
                                >
                                    Proceed to Assignment Submission
                                </Link>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

// ... victory modal ...

function VictoryModal({ result, navigate, zoneId, nextQuestId, isAssignment }) {
    return (
        <motion.div className="result-card" initial={{ scale: 0.8 }} animate={{ scale: 1 }}>
            <h2>{isAssignment ? 'Transmission Sent' : '🎉 Quest Complete!'}</h2>
            {(result.leveled_up || result.event === 'LEVEL_UP') && (
                <motion.div
                    initial={{ scale: 0, rotate: -10 }}
                    animate={{ scale: 1.2, rotate: 0 }}
                    className="level-up-badge"
                    style={{ color: '#FFD700', fontSize: '2rem', fontWeight: 'bold', margin: '15px 0', textShadow: '0 0 10px #FFD700' }}
                >
                    🆙 LEVEL UP!
                </motion.div>
            )}
            {result.message && <p>{result.message}</p>}

            {result.xp_earned > 0 && (
                <div className="rewards-summary">
                    <div className="reward-item"><span>+{result.xp_earned} XP</span></div>
                    <div className="reward-item"><span>+{result.gold_earned} Gold</span></div>
                </div>
            )}

            <div className="nav-buttons">
                <button className="btn btn-primary" onClick={() => navigate(`/zones/${zoneId}`)}>Return to Map</button>
                {nextQuestId && <button className="btn btn-gold" onClick={() => navigate(`/quests/${nextQuestId}`)}>Next Lesson →</button>}
            </div>
        </motion.div>
    );
}
