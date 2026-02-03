import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { assignmentsAPI, submissionsAPI } from '../api/api';
import TiltCard from '../components/common/TiltCard';
import './AssignmentSubmission.css';

function AssignmentSubmission() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [assignment, setAssignment] = useState(null);
    const [submission, setSubmission] = useState(null);
    const [submissionContent, setSubmissionContent] = useState('');
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [isAiGenerating, setIsAiGenerating] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        loadData();
    }, [id]);

    const loadData = async () => {
        setLoading(true);
        try {
            // Fetch Assignment
            const assignRes = await assignmentsAPI.getOne(id);
            setAssignment(assignRes.data);

            // Fetch My Submissions to check status
            const subRes = await submissionsAPI.getMy();
            const mySub = subRes.data.find(s => s.assignment_id === parseInt(id));

            if (mySub) {
                setSubmission(mySub);
                setSubmissionContent(mySub.submission_text || mySub.content || '');
            }
        } catch (err) {
            console.error("Failed to load assignment data", err);
            setError("Could not retrieve the bounty scroll. It may not exist.");
        } finally {
            setLoading(false);
        }
    };

    const handleAiAssist = () => {
        if (submissionContent.trim().length > 10) {
            if (!window.confirm("This will overwrite your current scroll. Continue?")) return;
        }

        setIsAiGenerating(true);
        // Simulate AI delay - In production this would call an API endpoint
        setTimeout(() => {
            setSubmissionContent(
                "🧙‍♂️ **Merlin's Insight:**\n\n" +
                "To solve this quest, consider the following approach:\n" +
                "1. Analyze the core requirements carefully.\n" +
                "2. Break down the problem into smaller magical steps.\n" +
                "3. Implement the solution using standard incantations (code).\n\n" +
                "**Proposed Solution:**\n" +
                "```python\n" +
                "def solve_quest():\n" +
                "    return 'Victory!'\n" +
                "```"
            );
            setIsAiGenerating(false);
        }, 1500);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!submissionContent.trim()) return;

        setSubmitting(true);
        try {
            await submissionsAPI.create({
                assignment_id: parseInt(id),
                submission_text: submissionContent
            });
            setSuccessMessage("Your scroll has been dispatched successfully! 🦅");
            // Reload data to show updated state and navigate back shortly
            setTimeout(() => {
                navigate('/assignments');
            }, 2000);
        } catch (err) {
            console.error("Failed to submit", err);
            if (err.response?.status === 400 && err.response?.data?.detail?.includes("already submitted")) {
                setError("You have already submitted a scroll for this bounty.");
            } else {
                setError("Failed to dispatch the scroll. The guild hall is unreachable.");
            }
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <div className="page-centered"><div className="spinner"></div></div>;

    if (error) {
        return (
            <div className="page-centered">
                <div className="error-card glass-card">
                    <h2>⚠️ Bounty Error</h2>
                    <p>{error}</p>
                    <button className="btn btn-primary" onClick={() => navigate('/assignments')}>Return to Bounties</button>
                </div>
            </div>
        );
    }

    if (!assignment) return null;

    const isSubmitted = !!submission;
    const isGraded = submission?.status === 'graded' || submission?.status === 'approved' || submission?.status === 'rejected';

    return (
        <div className="submission-page">
            <div className="submission-container">
                <button className="back-btn" onClick={() => navigate(-1)}>← Back</button>

                <TiltCard>
                    <div className="assignment-details glass-card">
                        <div className="submission-header">
                            <span className="bounty-label">📜 Royal Bounty</span>
                            <h1>{assignment.title}</h1>
                            <div className="rewards-pill">
                                <span className="reward xp">+{assignment.xp_reward} XP</span>
                                <span className="reward gold">🪙 {assignment.gold_reward} GP</span>
                            </div>
                        </div>

                        <div className="description-section">
                            <h3>Briefing</h3>
                            <p>{assignment.description}</p>
                        </div>

                        {assignment.due_date && (
                            <div className="date-section">
                                <span className="date-icon">📅</span>
                                <span>Deadline: {new Date(assignment.due_date).toLocaleString()}</span>
                            </div>
                        )}
                    </div>
                </TiltCard>

                <motion.div
                    className="submission-form-section glass-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="form-header">
                        <h2>✍️ Your Contribution</h2>
                        {isSubmitted && (
                            <span className={`status-badge ${submission.status}`}>
                                {submission.status.toUpperCase()}
                            </span>
                        )}
                    </div>

                    {successMessage && (
                        <div className="success-banner">
                            {successMessage}
                        </div>
                    )}

                    {!isSubmitted ? (
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                                    <label style={{ margin: 0 }}>Write your solution or paste a link to your scroll:</label>
                                    <button
                                        type="button"
                                        className="btn btn-gold btn-sm"
                                        onClick={handleAiAssist}
                                        disabled={isAiGenerating || submitting}
                                        style={{
                                            fontSize: '0.8rem',
                                            padding: '4px 12px',
                                            background: 'linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%)',
                                            border: '1px solid var(--primary-light)',
                                            color: 'white',
                                            cursor: 'pointer',
                                            borderRadius: '4px'
                                        }}
                                    >
                                        {isAiGenerating ? '🔮 Conjuring...' : '✨ AI Assist'}
                                    </button>
                                </div>
                                <textarea
                                    value={submissionContent}
                                    onChange={e => setSubmissionContent(e.target.value)}
                                    placeholder="Enter your answer here..."
                                    required
                                    disabled={submitting || isAiGenerating}
                                    className="submission-textarea"
                                />
                            </div>

                            <div className="form-actions">
                                <button
                                    type="submit"
                                    className="btn btn-primary btn-lg"
                                    disabled={submitting || !submissionContent.trim()}
                                >
                                    {submitting ? <span className="spinner-small" /> : 'Submit Assignment'}
                                </button>
                            </div>
                        </form>
                    ) : (
                        <div className="submission-view">
                            <p className="submitted-text-label">You submitted:</p>
                            <div className="submitted-content">
                                {submission.submission_text || submission.submission_url || "No content found."}
                            </div>
                            <p className="submitted-date">
                                On {new Date(submission.submitted_at).toLocaleString()}
                            </p>

                            {isGraded && (
                                <div className="grading-result">
                                    <h3>🎖️ Guild Master's Verdict</h3>
                                    <div className="grading-stats">
                                        <div className="grade-score">
                                            Score: <span>{submission.grade_awarded}/{assignment.max_score}</span>
                                        </div>
                                    </div>
                                    {submission.teacher_feedback && (
                                        <div className="grading-feedback">
                                            <p>"{submission.teacher_feedback}"</p>
                                        </div>
                                    )}
                                </div>
                            )}

                            {!isGraded && (
                                <p className="pending-msg">The Guild Masters are currently reviewing your scroll. Check back later!</p>
                            )}
                        </div>
                    )}
                </motion.div>
            </div>
        </div>
    );
}

export default AssignmentSubmission;
