import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { worldsAPI, assignmentsAPI, submissionsAPI, zonesAPI, questsAPI } from '../api/api';
import './TeacherDashboard.css';

function TeacherDashboard() {
    const { user } = useAuth();
    const [activeTab, setActiveTab] = useState('worlds');

    // Worlds State
    const [myWorlds, setMyWorlds] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showWorldModal, setShowWorldModal] = useState(false);
    const [newWorld, setNewWorld] = useState({
        title: '',
        description: '',
        difficulty_level: 'Easy',
        is_published: false
    });

    // Assignments State
    const [assignments, setAssignments] = useState([]);
    const [assignmentsLoading, setAssignmentsLoading] = useState(false);
    const [showAssignmentModal, setShowAssignmentModal] = useState(false);
    const [selectedAssignment, setSelectedAssignment] = useState(null);
    const [submissions, setSubmissions] = useState([]);

    // Create Assignment State
    const [showCreateAssignmentModal, setShowCreateAssignmentModal] = useState(false);
    const [creationStep, setCreationStep] = useState(1); // 1: Select Location, 2: Details
    const [selectedWorldId, setSelectedWorldId] = useState('');
    const [selectedZoneId, setSelectedZoneId] = useState('');
    const [selectedQuestId, setSelectedQuestId] = useState('');
    const [zones, setZones] = useState([]);
    const [quests, setQuests] = useState([]);

    const [newAssignment, setNewAssignment] = useState({
        title: '',
        description: '',
        max_score: 100,
        xp_reward: 50,
        gold_reward: 50,
        due_date: '',
        required_class: 'All'
    });

    useEffect(() => {
        loadMyWorlds();
    }, [user]);

    useEffect(() => {
        if (activeTab === 'assignments') {
            loadAssignments();
        }
    }, [activeTab]);

    // Load Zones when World changes
    useEffect(() => {
        if (selectedWorldId) {
            loadZones(selectedWorldId);
            setSelectedZoneId('');
            setSelectedQuestId('');
            setQuests([]);
        }
    }, [selectedWorldId]);

    // Load Quests when Zone changes
    useEffect(() => {
        if (selectedZoneId) {
            loadQuests(selectedZoneId);
            setSelectedQuestId('');
        }
    }, [selectedZoneId]);

    const loadMyWorlds = async () => {
        try {
            const res = await worldsAPI.getAll(false);
            // Show all worlds as requested
            setMyWorlds(res.data);
        } catch (error) {
            console.error("Failed to load worlds", error);
        }
        setLoading(false);
    };

    const loadAssignments = async () => {
        setAssignmentsLoading(true);
        try {
            const res = await assignmentsAPI.getTeacherAssignments();
            setAssignments(res.data);
        } catch (error) {
            console.error("Failed to load assignments", error);
        }
        setAssignmentsLoading(false);
    };

    const loadZones = async (worldId) => {
        try {
            const res = await zonesAPI.getByWorld(worldId);
            setZones(res.data);
        } catch (error) {
            console.error("Failed to load zones", error);
        }
    };

    const loadQuests = async (zoneId) => {
        try {
            const res = await questsAPI.getByZone(zoneId);
            setQuests(res.data);
        } catch (error) {
            console.error("Failed to load quests", error);
        }
    };

    const loadSubmissions = async (assignmentId) => {
        try {
            const res = await submissionsAPI.getByAssignment(assignmentId);
            setSubmissions(res.data);
        } catch (error) {
            console.error("Failed to load submissions", error);
        }
    };

    const handleCreateWorld = async (e) => {
        e.preventDefault();
        try {
            await worldsAPI.create(newWorld);
            setShowWorldModal(false);
            setNewWorld({ title: '', description: '', difficulty_level: 'Easy', is_published: false });
            loadMyWorlds();
        } catch (error) {
            alert("Failed to create world");
        }
    };

    const handleCreateAssignment = async (e) => {
        e.preventDefault();
        if (!selectedQuestId) {
            alert("Please select a valid quest first.");
            return;
        }

        try {
            await assignmentsAPI.create({
                ...newAssignment,
                quest_id: parseInt(selectedQuestId),
                due_date: newAssignment.due_date || null
            });
            alert("Assignment created successfully!");
            setShowCreateAssignmentModal(false);
            setNewAssignment({
                title: '',
                description: '',
                max_score: 100,
                xp_reward: 50,
                gold_reward: 50,
                due_date: '',
                required_class: 'All'
            });
            // Reset selection
            setSelectedWorldId('');
            setCreationStep(1);
            loadAssignments();
        } catch (error) {
            console.error("Failed to create assignment", error.response?.data || error.message);
            alert(`Failed to create assignment: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleViewSubmissions = (assignment) => {
        setSelectedAssignment(assignment);
        loadSubmissions(assignment.assignment_id);
        setShowAssignmentModal(true);
    };

    const handleGradeSubmission = async (submissionId, score, feedback) => {
        try {
            const status = 'approved';

            await submissionsAPI.grade(submissionId, {
                grade_awarded: score,
                teacher_feedback: feedback,
                status: status
            });
            loadSubmissions(selectedAssignment.assignment_id);
        } catch (error) {
            console.error("Grading failed", error);
            alert("Failed to grade submission");
        }
    };

    if (loading) return <div className="page-centered"><div className="spinner"></div></div>;

    const tabs = [
        { id: 'worlds', label: '🌍 My Worlds', icon: '🏰' },
        { id: 'assignments', label: '📝 Assignments', icon: '📋' }
    ];

    return (
        <div className="teacher-dashboard">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🏰 Guild Master's Studio</h1>
                    <p>Welcome, {user?.username || 'Guild Master'}. Craft your realms of knowledge here.</p>
                </div>
            </header>

            {/* Tab Navigation */}
            <div className="teacher-tabs">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`teacher-tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <span className="tab-icon">{tab.icon}</span>
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="tab-content">
                {/* WORLDS TAB */}
                {activeTab === 'worlds' && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="worlds-section"
                    >
                        <div className="studio-actions">
                            <button className="btn btn-gold" onClick={() => setShowWorldModal(true)}>
                                + Create New World
                            </button>
                        </div>

                        <div className="worlds-grid">
                            {myWorlds.map((world, index) => (
                                <motion.div
                                    key={world.world_id}
                                    className="studio-card glass-card"
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: index * 0.1 }}
                                >
                                    <span className={`card-status ${world.is_published ? 'published' : 'draft'}`}>
                                        {world.is_published ? '● PUBLISHED' : '● DRAFT'}
                                    </span>
                                    <h3>{world.title}</h3>
                                    <p>{world.description}</p>
                                    <div className="card-stats">
                                        <span>📚 {world.zones_count || 0} Chapters</span>
                                        <span>⚔️ {world.difficulty_level}</span>
                                    </div>
                                    <div className="card-actions">
                                        <Link to={`/teacher/editor/world/${world.world_id}`} className="btn btn-sm btn-ghost">Edit Structure</Link>
                                        <Link to={`/teacher/editor/world/${world.world_id}`} className="btn btn-sm btn-ghost">Manage Content</Link>
                                    </div>
                                </motion.div>
                            ))}

                            {myWorlds.length === 0 && (
                                <div className="empty-state glass-card">
                                    <span className="empty-icon">🏗️</span>
                                    <h3>No Worlds Yet</h3>
                                    <p>Create your first world to start building your curriculum!</p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}

                {/* ASSIGNMENTS TAB */}
                {activeTab === 'assignments' && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="assignments-section"
                    >
                        <div className="section-header">
                            <div>
                                <h2>📝 Assignment Management</h2>
                                <p>Review and grade student submissions for your quests.</p>
                            </div>
                            <button className="btn btn-gold" onClick={() => setShowCreateAssignmentModal(true)}>
                                + New Assignment
                            </button>
                        </div>

                        {assignmentsLoading ? (
                            <div className="page-centered"><div className="spinner"></div></div>
                        ) : (
                            <div className="assignments-list">
                                {assignments.length === 0 ? (
                                    <div className="empty-state glass-card">
                                        <span className="empty-icon">📋</span>
                                        <h3>No Assignments Yet</h3>
                                        <p>Create assignments to see them here.</p>
                                        <button className="btn btn-primary" onClick={() => setShowCreateAssignmentModal(true)}>
                                            Create First Assignment
                                        </button>
                                    </div>
                                ) : (
                                    <table className="assignments-table glass-card">
                                        <thead>
                                            <tr>
                                                <th>Assignment</th>
                                                <th>XP Reward</th>
                                                <th>Gold</th>
                                                <th>Due Date</th>
                                                <th>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {assignments.map(assignment => (
                                                <tr key={assignment.assignment_id}>
                                                    <td>
                                                        <strong>{assignment.title}</strong>
                                                        <span className="assignment-desc">{assignment.description?.substring(0, 50)}...</span>
                                                    </td>
                                                    <td><span className="xp-badge">+{assignment.xp_reward} XP</span></td>
                                                    <td><span className="gold-badge">🪙 {assignment.gold_reward}</span></td>
                                                    <td>
                                                        {assignment.due_date
                                                            ? new Date(assignment.due_date).toLocaleDateString()
                                                            : 'No deadline'
                                                        }
                                                    </td>
                                                    <td>
                                                        <button
                                                            className="btn btn-sm btn-primary"
                                                            onClick={() => handleViewSubmissions(assignment)}
                                                        >
                                                            View Submissions
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                )}
                            </div>
                        )}
                    </motion.div>
                )}
            </div>

            {/* Create World Modal */}
            <AnimatePresence>
                {showWorldModal && (
                    <div className="modal-overlay">
                        <motion.div
                            className="modal-content glass-card"
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                        >
                            <h2>🌍 Forge New World</h2>
                            <form onSubmit={handleCreateWorld}>
                                <div className="form-group">
                                    <label>World Title</label>
                                    <input
                                        value={newWorld.title}
                                        onChange={e => setNewWorld({ ...newWorld, title: e.target.value })}
                                        placeholder="e.g. The Python Peaks"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Description</label>
                                    <textarea
                                        value={newWorld.description}
                                        onChange={e => setNewWorld({ ...newWorld, description: e.target.value })}
                                        placeholder="Describe your world..."
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Difficulty</label>
                                    <select
                                        value={newWorld.difficulty_level}
                                        onChange={e => setNewWorld({ ...newWorld, difficulty_level: e.target.value })}
                                    >
                                        <option>Easy</option>
                                        <option>Medium</option>
                                        <option>Hard</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={newWorld.is_published}
                                            onChange={e => setNewWorld({ ...newWorld, is_published: e.target.checked })}
                                        />
                                        {' '}Publish immediately
                                    </label>
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowWorldModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-primary">Create World</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Create Assignment Modal */}
            <AnimatePresence>
                {showCreateAssignmentModal && (
                    <div className="modal-overlay">
                        <motion.div
                            className="modal-content glass-card"
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                        >
                            <h2>📝 New Assignment</h2>
                            <form onSubmit={handleCreateAssignment}>
                                <div className="form-section">
                                    <h3>📍 Location</h3>
                                    <div className="form-group">
                                        <label>Select World</label>
                                        <select
                                            value={selectedWorldId}
                                            onChange={e => setSelectedWorldId(e.target.value)}
                                            required
                                        >
                                            <option value="">-- Choose World --</option>
                                            {myWorlds.map(w => (
                                                <option key={w.world_id} value={w.world_id}>{w.title}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <div className="form-group">
                                        <label>Select Chapter (Zone)</label>
                                        <select
                                            value={selectedZoneId}
                                            onChange={e => setSelectedZoneId(e.target.value)}
                                            disabled={!selectedWorldId}
                                            required
                                        >
                                            <option value="">-- Choose Chapter --</option>
                                            {zones.map(z => (
                                                <option key={z.zone_id} value={z.zone_id}>{z.title}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <div className="form-group">
                                        <label>Select Lesson (Quest)</label>
                                        <select
                                            value={selectedQuestId}
                                            onChange={e => setSelectedQuestId(e.target.value)}
                                            disabled={!selectedZoneId}
                                            required
                                        >
                                            <option value="">-- Choose Lesson --</option>
                                            {quests.map(q => (
                                                <option key={q.quest_id} value={q.quest_id}>{q.title}</option>
                                            ))}
                                        </select>
                                    </div>
                                </div>

                                <div className="form-section" style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                                    <h3>📄 Details</h3>
                                    <div className="form-group">
                                        <label>Title</label>
                                        <input value={newAssignment.title} onChange={e => setNewAssignment({ ...newAssignment, title: e.target.value })} required placeholder="Assignment Title" />
                                    </div>
                                    <div className="form-group">
                                        <label>Instructions</label>
                                        <textarea value={newAssignment.description} onChange={e => setNewAssignment({ ...newAssignment, description: e.target.value })} required placeholder="What should the hero do?" rows={3} />
                                    </div>
                                    <div className="form-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
                                        <div className="form-group">
                                            <label>Max Score</label>
                                            <input type="number" value={newAssignment.max_score} onChange={e => setNewAssignment({ ...newAssignment, max_score: parseInt(e.target.value) || 0 })} min={1} required />
                                        </div>
                                        <div className="form-group">
                                            <label>XP Reward</label>
                                            <input type="number" value={newAssignment.xp_reward} onChange={e => setNewAssignment({ ...newAssignment, xp_reward: parseInt(e.target.value) || 0 })} min={0} />
                                        </div>
                                        <div className="form-group">
                                            <label>Gold Reward</label>
                                            <input type="number" value={newAssignment.gold_reward} onChange={e => setNewAssignment({ ...newAssignment, gold_reward: parseInt(e.target.value) || 0 })} min={0} />
                                        </div>
                                    </div>
                                    <div className="form-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                                        <div className="form-group">
                                            <label>Due Date</label>
                                            <input type="datetime-local" value={newAssignment.due_date} onChange={e => setNewAssignment({ ...newAssignment, due_date: e.target.value })} />
                                        </div>
                                        <div className="form-group">
                                            <label>Class Restriction</label>
                                            <select
                                                value={newAssignment.required_class}
                                                onChange={e => setNewAssignment({ ...newAssignment, required_class: e.target.value })}
                                            >
                                                <option value="All">All Classes (Universal)</option>
                                                <option value="Warrior">Warrior</option>
                                                <option value="Mage">Mage</option>
                                                <option value="Rogue">Rogue</option>
                                                <option value="Ranger">Ranger</option>
                                                <option value="Healer">Healer</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <div className="modal-actions">
                                    <button type="button" className="btn btn-ghost" onClick={() => setShowCreateAssignmentModal(false)}>Cancel</button>
                                    <button type="submit" className="btn btn-primary" disabled={!selectedQuestId}>Create Assignment</button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Submissions Modal */}
            <AnimatePresence>
                {showAssignmentModal && selectedAssignment && (
                    <div className="modal-overlay">
                        <motion.div
                            className="modal-content glass-card modal-large"
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                        >
                            <h2>📝 Submissions for: {selectedAssignment.title}</h2>

                            {submissions.length === 0 ? (
                                <div className="empty-submissions">
                                    <p>No submissions yet for this assignment.</p>
                                </div>
                            ) : (
                                <div className="submissions-list">
                                    {submissions.map(sub => (
                                        <div key={sub.submission_id} className="submission-card glass-card">
                                            <div className="submission-header">
                                                <span className="student-name">👤 {sub.username || `Hero #${sub.user_id}`}</span>
                                                <span className={`status-badge ${sub.status}`}>{sub.status}</span>
                                            </div>
                                            <div className="submission-content">
                                                <p>{(sub.submission_text || sub.content || '').substring(0, 200)}...</p>
                                            </div>
                                            <div className="submission-meta">
                                                <span>Submitted: {new Date(sub.submitted_at).toLocaleString()}</span>
                                            </div>
                                            {sub.status === 'pending' && (
                                                <div className="grading-form">
                                                    <input
                                                        type="number"
                                                        placeholder="Score"
                                                        max={selectedAssignment.max_score}
                                                        min={0}
                                                        id={`score-${sub.submission_id}`}
                                                    />
                                                    <input
                                                        type="text"
                                                        placeholder="Feedback..."
                                                        id={`feedback-${sub.submission_id}`}
                                                    />
                                                    <button
                                                        className="btn btn-sm btn-gold"
                                                        onClick={() => {
                                                            const score = document.getElementById(`score-${sub.submission_id}`).value;
                                                            const feedback = document.getElementById(`feedback-${sub.submission_id}`).value;
                                                            handleGradeSubmission(sub.submission_id, parseInt(score), feedback);
                                                        }}
                                                    >
                                                        Grade
                                                    </button>
                                                </div>
                                            )}
                                            {['approved', 'rejected', 'graded'].includes(sub.status) && (
                                                <div className="graded-info">
                                                    <span className="score">Score: {sub.grade_awarded}/{selectedAssignment.max_score}</span>
                                                    <span className="feedback">{sub.teacher_feedback}</span>
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            )}

                            <div className="modal-actions">
                                <button className="btn btn-ghost" onClick={() => setShowAssignmentModal(false)}>Close</button>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default TeacherDashboard;
