import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { submissionsAPI, assignmentsAPI } from '../api/api';
import './GradingConsole.css';

function GradingConsole({ assignmentId }) {
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedSub, setSelectedSub] = useState(null);
    const [grade, setGrade] = useState({ score: 0, feedback: '', status: 'APPROVED' });

    useEffect(() => {
        loadSubmissions();
    }, [assignmentId]);

    const loadSubmissions = async () => {
        try {
            const res = await submissionsAPI.getByAssignment(assignmentId);
            setSubmissions(res.data);
        } catch (error) {
            console.error("Failed to load submissions", error);
        }
        setLoading(false);
    };

    const handleGrade = async (e) => {
        e.preventDefault();
        if (!selectedSub) return;

        try {
            await submissionsAPI.grade(selectedSub.submission_id, {
                grade_awarded: grade.score,
                teacher_feedback: grade.feedback,
                status: grade.status
            });
            // Refresh list
            loadSubmissions();
            setSelectedSub(null);
        } catch (error) {
            alert("Grading failed");
        }
    };

    if (loading) return <div>Scan in progress...</div>;

    return (
        <div className="grading-console">
            <div className="submissions-list">
                <h3>Incoming Transmissions ({submissions.length})</h3>
                {submissions.map(sub => (
                    <div
                        key={sub.submission_id}
                        className={`sub-item ${selectedSub?.submission_id === sub.submission_id ? 'active' : ''}`}
                        onClick={() => { setSelectedSub(sub); setGrade({ score: 90, feedback: '', status: 'APPROVED' }); }}
                    >
                        <div className="sub-header">
                            <span className="student-id">Cadet #{sub.user_id}</span>
                            <span className={`status-badge ${sub.status.toLowerCase()}`}>{sub.status}</span>
                        </div>
                        <div className="sub-date">{new Date(sub.submitted_at).toLocaleDateString()}</div>
                    </div>
                ))}
            </div>

            <div className="inspector-panel glass-card">
                {selectedSub ? (
                    <>
                        <h3>Inspection Deck</h3>
                        <div className="artifact-details">
                            <a href={selectedSub.submission_url} target="_blank" rel="noopener noreferrer" className="artifact-link">
                                🔗 Open Artifact Protocol
                            </a>
                            <p className="mission-log">"{selectedSub.submission_text}"</p>
                        </div>

                        <form onSubmit={handleGrade} className="grading-form">
                            <div className="form-group">
                                <label>Score</label>
                                <input
                                    type="number"
                                    value={grade.score}
                                    onChange={e => setGrade({ ...grade, score: parseInt(e.target.value) })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Feedback</label>
                                <textarea
                                    value={grade.feedback}
                                    onChange={e => setGrade({ ...grade, feedback: e.target.value })}
                                    placeholder="Evaluation notes..."
                                />
                            </div>
                            <div className="form-group">
                                <label>Verdict</label>
                                <select
                                    value={grade.status}
                                    onChange={e => setGrade({ ...grade, status: e.target.value })}
                                >
                                    <option value="APPROVED">APPROVE</option>
                                    <option value="REJECTED">REJECT</option>
                                    <option value="PENDING">PENDING</option>
                                </select>
                            </div>
                            <button type="submit" className="btn btn-gold">Publish Evaluation</button>
                        </form>
                    </>
                ) : (
                    <div className="select-prompt">Select a transmission to inspect</div>
                )}
            </div>
        </div>
    );
}

export default GradingConsole;
