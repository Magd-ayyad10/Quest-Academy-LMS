import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ParticleBackground from '../components/common/ParticleBackground';
import { motion } from 'framer-motion';
import './Auth.css'; // Reusing Auth styles

function TeacherLogin() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        // Call login with 'teacher' role!
        const result = await login(email, password, 'teacher');

        if (result.success) {
            navigate('/teacher/dashboard');
        } else {
            setError(result.error);
        }
        setLoading(false);
    };

    return (
        <div className="auth-page teacher-auth">
            <ParticleBackground count={30} />

            <motion.div
                className="auth-container"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div className="auth-card glass-card">
                    <div className="auth-header">
                        <span className="auth-icon">🎓</span>
                        <h1>Guild Master Access</h1>
                        <p>Enter your credentials to manage the academy</p>
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
                                placeholder="master@questacademy.edu"
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
                            className="btn btn-primary btn-full"
                            disabled={loading}
                        >
                            {loading ? (
                                <span className="spinner-small" />
                            ) : (
                                <>⚡ Enter Studio</>
                            )}
                        </button>
                    </form>

                    <div className="auth-footer">
                        <p>Not a Guild Master?</p>
                        <Link to="/login" className="auth-link">Student Login →</Link>
                    </div>
                </div>

                <div className="auth-decoration">
                    <motion.div
                        className="deco-orb orb-1"
                        animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.8, 0.5] }}
                        transition={{ duration: 3, repeat: Infinity }}
                        style={{ background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)' }}
                    />
                    <motion.div
                        className="deco-orb orb-2"
                        animate={{ scale: [1, 1.3, 1], opacity: [0.3, 0.6, 0.3] }}
                        transition={{ duration: 4, repeat: Infinity }}
                        style={{ background: 'radial-gradient(circle, #ec4899 0%, transparent 70%)' }}
                    />
                </div>
            </motion.div>
        </div>
    );
}

export default TeacherLogin;
