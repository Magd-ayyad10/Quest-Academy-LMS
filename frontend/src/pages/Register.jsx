import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import ParticleBackground from '../components/common/ParticleBackground';
import './Auth.css';

const AVATAR_CLASSES = [
    { id: 'Warrior', icon: '⚔️', name: 'Warrior', desc: 'Strong and brave' },
    { id: 'Mage', icon: '🔮', name: 'Mage', desc: 'Wise and powerful' },
    { id: 'Ranger', icon: '🏹', name: 'Ranger', desc: 'Quick and precise' },
    { id: 'Paladin', icon: '🛡️', name: 'Paladin', desc: 'Noble defender' },
];

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        avatar_class: 'Warrior',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        setLoading(true);

        const result = await register({
            username: formData.username,
            email: formData.email,
            password: formData.password,
            avatar_class: formData.avatar_class,
        });

        if (result.success) {
            navigate('/dashboard');
        } else {
            setError(result.error);
        }

        setLoading(false);
    };

    return (
        <div className="auth-page">
            <ParticleBackground count={40} />

            <motion.div
                className="auth-container"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div className="auth-card glass-card register-card">
                    <div className="auth-header">
                        <span className="auth-icon">🎮</span>
                        <h1>Create Your Hero</h1>
                        <p>Begin your legendary journey</p>
                    </div>

                    {error && (
                        <motion.div
                            className="auth-error"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                        >
                            ⚠️ {error}
                        </motion.div>
                    )}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="input-group">
                            <label>Hero Name</label>
                            <input
                                type="text"
                                name="username"
                                className="input-field"
                                placeholder="Enter your hero name"
                                value={formData.username}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label>Email</label>
                            <input
                                type="email"
                                name="email"
                                className="input-field"
                                placeholder="hero@questacademy.edu"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label>Choose Your Class</label>
                            <div className="class-selector">
                                {AVATAR_CLASSES.map((cls) => (
                                    <motion.div
                                        key={cls.id}
                                        className={`class-option ${formData.avatar_class === cls.id ? 'selected' : ''}`}
                                        onClick={() => setFormData({ ...formData, avatar_class: cls.id })}
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                    >
                                        <span className="class-icon">{cls.icon}</span>
                                        <span className="class-name">{cls.name}</span>
                                    </motion.div>
                                ))}
                            </div>
                        </div>

                        <div className="input-row">
                            <div className="input-group">
                                <label>Password</label>
                                <input
                                    type="password"
                                    name="password"
                                    className="input-field"
                                    placeholder="Create password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                            <div className="input-group">
                                <label>Confirm Password</label>
                                <input
                                    type="password"
                                    name="confirmPassword"
                                    className="input-field"
                                    placeholder="Confirm password"
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            className="btn btn-gold btn-full"
                            disabled={loading}
                        >
                            {loading ? (
                                <span className="spinner-small" />
                            ) : (
                                <>🎮 Begin Adventure</>
                            )}
                        </button>
                    </form>

                    <div className="auth-footer">
                        <p>Already a hero?</p>
                        <Link to="/login" className="auth-link">
                            Continue Journey →
                        </Link>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}

export default Register;
