
import { useState, useEffect, useMemo } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import './NavTabs.css';

function NavTabs() {
    const { user } = useAuth();
    const location = useLocation();
    const [hoveredTab, setHoveredTab] = useState(null);

    // Dynamic tabs based on role
    const allTabs = useMemo(() => {
        const baseTabs = [
            { path: '/dashboard', label: 'Dashboard', icon: '🏰' },
            { path: '/worlds', label: 'Worlds', icon: '🗺️' },
            { path: '/assignments', label: 'Bounties', icon: '📜' },
            { path: '/shop', label: 'Shop', icon: '🛒' },
            { path: '/leaderboard', label: 'Leaderboard', icon: '🏆' }
        ];

        const roleSpecificTabs = [];
        if (user?.role === 'teacher') {
            roleSpecificTabs.push({ path: '/teacher/dashboard', label: 'Guild Studio', icon: '⚒️' });
            roleSpecificTabs.push({ path: '/admin', label: 'Admin', icon: '🛡️' });
        }
        return [...baseTabs, ...roleSpecificTabs];
    }, [user?.role]); // Dependency on user.role to re-calculate when role changes

    const [activeTab, setActiveTab] = useState(location.pathname);

    useEffect(() => {
        const current = allTabs.find(tab =>
            location.pathname === tab.path ||
            (tab.path !== '/' && location.pathname.startsWith(tab.path))
        );
        if (current) {
            setActiveTab(current.path);
        } else {
            setActiveTab(null);
        }
    }, [location.pathname, allTabs]); // allTabs is now a stable reference due to useMemo, but its content can change

    return (
        <nav className="nav-tabs-container">
            {allTabs.map((tab) => (
                <Link
                    key={tab.path}
                    to={tab.path}
                    className={`nav-tab-item ${activeTab === tab.path ? 'active' : ''}`}
                    onMouseEnter={() => setHoveredTab(tab.path)}
                    onMouseLeave={() => setHoveredTab(null)}
                >
                    {/* Hover Background - Glass Effect */}
                    <AnimatePresence>
                        {hoveredTab === tab.path && (
                            <motion.div
                                className="nav-tab-hover-bg"
                                layoutId="navHover"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.2 }}
                            />
                        )}
                    </AnimatePresence>

                    {/* Active Background - Solid/Gradient */}
                    {activeTab === tab.path && (
                        <motion.div
                            className="nav-tab-active-bg"
                            layoutId="navActive"
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        />
                    )}

                    <span className="nav-tab-content">
                        <span className="nav-tab-icon">{tab.icon}</span>
                        <span className="nav-tab-label">{tab.label}</span>
                    </span>
                </Link>
            ))}
        </nav>
    );
}

export default NavTabs;
