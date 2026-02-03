
import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Stars, Float } from '@react-three/drei';
import * as THREE from 'three';
import { useTheme } from '../../context/ThemeContext';

function FloatingCrystal({ position, color, speed = 1 }) {
    const mesh = useRef();

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        mesh.current.rotation.x = time * 0.2 * speed;
        mesh.current.rotation.y = time * 0.1 * speed;
    });

    return (
        <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
            <mesh ref={mesh} position={position}>
                <octahedronGeometry args={[0.5, 0]} />
                <meshStandardMaterial
                    color={color}
                    emissive={color}
                    emissiveIntensity={0.5}
                    transparent
                    opacity={0.8}
                    roughness={0}
                    metalness={0.8}
                />
            </mesh>
        </Float>
    );
}

function RpgBackground() {
    const { theme } = useTheme();
    const isDark = theme === 'dark';

    // Generate random crystals
    const crystals = useMemo(() => {
        return Array.from({ length: 15 }).map((_, i) => ({
            position: [
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 10,
                (Math.random() - 0.5) * 10 - 5
            ],
            color: Math.random() > 0.5 ? '#646cff' : '#a855f7', // Blue or Purple
            speed: 0.5 + Math.random()
        }));
    }, []);

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            zIndex: -50, // Far back
            pointerEvents: 'none',
            background: isDark
                ? 'radial-gradient(circle at 50% 50%, #1a1a2e 0%, #16213e 50%, #050510 100%)'
                : 'radial-gradient(circle at 50% 50%, #f0f4ff 0%, #e6e9ff 50%, #ffffff 100%)'
        }}>
            <Canvas camera={{ position: [0, 0, 10], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} />
                <Stars
                    radius={100}
                    depth={50}
                    count={isDark ? 5000 : 2000}
                    factor={4}
                    saturation={0}
                    fade
                    speed={1}
                />

                {crystals.map((crystal, i) => (
                    <FloatingCrystal
                        key={i}
                        position={crystal.position}
                        color={crystal.color}
                        speed={crystal.speed}
                    />
                ))}

                <fog attach="fog" args={[isDark ? '#050510' : '#ffffff', 5, 25]} />
            </Canvas>
        </div>
    );
}

export default RpgBackground;
