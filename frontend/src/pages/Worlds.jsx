import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { worldsAPI } from '../api/api';
import TiltCard from '../components/common/TiltCard';
import './Worlds.css';
import { useAuth } from '../context/AuthContext';

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
    if (lowerTitle.includes('cloud')) return { primary: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.5)' }; // Purple

    return { primary: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.5)' };
};

function Worlds() {
    const { user } = useAuth();
    const [worlds, setWorlds] = useState([]);
    const [loading, setLoading] = useState(true);

    const filteredWorlds = worlds.filter(w => !w.required_class || w.required_class === 'All' || w.required_class === user?.avatar_class);

    useEffect(() => {
        loadWorlds();
    }, []);

    const loadWorlds = async () => {
        try {
            const response = await worldsAPI.getAll();
            setWorlds(response.data);
        } catch (error) {
            console.error('Failed to load worlds:', error);
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

    return (
        <div className="worlds-page">
            <div className="content-wrapper">
                <motion.div
                    className="page-header"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h1>🗺️ World Map</h1>
                    <p className="text-muted">Choose a realm to begin your adventure</p>
                </motion.div>

                <div className="worlds-grid-page">
                    {filteredWorlds.length > 0 ? (
                        filteredWorlds.map((world, index) => {
                            const theme = getWorldTheme(world.title);
                            const mageCard = getMageCard(world.title);
                            const bgImage = (user?.avatar_class === 'Mage' && mageCard) ? mageCard : (world.thumbnail_url || getWorldBg(world.title));

                            return (
                                <motion.div
                                    key={world.world_id}
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: index * 0.1 }}
                                >
                                    <Link
                                        to={`/worlds/${world.world_id}`}
                                        style={{ display: 'block', textDecoration: 'none' }}
                                    >
                                        <TiltCard className="world-card-wrapper-page">
                                            <div
                                                className="world-card-illustrated"
                                                style={{
                                                    '--world-primary': theme.primary,
                                                    '--world-glow': theme.glow,
                                                    backgroundImage: `url(${bgImage})`,
                                                    backgroundSize: 'cover',
                                                    backgroundPosition: 'center'
                                                }}
                                            >
                                                <div className="world-card-overlay" />
                                                <div className="world-card-content">
                                                    <h3 className="world-title">{world.title}</h3>
                                                    <span className="world-difficulty">
                                                        Level: {world.difficulty_level || 'Easy'}
                                                    </span>
                                                </div>
                                                <div className="world-card-glow" />
                                            </div>
                                        </TiltCard>
                                    </Link>
                                </motion.div>
                            );
                        })
                    ) : (
                        <motion.div
                            className="empty-state glass-card"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            <span className="empty-icon">🏰</span>
                            <h3>No Worlds Available</h3>
                            <p>New realms are being crafted. Check back soon!</p>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Worlds;
