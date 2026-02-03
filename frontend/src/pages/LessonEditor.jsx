import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { zonesAPI, questsAPI, assignmentsAPI } from '../api/api';
import './LessonEditor.css';

function LessonEditor() {
    const { zoneId } = useParams();
    const [zone, setZone] = useState(null);
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(true);

    // Modal States
    const [showLessonModal, setShowLessonModal] = useState(false);
    const [showAssignmentModal, setShowAssignmentModal] = useState(false);

    const [activeQuestId, setActiveQuestId] = useState(null); // For connecting assignment

    const [newLesson, setNewLesson] = useState({
        title: '',
        content_url: '',
        description: '',
        xp_reward: 100,
        gold_reward: 10,
        order_index: 1,
        ai_narrative_prompt: 'Explain this concept clearly.'
    });

    const [newAssignment, setNewAssignment] = useState({
        title: '',
        description: '',
        max_score: 100,
        xp_reward: 50,
        gold_reward: 50
    });

    useEffect(() => {
        loadZoneData();
    }, [zoneId]);

    const loadZoneData = async () => {
        try {
            const zRes = await zonesAPI.getOne(zoneId);
            setZone(zRes.data);
            const qRes = await questsAPI.getByZone(zoneId);
            setLessons(qRes.data.sort((a, b) => a.order_index - b.order_index));
        } catch (error) {
            console.error("Failed to load lessons", error);
        }
        setLoading(false);
    };

    const handleCreateLesson = async (e) => {
        e.preventDefault();
        try {
            const res = await questsAPI.create({ ...newLesson, zone_id: zoneId });
            setLessons([...lessons, res.data].sort((a, b) => a.order_index - b.order_index));
            setShowLessonModal(false);
            setNewLesson({ title: '', content_url: '', description: '', xp_reward: 100, gold_reward: 10, order_index: lessons.length + 2, ai_narrative_prompt: '' });
        } catch (error) {
            alert("Failed to create lesson");
        }
    };

    const handleAddAssignment = async (e) => {
        e.preventDefault();
        if (!activeQuestId) return;
        try {
            await assignmentsAPI.create({
                ...newAssignment,
                quest_id: activeQuestId,
                // Ensure due_date is set, defaulting to null if not provided
                due_date: newAssignment.due_date || null
            });
            alert("Assignment attached successfully! 📜");
            setShowAssignmentModal(false);
            setNewAssignment({
                title: '',
                description: '',
                max_score: 100,
                xp_reward: 50,
                gold_reward: 50,
                due_date: ''
            });
        } catch (error) {
            console.error("Assignment creation error:", error);
            alert("Failed to add assignment. Please try again.");
        }
    };

    const openAssignmentModal = (questId) => {
        setActiveQuestId(questId);
        setShowAssignmentModal(true);
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="lesson-editor">
            <div className="editor-header">
                <Link to={`/teacher/editor/world/${zone.world_id}`} className="back-link">← Return to Course</Link>
                <h1>Editing: {zone.title}</h1>
                <p>Manage lessons, quizzes, and assignments for this chapter.</p>
            </div>

            <div className="lessons-list">
                {lessons.map(lesson => (
                    <div key={lesson.quest_id} className="lesson-item glass-card">
                        <div className="lesson-main">
                            <h4>{lesson.order_index}. {lesson.title}</h4>
                            <span className="badge-xp">{lesson.xp_reward} XP</span>
                        </div>
                        <div className="lesson-tools">
                            <button
                                className="btn btn-sm btn-ghost"
                                onClick={() => openAssignmentModal(lesson.quest_id)}
                            >
                                📎 Attach Assignment
                            </button>
                            <button className="btn btn-sm btn-ghost">⚔️ Add Quiz Monster</button>
                            <button className="btn btn-sm btn-ghost">✏️ Edit</button>
                        </div>
                    </div>
                ))}

                <button className="btn btn-dashed new-lesson-btn" onClick={() => setShowLessonModal(true)}>
                    + Add New Lesson
                </button>
            </div>

            {/* Create Lesson Modal */}
            {showLessonModal && (
                <div className="modal-overlay">
                    <div className="modal-content glass-card">
                        <h2>New Lesson</h2>
                        <form onSubmit={handleCreateLesson}>
                            <div className="form-group">
                                <label>Title</label>
                                <input value={newLesson.title} onChange={e => setNewLesson({ ...newLesson, title: e.target.value })} required />
                            </div>
                            <div className="form-group">
                                <label>Description (Markdown)</label>
                                <textarea value={newLesson.description} onChange={e => setNewLesson({ ...newLesson, description: e.target.value })} required />
                            </div>
                            <div className="form-group">
                                <label>AI Mentor Prompt</label>
                                <input value={newLesson.ai_narrative_prompt} onChange={e => setNewLesson({ ...newLesson, ai_narrative_prompt: e.target.value })} placeholder="What should the mentor say?" />
                            </div>
                            <div className="modal-actions">
                                <button type="button" className="btn btn-ghost" onClick={() => setShowLessonModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Create Lesson</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Create Assignment Modal */}
            {showAssignmentModal && (
                <div className="modal-overlay">
                    <div className="modal-content glass-card">
                        <h2>Attach Assignment</h2>
                        <form onSubmit={handleAddAssignment}>
                            <div className="form-group">
                                <label>Assignment Title</label>
                                <input
                                    value={newAssignment.title}
                                    onChange={e => setNewAssignment({ ...newAssignment, title: e.target.value })}
                                    maxLength={255}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Instructions</label>
                                <textarea
                                    value={newAssignment.description}
                                    onChange={e => setNewAssignment({ ...newAssignment, description: e.target.value })}
                                    rows={4}
                                    required
                                />
                            </div>
                            <div className="form-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <div className="form-group">
                                    <label>Max Score</label>
                                    <input
                                        type="number"
                                        value={newAssignment.max_score}
                                        onChange={e => setNewAssignment({ ...newAssignment, max_score: parseInt(e.target.value) || 0 })}
                                        min={1}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Due Date</label>
                                    <input
                                        type="datetime-local"
                                        value={newAssignment.due_date ? newAssignment.due_date.substring(0, 16) : ''}
                                        onChange={e => setNewAssignment({ ...newAssignment, due_date: new Date(e.target.value).toISOString() })}
                                    />
                                </div>
                            </div>
                            <div className="form-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <div className="form-group">
                                    <label>XP Reward</label>
                                    <input
                                        type="number"
                                        value={newAssignment.xp_reward}
                                        onChange={e => setNewAssignment({ ...newAssignment, xp_reward: parseInt(e.target.value) || 0 })}
                                        min={0}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Gold Reward</label>
                                    <input
                                        type="number"
                                        value={newAssignment.gold_reward}
                                        onChange={e => setNewAssignment({ ...newAssignment, gold_reward: parseInt(e.target.value) || 0 })}
                                        min={0}
                                    />
                                </div>
                            </div>
                            <div className="modal-actions">
                                <button type="button" className="btn btn-ghost" onClick={() => setShowAssignmentModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Attach Assignment</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default LessonEditor;
