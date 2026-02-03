import { useMemo } from 'react';
import './ParticleBackground.css';

function ParticleBackground({ count = 50 }) {
    const particles = useMemo(() => {
        return Array.from({ length: count }, (_, i) => ({
            id: i,
            left: Math.random() * 100,
            delay: Math.random() * 15,
            duration: 15 + Math.random() * 20,
            size: 2 + Math.random() * 4,
        }));
    }, [count]);

    return (
        <>
            <div className="app-background" />
            <div className="particles">
                {particles.map((particle) => (
                    <div
                        key={particle.id}
                        className="particle"
                        style={{
                            left: `${particle.left}%`,
                            width: `${particle.size}px`,
                            height: `${particle.size}px`,
                            animationDelay: `${particle.delay}s`,
                            animationDuration: `${particle.duration}s`,
                        }}
                    />
                ))}
            </div>
        </>
    );
}

export default ParticleBackground;
