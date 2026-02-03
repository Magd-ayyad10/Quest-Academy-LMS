import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import ParticleBackground from '../components/common/ParticleBackground';
import './Landing.css';

function Landing() {
    return (
        <div className="landing-page">
            <ParticleBackground count={60} />

            {/* Hero Section */}
            <section className="hero">
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <motion.div
                        className="hero-badge"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
                    >
                        ⚔️ RPG Learning Experience
                    </motion.div>

                    <h1 className="hero-title">
                        <span className="title-line">Learn. Battle.</span>
                        <span className="title-line highlight">Level Up.</span>
                    </h1>

                    <p className="hero-subtitle">
                        Transform your learning journey into an epic adventure.
                        Complete quests, defeat monsters, earn rewards, and become a legendary scholar.
                    </p>

                    <div className="hero-actions">
                        <Link to="/register" className="btn btn-gold btn-lg">
                            <span>🎮</span> Start Your Quest
                        </Link>
                        <Link to="/login" className="btn btn-outline btn-lg">
                            <span>⚡</span> Continue Journey
                        </Link>
                    </div>

                    <div className="hero-stats">
                        <div className="hero-stat">
                            <span className="stat-number">100+</span>
                            <span className="stat-text">Quests</span>
                        </div>
                        <div className="hero-stat">
                            <span className="stat-number">50+</span>
                            <span className="stat-text">Monsters</span>
                        </div>
                        <div className="hero-stat">
                            <span className="stat-number">∞</span>
                            <span className="stat-text">Adventures</span>
                        </div>
                    </div>
                </motion.div>

                {/* Floating Elements */}
                <div className="floating-elements">
                    <motion.div
                        className="floating-icon icon-1"
                        animate={{ y: [0, -20, 0], rotate: [0, 10, 0] }}
                        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                    >
                        📚
                    </motion.div>
                    <motion.div
                        className="floating-icon icon-2"
                        animate={{ y: [0, 20, 0], rotate: [0, -10, 0] }}
                        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                    >
                        🏆
                    </motion.div>
                    <motion.div
                        className="floating-icon icon-3"
                        animate={{ y: [0, -15, 0], rotate: [0, 15, 0] }}
                        transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut" }}
                    >
                        💎
                    </motion.div>
                    <motion.div
                        className="floating-icon icon-4"
                        animate={{ y: [0, 25, 0], rotate: [0, -5, 0] }}
                        transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }}
                    >
                        🗡️
                    </motion.div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features">
                <motion.h2
                    className="section-title"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                >
                    Your Adventure Awaits
                </motion.h2>

                <div className="features-grid">
                    {[
                        { icon: '🗺️', title: 'Explore Worlds', desc: 'Journey through courses designed as magical realms' },
                        { icon: '⚔️', title: 'Battle Monsters', desc: 'Test your knowledge against fearsome quiz creatures' },
                        { icon: '🎒', title: 'Collect Loot', desc: 'Earn gold, items, and powerful equipment' },
                        { icon: '📈', title: 'Level Up', desc: 'Gain XP and unlock new abilities as you progress' },
                        { icon: '🏆', title: 'Achievements', desc: 'Unlock trophies and earn legendary titles' },
                        { icon: '👑', title: 'Leaderboards', desc: 'Compete with heroes from around the realm' },
                    ].map((feature, index) => (
                        <motion.div
                            key={index}
                            className="feature-card glass-card"
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.03 }}
                        >
                            <span className="feature-icon">{feature.icon}</span>
                            <h3>{feature.title}</h3>
                            <p>{feature.desc}</p>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <motion.div
                    className="cta-content glass-card"
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                >
                    <h2>Ready to Begin Your Journey?</h2>
                    <p>Join thousands of heroes already leveling up their knowledge</p>
                    <Link to="/register" className="btn btn-gold btn-lg">
                        Create Your Hero
                    </Link>
                </motion.div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <p>⚔️ Quest Academy LMS - Where Learning Becomes Adventure</p>
            </footer>
        </div>
    );
}

export default Landing;
