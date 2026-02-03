import { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { worldsAPI, zonesAPI } from '../api/api';
import TiltCard from '../components/common/TiltCard';
import './WorldDetail.css';

// World image mapping based on title keywords
const getWorldImage = (title) => {
    const lowerTitle = title?.toLowerCase() || '';
    if (lowerTitle.includes('python')) return '/images/worlds/python.png';
    if (lowerTitle.includes('sql')) return '/images/worlds/sql.png';
    if (lowerTitle.includes('git')) return '/images/worlds/git.png';
    if (lowerTitle.includes('javascript') || lowerTitle.includes('js')) return '/images/worlds/javascript.png';
    return '/images/worlds/python.png'; // default
};

// World theme colors
const getWorldTheme = (title) => {
    const lowerTitle = title?.toLowerCase() || '';
    if (lowerTitle.includes('python')) return { primary: '#10b981', secondary: '#059669', glow: 'rgba(16, 185, 129, 0.5)' };
    if (lowerTitle.includes('sql')) return { primary: '#3b82f6', secondary: '#2563eb', glow: 'rgba(59, 130, 246, 0.5)' };
    if (lowerTitle.includes('git')) return { primary: '#8b5cf6', secondary: '#7c3aed', glow: 'rgba(139, 92, 246, 0.5)' };
    if (lowerTitle.includes('javascript') || lowerTitle.includes('js')) return { primary: '#f59e0b', secondary: '#d97706', glow: 'rgba(245, 158, 11, 0.5)' };

    // Mage Worlds (matching Dashboard)
    if (lowerTitle.includes('go')) return { primary: '#06b6d4', secondary: '#0891b2', glow: 'rgba(6, 182, 212, 0.5)' };
    if (lowerTitle.includes('rust')) return { primary: '#f97316', secondary: '#ea580c', glow: 'rgba(249, 115, 22, 0.5)' };
    if (lowerTitle.includes('docker')) return { primary: '#0ea5e9', secondary: '#0284c7', glow: 'rgba(14, 165, 233, 0.5)' };
    if (lowerTitle.includes('kube')) return { primary: '#3b82f6', secondary: '#2563eb', glow: 'rgba(59, 130, 246, 0.5)' };
    if (lowerTitle.includes('graph')) return { primary: '#ec4899', secondary: '#db2777', glow: 'rgba(236, 72, 153, 0.5)' };
    if (lowerTitle.includes('cloud')) return { primary: '#8b5cf6', secondary: '#7c3aed', glow: 'rgba(139, 92, 246, 0.5)' };

    return { primary: '#f59e0b', secondary: '#d97706', glow: 'rgba(245, 158, 11, 0.5)' };
};

// Mage zone icon mapping - USING DASHBOARD PORTRAIT CARDS
const getMageZoneIcon = (title) => {
    const lowerTitle = title?.toLowerCase() || '';
    if (lowerTitle.includes('go')) return '/images/worlds/mage_go_card.png';
    if (lowerTitle.includes('rust')) return '/images/worlds/mage_rust_card.png';
    if (lowerTitle.includes('docker')) return '/images/worlds/mage_docker_card.png';
    if (lowerTitle.includes('kube')) return '/images/worlds/mage_kube_card.png';
    if (lowerTitle.includes('graph')) return '/images/worlds/mage_graph_card.png';
    if (lowerTitle.includes('cloud')) return '/images/worlds/mage_cloud_card.png';
    return null;
};

function WorldDetail() {
    const { id } = useParams();
    const [world, setWorld] = useState(null);
    const [zones, setZones] = useState([]);
    const [loading, setLoading] = useState(true);
    const containerRef = useRef(null);
    const activeNodeRef = useRef(null); // Ref for auto-scroll
    const { scrollYProgress } = useScroll({ container: containerRef });

    // Parallax effects
    const backgroundY = useTransform(scrollYProgress, [0, 1], ['0%', '20%']);
    const midgroundY = useTransform(scrollYProgress, [0, 1], ['0%', '10%']);

    useEffect(() => {
        loadWorld();
    }, [id]);

    const loadWorld = async () => {
        try {
            const [worldRes, zonesRes] = await Promise.all([
                worldsAPI.getOne(id),
                zonesAPI.getByWorld(id),
            ]);
            setWorld(worldRes.data);
            setZones(zonesRes.data);

            // Auto-scroll after render
            setTimeout(() => {
                if (activeNodeRef.current) {
                    activeNodeRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 500);
        } catch (error) {
            console.error('Failed to load world:', error);
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

    if (!world) {
        return (
            <div className="page-centered">
                <h2>World not found</h2>
                <Link to="/worlds" className="btn btn-primary">Back to Worlds</Link>
            </div>
        );
    }

    const theme = getWorldTheme(world.title);
    const worldImage = world.thumbnail_url || getWorldImage(world.title);

    return (
        <div
            className="world-detail-page"
            ref={containerRef}
            style={{
                '--world-primary': theme.primary,
                '--world-secondary': theme.secondary,
                '--world-glow': theme.glow
            }}
        >
            {/* Animated Backgrounds */}
            <motion.div className="parallax-bg layer-back" style={{ y: backgroundY }} />
            <motion.div className="parallax-bg layer-mid" style={{ y: midgroundY }} />
            <div className="particles-container" />

            {/* Header / HUD */}
            <div className="world-hud">
                <Link to="/worlds" className="back-btn">
                    <span className="arrow">←</span> Map
                </Link>
                <div className="world-hud-title">
                    <img src={worldImage} alt="icon" className="hud-icon" />
                    <h1>{world.title}</h1>
                </div>
                <div className="world-resources">
                    <div className="resource-pill">
                        <span className="res-icon">⭐</span>
                        <span>{world.xp_reward} XP</span>
                    </div>
                </div>
            </div>

            {/* Main Roadmap Container */}
            <div className="roadmap-container">
                <div className="roadmap-path">
                    {/* SVG Line connecting nodes would go here - simplified for now with CSS lines */}
                    <div className="path-line-container">
                        <svg className="path-svg" viewBox={`0 0 100 ${zones.length * 75}`}>
                            {/* Dynamic path generation could happen here */}
                        </svg>
                    </div>

                    {zones.map((zone, index) => {
                        // Alternate left/right alignment or zigzag
                        const isLeft = index % 2 === 0;
                        const mageIcon = getMageZoneIcon(world.title);

                        // Determine if this is the "active" node (latest unlocked)
                        // Simple logic: Is this the last unlocked zone?
                        // Assuming zones are sorted by order.
                        const isUnlocked = !zone.is_locked; // Assuming property exists, or derived
                        // If we don't have is_locked, rely on index logic if applicable. 
                        // For now, let's assume we scroll to the last one.
                        const isLast = index === zones.length - 1;

                        return (
                            <motion.div
                                key={zone.zone_id}
                                ref={isLast ? activeNodeRef : null} // Scroll to the end if that's what "content I want" likely implies for progression
                                className={`roadmap-node ${isLeft ? 'node-left' : 'node-right'}`}
                                initial={{ opacity: 0, scale: 0.8, x: isLeft ? -50 : 50 }}
                                whileInView={{ opacity: 1, scale: 1, x: 0 }}
                                viewport={{ once: true, margin: "-50px" }}
                                transition={{
                                    type: "spring",
                                    bounce: 0.4,
                                    duration: 0.8,
                                    delay: 0.1
                                }}
                            >
                                <div className="node-connector" />

                                <Link to={`/zones/${zone.zone_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                                    <TiltCard className="zone-node-wrapper">
                                        <div className="node-content glass-card" style={{ transform: 'none' }}>
                                            <div className="node-visual">
                                                <div className="node-icon-wrapper">
                                                    <span className="node-icon">
                                                        {mageIcon ? ( // Use mageIcon variable
                                                            <img
                                                                src={mageIcon} // Use mageIcon variable
                                                                alt={world.title}
                                                                style={{
                                                                    width: '100%',
                                                                    height: '100%',
                                                                    objectFit: 'cover',
                                                                    borderRadius: '10px'
                                                                }}
                                                                onError={(e) => {
                                                                    e.target.style.display = 'none'; // Hide broken images
                                                                    // Fallback logic could go here but React makes it tricky in-line
                                                                }}
                                                            />
                                                        ) : (
                                                            <>
                                                                {index === 0 && '🏰'}
                                                                {index === 1 && '⚔️'}
                                                                {index === 2 && '🛡️'}
                                                                {index === 3 && '🔥'}
                                                                {index >= 4 && '⚡'}
                                                            </>
                                                        )}
                                                    </span>
                                                    <div className="node-level">{index + 1}</div>
                                                </div>
                                            </div>

                                            <div className="node-info">
                                                <h3>{zone.title}</h3>
                                                <div className="node-meta">
                                                    <span className="quest-count">📜 {zone.quests?.length || 0} Quests</span>
                                                    <span className="xp-count">+{zone.xp_reward} XP</span>
                                                </div>
                                            </div>

                                            <div className="play-button">
                                                ▶
                                            </div>
                                        </div>
                                    </TiltCard>
                                </Link>
                            </motion.div>
                        );
                    })}

                    {/* Coming Soon Node */}
                    <motion.div
                        className="roadmap-node node-center"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 0.7 }}
                    >
                        <div className="node-content locked-node">
                            <span className="lock-icon">🔒</span>
                            <h3>Future Expansion</h3>
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
}

export default WorldDetail;
