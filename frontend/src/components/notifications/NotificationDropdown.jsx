import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { notificationsAPI } from '../../api/api';
import { useNavigate } from 'react-router-dom';
import './NotificationDropdown.css';

function NotificationDropdown() {
    const [isOpen, setIsOpen] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [loading, setLoading] = useState(false);
    const dropdownRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        loadUnreadCount();
        // Poll for new notifications every 30 seconds
        const interval = setInterval(loadUnreadCount, 30000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        // Close dropdown when clicking outside
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const loadUnreadCount = async () => {
        try {
            const res = await notificationsAPI.getUnreadCount();
            setUnreadCount(res.data.unread_count);
        } catch (error) {
            console.error('Failed to load unread count:', error);
        }
    };

    const loadNotifications = async () => {
        setLoading(true);
        try {
            const res = await notificationsAPI.getAll(20);
            setNotifications(res.data);
        } catch (error) {
            console.error('Failed to load notifications:', error);
        }
        setLoading(false);
    };

    const handleToggle = () => {
        if (!isOpen) {
            loadNotifications();
        }
        setIsOpen(!isOpen);
    };

    const handleNotificationClick = async (notification) => {
        // Mark as read
        if (!notification.is_read) {
            try {
                await notificationsAPI.markAsRead(notification.notification_id);
                setNotifications(prev =>
                    prev.map(n =>
                        n.notification_id === notification.notification_id
                            ? { ...n, is_read: true }
                            : n
                    )
                );
                setUnreadCount(prev => Math.max(0, prev - 1));
            } catch (error) {
                console.error('Failed to mark notification as read:', error);
            }
        }

        // Navigate to related content
        if (notification.related_type === 'assignment' && notification.related_id) {
            navigate(`/assignment/${notification.related_id}`);
            setIsOpen(false);
        }
    };

    const handleMarkAllRead = async () => {
        try {
            await notificationsAPI.markAllAsRead();
            setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
            setUnreadCount(0);
        } catch (error) {
            console.error('Failed to mark all as read:', error);
        }
    };

    const handleClearAll = async () => {
        try {
            await notificationsAPI.clearAll();
            setNotifications([]);
            setUnreadCount(0);
        } catch (error) {
            console.error('Failed to clear notifications:', error);
        }
    };

    const formatTime = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className="notification-container" ref={dropdownRef}>
            <button
                className={`notification-btn ${unreadCount > 0 ? 'has-unread' : ''}`}
                onClick={handleToggle}
                aria-label="Notifications"
            >
                <span className="notification-icon">🔔</span>
                {unreadCount > 0 && (
                    <span className="notification-badge">
                        {unreadCount > 99 ? '99+' : unreadCount}
                    </span>
                )}
            </button>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className="notification-dropdown"
                        initial={{ opacity: 0, y: -10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -10, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="notification-header">
                            <h3>🔔 Notifications</h3>
                            <div className="notification-actions">
                                {unreadCount > 0 && (
                                    <button
                                        className="notif-action-btn"
                                        onClick={handleMarkAllRead}
                                        title="Mark all as read"
                                    >
                                        ✓
                                    </button>
                                )}
                                {notifications.length > 0 && (
                                    <button
                                        className="notif-action-btn danger"
                                        onClick={handleClearAll}
                                        title="Clear all"
                                    >
                                        🗑️
                                    </button>
                                )}
                            </div>
                        </div>

                        <div className="notification-list">
                            {loading ? (
                                <div className="notification-loading">
                                    <div className="spinner-small" />
                                    <span>Loading...</span>
                                </div>
                            ) : notifications.length === 0 ? (
                                <div className="notification-empty">
                                    <span className="empty-icon">📭</span>
                                    <p>No notifications yet</p>
                                </div>
                            ) : (
                                notifications.map((notification) => (
                                    <motion.div
                                        key={notification.notification_id}
                                        className={`notification-item ${notification.is_read ? 'read' : 'unread'}`}
                                        onClick={() => handleNotificationClick(notification)}
                                        whileHover={{ backgroundColor: 'rgba(139, 92, 246, 0.1)' }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        <div className="notif-icon">{notification.icon}</div>
                                        <div className="notif-content">
                                            <div className="notif-title">{notification.title}</div>
                                            <div className="notif-message">{notification.message}</div>
                                            <div className="notif-time">{formatTime(notification.created_at)}</div>
                                        </div>
                                        {!notification.is_read && <div className="unread-dot" />}
                                    </motion.div>
                                ))
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default NotificationDropdown;
