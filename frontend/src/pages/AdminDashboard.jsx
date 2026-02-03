import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { adminAPI } from '../api/api';
import './AdminDashboard.css';

function AdminDashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('overview');

    // Teachers data
    const [teachers, setTeachers] = useState([]);

    // Items data
    const [items, setItems] = useState([]);

    // Leaderboard data
    const [leaderboard, setLeaderboard] = useState([]);

    // Inventories data
    const [inventories, setInventories] = useState([]);

    // Modal States
    const [showUserModal, setShowUserModal] = useState(false);
    const [showTeacherModal, setShowTeacherModal] = useState(false);
    const [showWorldModal, setShowWorldModal] = useState(false);
    const [showItemModal, setShowItemModal] = useState(false);
    const [showGrantItemModal, setShowGrantItemModal] = useState(false);

    // Form States
    const [newUser, setNewUser] = useState({ username: '', email: '', password: '', avatar_class: 'Warrior' });
    const [newTeacher, setNewTeacher] = useState({ username: '', email: '', password: '', bio: '', specialization: '' });
    const [newWorld, setNewWorld] = useState({ title: '', description: '', difficulty_level: 'Easy', is_published: false, required_class: 'All' });
    const [newItem, setNewItem] = useState({ name: '', description: '', item_type: 'consumable', rarity: 'common', price: 100 });
    const [grantData, setGrantData] = useState({ user_id: '', item_id: '', quantity: 1 });

    const [formError, setFormError] = useState('');

    useEffect(() => {
        loadData();
    }, []);

    useEffect(() => {
        // Load tab-specific data when tab changes
        if (activeTab === 'teachers' && teachers.length === 0) loadTeachers();
        if (activeTab === 'shop' && items.length === 0) loadItems();
        if (activeTab === 'leaderboard' && leaderboard.length === 0) loadLeaderboard();
        if (activeTab === 'inventory' && inventories.length === 0) loadInventories();
    }, [activeTab]);

    const loadData = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await adminAPI.getDashboard();
            setData(res.data);
        } catch (err) {
            console.error("Failed to load admin data", err);
            setError(err.response?.data?.detail || err.message || "Failed to connect to the realm of administration.");
        } finally {
            setLoading(false);
        }
    };

    const loadTeachers = async () => {
        try {
            const res = await adminAPI.getAllTeachers();
            setTeachers(res.data);
        } catch (error) {
            console.error("Failed to load teachers", error);
        }
    };

    const loadItems = async () => {
        try {
            const res = await adminAPI.getAllItems();
            setItems(res.data);
        } catch (error) {
            console.error("Failed to load items", error);
        }
    };

    const loadLeaderboard = async () => {
        try {
            const res = await adminAPI.getLeaderboard();
            setLeaderboard(res.data);
        } catch (error) {
            console.error("Failed to load leaderboard", error);
        }
    };

    const loadInventories = async () => {
        try {
            const res = await adminAPI.getAllInventories();
            setInventories(res.data);
        } catch (error) {
            console.error("Failed to load inventories", error);
        }
    };

    // CRUD Handlers
    const handleDeleteUser = async (id) => {
        if (window.confirm('Are you sure you want to banish this hero forever?')) {
            try {
                await adminAPI.deleteUser(id);
                setData(prev => ({
                    ...prev,
                    recent_users: prev.recent_users.filter(u => u.user_id !== id),
                    stats: { ...prev.stats, total_users: prev.stats.total_users - 1 }
                }));
            } catch (err) {
                alert('Failed to delete user');
            }
        }
    };

    const handleDeleteTeacher = async (id) => {
        if (window.confirm('Are you sure you want to remove this guild master?')) {
            try {
                await adminAPI.deleteTeacher(id);
                setTeachers(prev => prev.filter(t => t.teacher_id !== id));
            } catch (err) {
                alert('Failed to delete teacher');
            }
        }
    };

    const handleDeleteWorld = async (id) => {
        if (window.confirm('Are you sure you want to destroy this world?')) {
            try {
                await adminAPI.deleteWorld(id);
                setData(prev => ({
                    ...prev,
                    recent_worlds: prev.recent_worlds.filter(w => w.world_id !== id),
                    stats: { ...prev.stats, total_worlds: prev.stats.total_worlds - 1 }
                }));
            } catch (err) {
                alert('Failed to delete world');
            }
        }
    };

    const handleDeleteItem = async (id) => {
        if (window.confirm('Are you sure you want to delete this item?')) {
            try {
                await adminAPI.deleteItem(id);
                setItems(prev => prev.filter(i => i.item_id !== id));
            } catch (err) {
                alert('Failed to delete item');
            }
        }
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        setFormError('');
        try {
            await adminAPI.createUser(newUser);
            setShowUserModal(false);
            setNewUser({ username: '', email: '', password: '', avatar_class: 'Warrior' });
            loadData();
        } catch (err) {
            setFormError(err.response?.data?.detail || 'Failed to create hero');
        }
    };

    const handleCreateTeacher = async (e) => {
        e.preventDefault();
        setFormError('');
        try {
            await adminAPI.createTeacher(newTeacher);
            setShowTeacherModal(false);
            setNewTeacher({ username: '', email: '', password: '', bio: '', specialization: '' });
            loadTeachers();
        } catch (err) {
            setFormError(err.response?.data?.detail || 'Failed to create teacher');
        }
    };

    const handleCreateWorld = async (e) => {
        e.preventDefault();
        try {
            await adminAPI.createWorld(newWorld);
            setShowWorldModal(false);
            setNewWorld({ title: '', description: '', difficulty_level: 'Easy', is_published: false, required_class: 'All' });
            loadData();
        } catch (err) {
            alert('Failed to create world');
        }
    };

    const handleCreateItem = async (e) => {
        e.preventDefault();
        try {
            await adminAPI.createItem(newItem);
            setShowItemModal(false);
            setNewItem({ name: '', description: '', item_type: 'consumable', rarity: 'common', price: 100 });
            loadItems();
        } catch (err) {
            alert('Failed to create item');
        }
    };

    const handleGrantItem = async (e) => {
        e.preventDefault();
        try {
            await adminAPI.grantItem(grantData);
            setShowGrantItemModal(false);
            setGrantData({ user_id: '', item_id: '', quantity: 1 });
            loadInventories();
            alert('Item granted successfully!');
        } catch (err) {
            alert('Failed to grant item');
        }
    };

    const handleRecalculateLeaderboard = async () => {
        try {
            const res = await adminAPI.recalculateLeaderboard();
            alert(res.data.message);
            loadLeaderboard();
        } catch (err) {
            alert('Failed to recalculate leaderboard');
        }
    };

    if (loading) return <div className="page-centered"><div className="spinner"></div></div>;

    if (error) {
        return (
            <div className="page-centered">
                <div className="error-card glass-card">
                    <h2>⚠️ Restricted Access or System Error</h2>
                    <p>{error}</p>
                    <button className="btn btn-primary" onClick={loadData}>Retry</button>
                </div>
            </div>
        );
    }

    if (!data) return <div className="page-centered">No data available.</div>;

    const tabs = [
        { id: 'overview', label: '📊 Overview' },
        { id: 'users', label: '👥 Users' },
        { id: 'teachers', label: '🎓 Teachers' },
        { id: 'content', label: '🌍 Worlds' },
        { id: 'shop', label: '🛒 Shop Items' },
        { id: 'leaderboard', label: '🏆 Leaderboard' },
        { id: 'inventory', label: '🎒 Inventories' },
        { id: 'activity', label: '⚡ Activity' }
    ];

    return (
        <div className="admin-dashboard">
            <header className="admin-header">
                <h1>🛡️ System Administration</h1>
                <p>Global oversight of the Quest Academy realm</p>
            </header>

            {/* Admin Tabs */}
            <div className="admin-tabs">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`admin-tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="admin-content">
                {/* OVERVIEW TAB */}
                {activeTab === 'overview' && (
                    <motion.div className="overview-grid" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="stat-card">
                            <h3>Total Users</h3>
                            <div className="stat-value">{data.stats.total_users}</div>
                        </div>
                        <div className="stat-card">
                            <h3>Guild Masters</h3>
                            <div className="stat-value">{data.stats.total_teachers}</div>
                        </div>
                        <div className="stat-card">
                            <h3>Worlds</h3>
                            <div className="stat-value">{data.stats.total_worlds}</div>
                        </div>
                        <div className="stat-card">
                            <h3>Quests</h3>
                            <div className="stat-value">{data.stats.total_quests}</div>
                        </div>
                        <div className="stat-card">
                            <h3>Monsters</h3>
                            <div className="stat-value">{data.stats.total_monsters}</div>
                        </div>
                        <div className="stat-card">
                            <h3>Items Forged</h3>
                            <div className="stat-value">{data.stats.total_items}</div>
                        </div>
                    </motion.div>
                )}

                {/* USERS TAB */}
                {activeTab === 'users' && (
                    <motion.div className="data-table-container glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="table-actions">
                            <button className="btn btn-primary" onClick={() => setShowUserModal(true)}>
                                + Summon New Hero
                            </button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Hero</th>
                                    <th>Class</th>
                                    <th>Level</th>
                                    <th>XP</th>
                                    <th>Gold</th>
                                    <th>Joined</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.recent_users.map(user => (
                                    <tr key={user.user_id}>
                                        <td>#{user.user_id}</td>
                                        <td className="user-cell">
                                            <span className="username">{user.username}</span>
                                            <span className="email">{user.email}</span>
                                        </td>
                                        <td>{user.avatar_class}</td>
                                        <td><span className="badge lvl">Lvl {user.level}</span></td>
                                        <td>{user.current_xp.toLocaleString()}</td>
                                        <td className="gold-text">{user.gold.toLocaleString()}</td>
                                        <td>{new Date(user.created_at).toLocaleDateString()}</td>
                                        <td>
                                            <button className="btn-icon delete" onClick={() => handleDeleteUser(user.user_id)} title="Delete">🗑️</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                )}

                {/* TEACHERS TAB */}
                {activeTab === 'teachers' && (
                    <motion.div className="data-table-container glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="table-actions">
                            <button className="btn btn-primary" onClick={() => setShowTeacherModal(true)}>
                                + Add Guild Master
                            </button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Specialization</th>
                                    <th>Joined</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {teachers.map(teacher => (
                                    <tr key={teacher.teacher_id}>
                                        <td>#{teacher.teacher_id}</td>
                                        <td><strong>{teacher.username}</strong></td>
                                        <td>{teacher.email}</td>
                                        <td>{teacher.specialization || 'General'}</td>
                                        <td>{new Date(teacher.created_at).toLocaleDateString()}</td>
                                        <td>
                                            <button className="btn-icon delete" onClick={() => handleDeleteTeacher(teacher.teacher_id)} title="Delete">🗑️</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                )}

                {/* CONTENT/WORLDS TAB */}
                {activeTab === 'content' && (
                    <motion.div className="data-table-container glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="table-actions">
                            <button className="btn btn-primary" onClick={() => setShowWorldModal(true)}>
                                + Forge New World
                            </button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>World Title</th>
                                    <th>Status</th>
                                    <th>Zones</th>
                                    <th>Quests</th>
                                    <th>Teacher ID</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.recent_worlds.map(world => (
                                    <tr key={world.world_id}>
                                        <td>#{world.world_id}</td>
                                        <td><strong>{world.title}</strong></td>
                                        <td>
                                            <span className={`status-badge ${world.is_published ? 'pub' : 'draft'}`}>
                                                {world.is_published ? 'Published' : 'Draft'}
                                            </span>
                                        </td>
                                        <td>{world.zone_count}</td>
                                        <td>{world.quest_count}</td>
                                        <td>#{world.teacher_id}</td>
                                        <td>
                                            <button className="btn-icon delete" onClick={() => handleDeleteWorld(world.world_id)} title="Delete">🗑️</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                )}

                {/* SHOP ITEMS TAB */}
                {activeTab === 'shop' && (
                    <motion.div className="data-table-container glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="table-actions">
                            <button className="btn btn-primary" onClick={() => setShowItemModal(true)}>
                                + Forge New Item
                            </button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Item Name</th>
                                    <th>Type</th>
                                    <th>Rarity</th>
                                    <th>Price</th>
                                    <th>HP Bonus</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {items.map(item => (
                                    <tr key={item.item_id}>
                                        <td>#{item.item_id}</td>
                                        <td><strong>{item.name}</strong></td>
                                        <td>{item.item_type}</td>
                                        <td><span className={`rarity-badge ${item.rarity}`}>{item.rarity}</span></td>
                                        <td className="gold-text">🪙 {item.price}</td>
                                        <td>{item.hp_bonus > 0 ? `+${item.hp_bonus}` : '-'}</td>
                                        <td>
                                            <button className="btn-icon delete" onClick={() => handleDeleteItem(item.item_id)} title="Delete">🗑️</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                )}

                {/* LEADERBOARD TAB */}
                {activeTab === 'leaderboard' && (
                    <motion.div className="data-table-container glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="table-actions">
                            <button className="btn btn-gold" onClick={handleRecalculateLeaderboard}>
                                🔄 Recalculate Rankings
                            </button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Hero</th>
                                    <th>Total XP</th>
                                    <th>Gold</th>
                                    <th>Quests Done</th>
                                    <th>Monsters Slain</th>
                                </tr>
                            </thead>
                            <tbody>
                                {leaderboard.map((entry, index) => (
                                    <tr key={entry.entry_id}>
                                        <td>
                                            {index === 0 && '🥇'}
                                            {index === 1 && '🥈'}
                                            {index === 2 && '🥉'}
                                            {index > 2 && `#${entry.rank_position || index + 1}`}
                                        </td>
                                        <td><strong>{entry.username}</strong></td>
                                        <td className="xp-text">{entry.total_xp?.toLocaleString()}</td>
                                        <td className="gold-text">🪙 {entry.total_gold?.toLocaleString()}</td>
                                        <td>{entry.quests_completed}</td>
                                        <td>{entry.monsters_defeated}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                )}

                {/* INVENTORY TAB */}
                {activeTab === 'inventory' && (
                    <motion.div className="data-table-container glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="table-actions">
                            <button className="btn btn-primary" onClick={() => setShowGrantItemModal(true)}>
                                🎁 Grant Item to User
                            </button>
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>User</th>
                                    <th>Item</th>
                                    <th>Quantity</th>
                                    <th>Equipped</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {inventories.map(inv => (
                                    <tr key={inv.inventory_id}>
                                        <td>#{inv.inventory_id}</td>
                                        <td>{inv.username}</td>
                                        <td><strong>{inv.item_name}</strong></td>
                                        <td>x{inv.quantity}</td>
                                        <td>{inv.is_equipped ? '✅' : '❌'}</td>
                                        <td>
                                            <button className="btn-icon delete" onClick={() => adminAPI.removeInventory(inv.inventory_id).then(() => loadInventories())} title="Remove">🗑️</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                )}

                {/* ACTIVITY TAB */}
                {activeTab === 'activity' && (
                    <motion.div className="activity-feed glass-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        {data.recent_activity.length === 0 ? (
                            <div style={{ padding: '20px', textAlign: 'center', color: '#888' }}>
                                No recent activity yet. Be the first hero!
                            </div>
                        ) : (
                            data.recent_activity.map(act => (
                                <div key={act.id} className="feed-item">
                                    <div className="feed-time">{new Date(act.created_at).toLocaleString()}</div>
                                    <div className="feed-content">
                                        <strong>{act.username}</strong>
                                        <span className="activity-type"> {act.activity_type.replace(/_/g, ' ')} </span>
                                        : {act.title}
                                        {act.xp_earned > 0 && <span className="xp-tag">+{act.xp_earned} XP</span>}
                                    </div>
                                </div>
                            ))
                        )}
                    </motion.div>
                )}
            </div>

            {/* ============ MODALS ============ */}

            {/* Create User Modal */}
            <AnimatePresence>
                {showUserModal && (
                    <div className="modal-overlay">
                        <motion.div className="modal-content glass-card" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}>
                            <h2>Summon New Hero</h2>
                            {formError && <div className="error-msg">{formError}</div>}
                            <form onSubmit={handleCreateUser}>
                                <div className="form-group">
                                    <label>Hero Name</label>
                                    <input value={newUser.username} onChange={e => setNewUser({ ...newUser, username: e.target.value })} required />
                                </div>
                                <div className="form-group">
                                    <label>Email</label>
                                    <input type="email" value={newUser.email} onChange={e => setNewUser({ ...newUser, email: e.target.value })} required />
                                </div>
                                <div className="form-group">
                                    <label>Password</label>
                                    <input type="password" value={newUser.password} onChange={e => setNewUser({ ...newUser, password: e.target.value })} required />
                                </div>
                                <div className="form-group">
                                    <label>Class</label>
                                    <select value={newUser.avatar_class} onChange={e => setNewUser({ ...newUser, avatar_class: e.target.value })}>
                                        <option>Warrior</option><option>Mage</option><option>Rogue</option><option>Healer</option>
                                    </select>
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowUserModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-primary">Summon</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Create Teacher Modal */}
            <AnimatePresence>
                {showTeacherModal && (
                    <div className="modal-overlay">
                        <motion.div className="modal-content glass-card" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}>
                            <h2>Add Guild Master</h2>
                            {formError && <div className="error-msg">{formError}</div>}
                            <form onSubmit={handleCreateTeacher}>
                                <div className="form-group">
                                    <label>Name</label>
                                    <input value={newTeacher.username} onChange={e => setNewTeacher({ ...newTeacher, username: e.target.value })} required />
                                </div>
                                <div className="form-group">
                                    <label>Email</label>
                                    <input type="email" value={newTeacher.email} onChange={e => setNewTeacher({ ...newTeacher, email: e.target.value })} required />
                                </div>
                                <div className="form-group">
                                    <label>Password</label>
                                    <input type="password" value={newTeacher.password} onChange={e => setNewTeacher({ ...newTeacher, password: e.target.value })} required />
                                </div>
                                <div className="form-group">
                                    <label>Bio</label>
                                    <textarea value={newTeacher.bio} onChange={e => setNewTeacher({ ...newTeacher, bio: e.target.value })} />
                                </div>
                                <div className="form-group">
                                    <label>Specialization</label>
                                    <input value={newTeacher.specialization} onChange={e => setNewTeacher({ ...newTeacher, specialization: e.target.value })} placeholder="e.g. Backend Sorcery" />
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowTeacherModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-primary">Add Master</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Create World Modal */}
            <AnimatePresence>
                {showWorldModal && (
                    <div className="modal-overlay">
                        <motion.div className="modal-content glass-card" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}>
                            <h2>Forge New World</h2>
                            <form onSubmit={handleCreateWorld}>
                                <div className="form-group">
                                    <label>World Title</label>
                                    <input value={newWorld.title} onChange={e => setNewWorld({ ...newWorld, title: e.target.value })} required placeholder="e.g. The Python Peaks" />
                                </div>
                                <div className="form-group">
                                    <label>Description</label>
                                    <input value={newWorld.description} onChange={e => setNewWorld({ ...newWorld, description: e.target.value })} placeholder="Brief description..." />
                                </div>
                                <div className="form-group">
                                    <label>Difficulty</label>
                                    <select value={newWorld.difficulty_level} onChange={e => setNewWorld({ ...newWorld, difficulty_level: e.target.value })}>
                                        <option>Easy</option><option>Medium</option><option>Hard</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>Required Class</label>
                                    <select value={newWorld.required_class} onChange={e => setNewWorld({ ...newWorld, required_class: e.target.value })}>
                                        <option value="All">All Classes</option><option>Warrior</option><option>Mage</option><option>Rogue</option><option>Healer</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>Status</label>
                                    <select value={newWorld.is_published} onChange={e => setNewWorld({ ...newWorld, is_published: e.target.value === 'true' })}>
                                        <option value="false">Draft</option><option value="true">Published</option>
                                    </select>
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowWorldModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-primary">Forge</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Create Item Modal */}
            <AnimatePresence>
                {showItemModal && (
                    <div className="modal-overlay">
                        <motion.div className="modal-content glass-card" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}>
                            <h2>Forge New Item</h2>
                            <form onSubmit={handleCreateItem}>
                                <div className="form-group">
                                    <label>Item Name</label>
                                    <input value={newItem.name} onChange={e => setNewItem({ ...newItem, name: e.target.value })} required placeholder="e.g. Health Potion" />
                                </div>
                                <div className="form-group">
                                    <label>Description</label>
                                    <input value={newItem.description} onChange={e => setNewItem({ ...newItem, description: e.target.value })} placeholder="What does this item do?" />
                                </div>
                                <div className="form-group">
                                    <label>Type</label>
                                    <select value={newItem.item_type} onChange={e => setNewItem({ ...newItem, item_type: e.target.value })}>
                                        <option value="consumable">Consumable</option>
                                        <option value="equipment">Equipment</option>
                                        <option value="cosmetic">Cosmetic</option>
                                        <option value="booster">Booster</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>Rarity</label>
                                    <select value={newItem.rarity} onChange={e => setNewItem({ ...newItem, rarity: e.target.value })}>
                                        <option value="common">Common</option>
                                        <option value="uncommon">Uncommon</option>
                                        <option value="rare">Rare</option>
                                        <option value="epic">Epic</option>
                                        <option value="legendary">Legendary</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>Price (Gold)</label>
                                    <input type="number" value={newItem.price} onChange={e => setNewItem({ ...newItem, price: parseInt(e.target.value) })} min="0" />
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowItemModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-primary">Forge Item</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Grant Item Modal */}
            <AnimatePresence>
                {showGrantItemModal && (
                    <div className="modal-overlay">
                        <motion.div className="modal-content glass-card" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}>
                            <h2>🎁 Grant Item to User</h2>
                            <form onSubmit={handleGrantItem}>
                                <div className="form-group">
                                    <label>User ID</label>
                                    <input type="number" value={grantData.user_id} onChange={e => setGrantData({ ...grantData, user_id: parseInt(e.target.value) })} required min="1" />
                                </div>
                                <div className="form-group">
                                    <label>Item ID</label>
                                    <input type="number" value={grantData.item_id} onChange={e => setGrantData({ ...grantData, item_id: parseInt(e.target.value) })} required min="1" />
                                </div>
                                <div className="form-group">
                                    <label>Quantity</label>
                                    <input type="number" value={grantData.quantity} onChange={e => setGrantData({ ...grantData, quantity: parseInt(e.target.value) })} min="1" />
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowGrantItemModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-gold">Grant Item</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default AdminDashboard;
