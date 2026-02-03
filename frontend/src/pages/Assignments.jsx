import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { assignmentsAPI, submissionsAPI } from '../api/api';
import { useAuth } from '../context/AuthContext';
import TiltCard from '../components/common/TiltCard';
import SubmissionModal from '../components/assignments/SubmissionModal';
import './Assignments.css';

function Assignments() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [assignments, setAssignments] = useState([]);
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);

    // Modal State
    const [selectedAssignment, setSelectedAssignment] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async (showLoading = true) => {
        if (showLoading) setLoading(true);
        try {
            const [assignRes, subRes] = await Promise.all([
                assignmentsAPI.getUserPending(),
                submissionsAPI.getMy()
            ]);
            setAssignments(assignRes.data);
            setSubmissions(subRes.data);
        } catch (error) {
            console.error("Failed to load assignments", error);
        } finally {
            if (showLoading) setLoading(false);
        }
    };

    const startSubmission = (assignment) => {
        console.log("Starting submission for:", assignment);
        setSelectedAssignment(assignment);
        setIsModalOpen(true);
    };

    const closeSubmission = () => {
        setIsModalOpen(false);
        setTimeout(() => setSelectedAssignment(null), 300); // Wait for animation
    };

    const handleSubmissionSuccess = () => {
        loadData(false); // Refresh silently to update status without unmounting
    };

    if (loading) return <div className="page-centered"><div className="spinner"></div></div>;

    const getSubmissionStatus = (assignmentId) => {
        const sub = submissions.find(s => s.assignment_id === assignmentId);
        if (!sub) return 'not_submitted';
        return sub.status; // pending, graded, etc.
    };

    return (
        <div className="assignments-page">
            <header className="page-header">
                <motion.h1
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                >
                    📜 Royal Bounties
                </motion.h1>
                <p>Complete assignments to earn rewards and reputation.</p>
            </header>

            <div className="assignments-grid">
                {assignments.length === 0 && (
                    <div className="empty-state glass-card">
                        <span className="empty-icon">🛡️</span>
                        <h3>All Quests Clear</h3>
                        <p>You have no pending assignments at the moment. Explore the worlds to find more!</p>
                    </div>
                )}

                {assignments.map((assignment, index) => {
                    const status = getSubmissionStatus(assignment.assignment_id);
                    const isOverdue = assignment.due_date && new Date(assignment.due_date) < new Date();

                    return (
                        <motion.div
                            key={assignment.assignment_id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <div className="assignment-card-wrapper">
                                <TiltCard>
                                    <div className={`bounty-card glass-card ${status} ${isOverdue ? 'overdue' : ''}`}>
                                        <div className="card-badge">
                                            {status === 'completed' && '✅ COMPLETED'}
                                            {status === 'pending' && '⏳ PENDING REVIEW'}
                                            {status === 'not_submitted' && (isOverdue ? '⚠️ OVERDUE' : '📝 ACTIVE')}
                                            {status === 'graded' && '🎖️ GRADED'}
                                        </div>

                                        <h3>{assignment.title}</h3>
                                        <p className="description">{assignment.description}</p>

                                        <div className="card-footer-info">
                                            <div className="rewards">
                                                <span className="reward xp">+{assignment.xp_reward} XP</span>
                                                <span className="reward gold">🪙 {assignment.gold_reward}</span>
                                            </div>
                                            {assignment.due_date && (
                                                <div className="due-date">
                                                    Deadline: {new Date(assignment.due_date).toLocaleDateString()}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </TiltCard>

                                <div className="assignment-action-bar">
                                    {status === 'not_submitted' || status === 'pending_review' || status === 'rejected' ? (
                                        status === 'not_submitted' ? (
                                            <button
                                                className="btn btn-primary btn-block"
                                                onClick={() => startSubmission(assignment)}
                                            >
                                                Submit Assignment
                                            </button>
                                        ) : (
                                            <Link
                                                className="btn btn-primary btn-block"
                                                to={`/assignment/${assignment.assignment_id}`}
                                            >
                                                View Submission
                                            </Link>
                                        )
                                    ) : (
                                        <Link
                                            className="btn btn-outline btn-block"
                                            to={`/assignment/${assignment.assignment_id}`}
                                        >
                                            {status === 'graded' ? 'View Results' : 'View Submission'}
                                        </Link>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    );
                })}
            </div>

            {/* Submission Modal */}
            {selectedAssignment && (
                <SubmissionModal
                    assignment={selectedAssignment}
                    isOpen={isModalOpen}
                    onClose={closeSubmission}
                    onSuccess={handleSubmissionSuccess}
                />
            )}
        </div>
    );
}

export default Assignments;
