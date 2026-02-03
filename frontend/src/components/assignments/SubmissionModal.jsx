import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { submissionsAPI, uploadAPI } from '../../api/api';
import './GradingConsole.css';

export default function SubmissionModal({ assignment, isOpen, onClose, onSuccess }) {
    const [content, setContent] = useState('');
    const [file, setFile] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [isAiGenerating, setIsAiGenerating] = useState(false);
    const [error, setError] = useState(null);

    const handleAiAssist = () => {
        if (content.trim().length > 10) {
            if (!window.confirm("This will overwrite your current scroll. Continue?")) return;
        }

        setIsAiGenerating(true);
        setTimeout(() => {
            setContent(
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

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = async (e) => {
        if (e) e.preventDefault();
        console.log("Submitting...", { content, file });

        // Validation: Need either text or file
        if (!content.trim() && !file) {
            setError("You must provide either a text solution or attach a scroll (file).");
            return;
        }

        setSubmitting(true);
        setError(null);

        try {
            let submissionUrl = null;

            // 1. Upload File if present
            if (file) {
                try {
                    const uploadRes = await uploadAPI.uploadFile(file);
                    submissionUrl = uploadRes.data.url;
                } catch (uploadErr) {
                    console.error("Upload failed", uploadErr);
                    let msg = uploadErr.response?.data?.detail || "Failed to upload the attached scroll.";
                    if (typeof msg === 'object') {
                        msg = JSON.stringify(msg);
                    }
                    throw new Error(msg);
                }
            }

            // 2. Submit Assignment
            await submissionsAPI.create({
                assignment_id: assignment.assignment_id,
                submission_text: content,
                submission_url: submissionUrl
            });

            onSuccess();
            onClose();
        } catch (err) {
            console.error("Failed to submit", err);
            // safe access to error message
            let msg = err.response?.data?.detail || err.message || "Failed to dispatch the scroll. The guild hall is unreachable.";

            if (typeof msg === 'object') {
                msg = JSON.stringify(msg);
            }

            setError(msg);
        } finally {
            setSubmitting(false);
        }
    };

    // if (!isOpen) return null; // Removed to allow exit animations via AnimatePresence

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="modal-overlay" style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundColor: 'rgba(0, 0, 0, 0.75)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 2000,
                    backdropFilter: 'blur(5px)'
                }}>
                    <motion.div
                        className="modal-content glass-card"
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        style={{
                            width: '90%',
                            maxWidth: '600px',
                            maxHeight: '90vh',
                            overflowY: 'auto',
                            padding: '30px',
                            position: 'relative',
                            border: '1px solid rgba(255, 255, 255, 0.1)'
                        }}
                    >
                        <button
                            onClick={onClose}
                            style={{
                                position: 'absolute',
                                top: '15px',
                                right: '15px',
                                background: 'transparent',
                                border: 'none',
                                color: 'white',
                                fontSize: '1.5rem',
                                cursor: 'pointer',
                                zIndex: 20
                            }}
                        >
                            ×
                        </button>

                        <h2 style={{ marginBottom: '10px', color: 'white' }}>📜 Submit Assignment</h2>
                        <h3 style={{ color: 'var(--gold)', fontSize: '1.1rem', marginBottom: '20px' }}>
                            {assignment.title}
                        </h3>

                        <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
                            {assignment.description}
                        </p>

                        {error && (
                            <div style={{
                                background: 'rgba(239, 68, 68, 0.2)',
                                color: '#fca5a5',
                                padding: '10px',
                                borderRadius: '6px',
                                marginBottom: '15px'
                            }}>
                                {error}
                            </div>
                        )}

                        <form onSubmit={(e) => e.preventDefault()}>
                            {/* Text Input Section */}
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                                <label style={{ color: 'var(--text-muted)' }}>Your Solution:</label>
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
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                placeholder="Write your solution here..."
                                style={{
                                    width: '100%',
                                    minHeight: '150px',
                                    background: 'rgba(0, 0, 0, 0.4)',
                                    border: '1px solid rgba(255, 255, 255, 0.15)',
                                    borderRadius: '8px',
                                    padding: '15px',
                                    color: 'white',
                                    fontFamily: 'inherit',
                                    fontSize: '1rem',
                                    resize: 'vertical',
                                    marginBottom: '20px'
                                }}
                            />

                            {/* File Upload Section */}
                            <div style={{ marginBottom: '20px' }}>
                                <label style={{ color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>
                                    📎 Attach Scroll (Document/Image):
                                </label>
                                <div style={{
                                    position: 'relative',
                                    overflow: 'hidden',
                                    display: 'inline-block'
                                }}>
                                    <input
                                        type="file"
                                        onChange={handleFileChange}
                                        style={{
                                            color: 'white',
                                            fontSize: '0.9rem'
                                        }}
                                    />
                                </div>
                            </div>

                            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                                <button
                                    type="button"
                                    className="btn btn-outline"
                                    onClick={onClose}
                                    style={{ padding: '10px 20px' }}
                                >
                                    Cancel
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-primary"
                                    onClick={handleSubmit}
                                    disabled={submitting || (!content.trim() && !file)}
                                    style={{ padding: '10px 20px' }}
                                >
                                    {submitting ? 'Dispatching...' : 'Dispatch Scroll'}
                                </button>
                            </div>
                        </form>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
}
