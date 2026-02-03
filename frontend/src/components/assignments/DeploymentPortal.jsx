import { useState } from 'react';
import { motion } from 'framer-motion';
import { submissionsAPI } from '../../api/api';
import './DeploymentPortal.css';

function DeploymentPortal({ assignmentId, onSubmissionComplete }) {
    const [url, setUrl] = useState('');
    const [description, setDescription] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);

        try {
            await submissionsAPI.create({
                assignment_id: assignmentId,
                submission_url: url,
                submission_text: description
            });
            onSubmissionComplete(true);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || "Deployment failed. Check frequency.");
        }
        setSubmitting(false);
    };

    return (
        <div className="deployment-portal glass-card">
            <h3>🚀 Deployment Portal</h3>
            <p className="portal-desc">Submit your artifact for inspection by the Guild.</p>

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Artifact Link (GitHub/Replit URL)</label>
                    <input
                        type="url"
                        value={url}
                        onChange={e => setUrl(e.target.value)}
                        placeholder="https://..."
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Mission Log (Optional)</label>
                    <textarea
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        placeholder="Describe your solution..."
                        rows={3}
                    />
                </div>

                {error && <div className="error-msg">{error}</div>}

                <button
                    type="submit"
                    className={`btn btn-primary btn-block ${submitting ? 'loading' : ''}`}
                    disabled={submitting}
                >
                    {submitting ? 'Transmitting...' : 'Deploy Solution'}
                </button>
            </form>
        </div>
    );
}

export default DeploymentPortal;
