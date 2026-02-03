import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ParticleBackground from '../components/common/ParticleBackground';
import { motion, AnimatePresence } from 'framer-motion';
import './Auth.css';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('user'); // 'user' or 'teacher'
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = await login(email, password, role);

        if (result.success) {
            if (role === 'teacher') {
                navigate('/teacher/dashboard');
            } else {
                navigate('/dashboard');
            }
        } else {
            setError(result.error);
        }
        setLoading(false);
    };

    return (
        <div className={`auth-page ${role === 'teacher' ? 'teacher-mode' : ''}`}>
            <ParticleBackground count={40} />

            <motion.div
                className="auth-container"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div className="auth-card glass-card">
                    {/* Role Toggle */}
                    <div className="role-toggle-container">
                        <div className="role-toggle">
                            <button
                                className={`role-btn ${role === 'user' ? 'active' : ''}`}
                                onClick={() => setRole('user')}
                            >
                                🎓 Student
                            </button>
                            <button
                                className={`role-btn ${role === 'teacher' ? 'active' : ''}`}
                                onClick={() => setRole('teacher')}
                            >
                                🧙‍♂️ Guild Master
                            </button>
                        </div>
                    </div>

                    <div className="auth-header">
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={role}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.2 }}
                            >
                                <span className="auth-icon">
                                    {role === 'user' ? '⚔️' : '📜'}
                                </span>
                                <h1>
                                    {role === 'user' ? 'Welcome Back Hero' : 'Guild Master Access'}
                                </h1>
                                <p>
                                    {role === 'user'
                                        ? 'Continue your quest for knowledge'
                                        : 'Enter the studio to forge new realms'}
                                </p>
                            </motion.div>
                        </AnimatePresence>
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
                            <label>Email Address</label>
                            <input
                                type="email"
                                className="input-field"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder={role === 'user' ? "hero@example.com" : "master@questacademy.edu"}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label>Password</label>
                            <input
                                type="password"
                                className="input-field"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            className={`btn btn-full ${role === 'teacher' ? 'btn-gold' : 'btn-primary'}`}
                            disabled={loading}
                        >
                            {loading ? (
                                <span className="spinner-small" />
                            ) : (
                                <>
                                    {role === 'user' ? '🚀 Resume Adventure' : '⚡ Enter Studio'}
                                </>
                            )}
                        </button>
                    </form>

                    <div className="auth-footer">
                        {role === 'user' ? (
                            <>
                                <p>First time here?</p>
                                <Link to="/register" className="auth-link">Create Hero Account →</Link>
                            </>
                        ) : (
                            <>
                                <p>First time here?</p>
                                <span className="auth-link disabled">Contact Admin →</span>
                            </>
                        )}
                    </div>
                </div>

                {/* Decoration Orbs */}
                <div className="auth-decoration">
                    <motion.div
                        className="deco-orb orb-1"
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.5, 0.8, 0.5],
                            background: role === 'user'
                                ? 'radial-gradient(circle, #3b82f6 0%, transparent 70%)'
                                : 'radial-gradient(circle, #d4af37 0%, transparent 70%)'
                        }}
                        transition={{ duration: 3, repeat: Infinity }}
                    />
                    <motion.div
                        className="deco-orb orb-2"
                        animate={{
                            scale: [1, 1.3, 1],
                            opacity: [0.3, 0.6, 0.3],
                            background: role === 'user'
                                ? 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)'
                                : 'radial-gradient(circle, #b8860b 0%, transparent 70%)'
                        }}
                        transition={{ duration: 4, repeat: Infinity }}
                    />
                </div>
            </motion.div>
        </div>
    );
}

export default Login;
