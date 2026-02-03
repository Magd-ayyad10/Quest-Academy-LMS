import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { zonesAPI, questsAPI } from '../api/api';
import TiltCard from '../components/common/TiltCard';
import './ZoneDetail.css';

function ZoneDetail() {
    const { id } = useParams();
    const [zone, setZone] = useState(null);
    const [quests, setQuests] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadZone();
    }, [id]);

    const loadZone = async () => {
        try {
            const [zoneRes, questsRes] = await Promise.all([
                zonesAPI.getOne(id),
                questsAPI.getByZone(id),
            ]);
            setZone(zoneRes.data);
            setQuests(questsRes.data || []);
        } catch (error) {
            console.error('Failed to load zone:', error);
        }
        setLoading(false);
    };

    // Helper to group quests
    const getRoadmapItems = () => {
        return quests.map((quest, index) => {
            // Determine if it's a "Boss/Quiz" node vs a "Lesson" node
            // Strict check: Must be type 'quiz' OR have actual monsters attached.
            // Failing that, only fallback to title if type is ambiguous.
            const isBossNode = (quest.quest_type === 'quiz') || (quest.monsters && quest.monsters.length > 0);

            return {
                type: isBossNode ? 'quiz' : 'quest',
                data: quest,
                index: index + 1
            };
        });
    };

    if (loading) {
        return (
            <div className="page-centered">
                <div className="spinner" />
            </div>
        );
    }

    if (!zone) {
        return (
            <div className="page-centered">
                <h2>Zone not found</h2>
                <Link to="/worlds" className="btn btn-primary">Back to Worlds</Link>
            </div>
        );
    }

    const roadmapItems = getRoadmapItems();

    return (
        <div className="zone-detail-page">
            <div className="particles-container" />

            {/* HUD */}
            <div className="zone-hud">
                <Link to={`/worlds/${zone.world_id}`} className="back-btn">
                    <span className="arrow">←</span> Leave Zone
                </Link>
                <div className="zone-info-hud">
                    <h1>{zone.title}</h1>
                    <div className="zone-progress-pill">
                        0% Complete
                    </div>
                </div>
            </div>

            <div className="lesson-roadmap">
                {/* SVG Path visualizer */}
                <div className="path-svg-container">
                    {/* Simple centered line for now */}
                    <div className="central-line" />
                </div>

                {roadmapItems.map((item, i) => {
                    const quest = item.data;
                    const isQuiz = item.type === 'quiz';
                    const delay = i * 0.1;

                    if (isQuiz) {
                        return (
                            <motion.div
                                key={quest.quest_id}
                                className="roadmap-step step-quiz"
                                initial={{ scale: 0, opacity: 0, rotate: -10 }}
                                whileInView={{ scale: 1, opacity: 1, rotate: 0 }}
                                viewport={{ once: true, margin: "-100px" }}
                                transition={{ delay, type: "spring", stiffness: 200, damping: 15 }}
                            >
                                <Link to={`/quests/${quest.quest_id}`} className="no-underline">
                                    <TiltCard max={25} scale={1.1} className="boss-tilt-wrapper">
                                        <div className="quiz-node-boss">
                                            <motion.div
                                                className="boss-skull"
                                                animate={{
                                                    y: [0, -10, 0],
                                                    filter: ["drop-shadow(0 0 5px var(--red))", "drop-shadow(0 0 20px var(--red))", "drop-shadow(0 0 5px var(--red))"]
                                                }}
                                                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                                            >
                                                💀
                                            </motion.div>
                                            <div className="boss-label">BOSS: {quest.title}</div>
                                            <div className="boss-glow" />
                                        </div>
                                    </TiltCard>
                                </Link>
                            </motion.div>
                        );
                    }

                    const side = i % 2 === 0 ? 'left' : 'right';

                    return (
                        <motion.div
                            key={quest.quest_id}
                            className={`roadmap-step step-quest side-${side}`}
                            initial={{ x: side === 'left' ? -100 : 100, opacity: 0 }}
                            whileInView={{ x: 0, opacity: 1 }}
                            viewport={{ once: true, margin: "-100px" }}
                            transition={{
                                delay,
                                type: "spring",
                                stiffness: 100,
                                damping: 20
                            }}
                        >
                            <div className="connector-arm" />

                            <Link to={`/quests/${quest.quest_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                                <TiltCard className="quest-node-wrapper">
                                    <div className="quest-node glass-card" style={{ transform: 'none' }}>
                                        <div className="quest-status-icon">
                                            ▶
                                        </div>
                                        <div className="quest-details">
                                            <div className="quest-header">
                                                <span className="quest-num">LESSON {item.index}</span>
                                                <span className="quest-xp">+{quest.xp_reward} XP</span>
                                            </div>
                                            <h3>{quest.title}</h3>
                                            <p>{quest.description}</p>
                                        </div>
                                    </div>
                                </TiltCard>
                            </Link>
                        </motion.div>
                    );
                })}

                {/* Start Label */}
                <div className="roadmap-start">
                    {quests.length > 0 ? (
                        <Link to={`/quests/${quests[0].quest_id}`} className="btn btn-primary start-btn">
                            START ZONE
                        </Link>
                    ) : (
                        <span>START</span>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ZoneDetail;
