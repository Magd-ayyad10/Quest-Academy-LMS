import './StatsBar.css';

function StatsBar({ user }) {
    if (!user) return null;

    const xpForNextLevel = 1000;

    // Safety checks
    const hpMax = user.hp_max || 100;
    const hpCurrent = user.hp_current || 0;
    const currentXP = user.current_xp || 0;

    const currentLevelXP = currentXP % xpForNextLevel;

    // Calculate percentages with clamping 0-100
    const rawXpPercent = (currentLevelXP / xpForNextLevel) * 100;
    const rawHpPercent = (hpCurrent / hpMax) * 100;

    const xpPercent = Math.min(100, Math.max(0, isNaN(rawXpPercent) ? 0 : rawXpPercent));
    const hpPercent = Math.min(100, Math.max(0, isNaN(rawHpPercent) ? 0 : rawHpPercent));

    return (
        <div className="stats-bar">
            {/* Level Badge */}
            <div className="level-section">
                <div className="level-badge">{user.level}</div>
                <span className="level-label">Level</span>
            </div>

            {/* HP Bar */}
            <div className="stat-section">
                <div className="stat-header">
                    <span className="stat-icon">❤️</span>
                    <span className="stat-label">HP</span>
                    <span className="stat-value">{user.hp_current} / {user.hp_max}</span>
                </div>
                <div className="stat-bar hp-bar">
                    <div
                        className="stat-bar-fill"
                        style={{ width: `${hpPercent}%` }}
                    />
                </div>
            </div>

            {/* XP Bar */}
            <div className="stat-section">
                <div className="stat-header">
                    <span className="stat-icon">⭐</span>
                    <span className="stat-label">XP</span>
                    <span className="stat-value">{currentLevelXP} / {xpForNextLevel}</span>
                </div>
                <div className="stat-bar xp-bar">
                    <div
                        className="stat-bar-fill"
                        style={{ width: `${xpPercent}%` }}
                    />
                </div>
            </div>

            {/* Gold Counter */}
            <div className="gold-section">
                <div className="gold-counter">
                    <div className="gold-icon" />
                    <span>{user.gold.toLocaleString()}</span>
                </div>
            </div>
        </div>
    );
}

export default StatsBar;
