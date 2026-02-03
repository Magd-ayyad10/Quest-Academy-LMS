import { Link, useLocation } from 'react-router-dom';
import NavTabs from '../common/NavTabs';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';
import './Header.css';

function Header() {
    const { user, logout, isAuthenticated } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const location = useLocation();

    return (
        <header className="header">
            <div className="header-content">
                {/* Logo */}
                <Link to="/" className="logo">
                    <span className="logo-icon">⚔️</span>
                    <span className="logo-text">Quest Academy</span>
                </Link>

                {/* Navigation */}
                {isAuthenticated && (
                    <NavTabs />
                )}

                {/* User Section */}
                <div className="header-actions">
                    <button className="btn-ghost theme-toggle" onClick={toggleTheme} title="Toggle Theme">
                        {theme === 'dark' ? '☀️' : '🌙'}
                    </button>

                    {isAuthenticated ? (
                        <div className="user-menu">
                            <div className="user-info">
                                <div className="user-avatar">
                                    <span className="avatar-class-icon">
                                        {user?.avatar_class === 'Warrior' && '⚔️'}
                                        {user?.avatar_class === 'Mage' && '🔮'}
                                        {user?.avatar_class === 'Ranger' && '🏹'}
                                        {user?.avatar_class === 'Paladin' && '🛡️'}
                                        {user?.avatar_class === 'Novice' && '👤'}
                                        {!['Warrior', 'Mage', 'Ranger', 'Paladin', 'Novice'].includes(user?.avatar_class) && '👤'}
                                    </span>
                                </div>
                                <div className="user-details">
                                    <span className="user-name">{user?.username}</span>
                                    <span className="user-level">Level {user?.level}</span>
                                </div>
                            </div>
                            <div className="gold-display">
                                <span className="gold-icon-small">🪙</span>
                                <span>{user?.gold?.toLocaleString()}</span>
                            </div>
                            <button onClick={logout} className="btn-ghost logout-btn">
                                Logout
                            </button>
                        </div>
                    ) : (
                        <div className="auth-buttons">
                            <Link to="/login" className="btn btn-ghost">Login</Link>
                            <Link to="/register" className="btn btn-primary">Start Quest</Link>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Header;
