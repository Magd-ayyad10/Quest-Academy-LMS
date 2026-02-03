import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { worldsAPI, zonesAPI } from '../api/api';
import './CourseEditor.css';

function CourseEditor() {
    const { worldId } = useParams();
    const [world, setWorld] = useState(null);
    const [zones, setZones] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showZoneModal, setShowZoneModal] = useState(false);
    const [newZone, setNewZone] = useState({ title: '', description: '', order_index: 1 });

    useEffect(() => {
        loadCourseData();
    }, [worldId]);

    const loadCourseData = async () => {
        try {
            const wRes = await worldsAPI.getOne(worldId);
            setWorld(wRes.data);

            // This endpoint logic depends on how backend exposes zones.
            // worldsAPI.getOne might include zones or we use zonesAPI.getByWorld
            // Defaulting to getByWorld to be sure.
            const zRes = await zonesAPI.getByWorld(worldId);
            setZones(zRes.data.sort((a, b) => a.order_index - b.order_index));
        } catch (error) {
            console.error("Failed to load course", error);
        }
        setLoading(false);
    };

    const handleCreateZone = async (e) => {
        e.preventDefault();
        try {
            const res = await zonesAPI.create({ ...newZone, world_id: worldId });
            setZones([...zones, res.data].sort((a, b) => a.order_index - b.order_index));
            setShowZoneModal(false);
            setNewZone({ title: '', description: '', order_index: zones.length + 2 });
        } catch (error) {
            alert("Failed to create zone");
        }
    };

    if (loading) return <div className="spinner"></div>;

    return (
        <div className="course-editor">
            <div className="editor-header">
                <Link to="/teacher/dashboard" className="back-link">← Return to Studio</Link>
                <h1>Editing: {world.title}</h1>
                <p>Structure your curriculum by creating Zones (Chapters).</p>
            </div>

            <div className="zones-list">
                {zones.map(zone => (
                    <div key={zone.zone_id} className="zone-editor-item glass-card">
                        <div className="zone-info">
                            <h3>{zone.order_index}. {zone.title}</h3>
                            <p>{zone.description}</p>
                        </div>
                        <div className="zone-actions">
                            <Link to={`/teacher/editor/zone/${zone.zone_id}`} className="btn btn-gold">
                                Edit Lessons ({zone.quests ? zone.quests.length : 'Manage'})
                            </Link>
                        </div>
                    </div>
                ))}

                <button className="btn btn-dashed new-zone-btn" onClick={() => setShowZoneModal(true)}>
                    + Add New Chapter
                </button>
            </div>

            {/* Create Zone Modal */}
            {showZoneModal && (
                <div className="modal-overlay">
                    <div className="modal-content glass-card">
                        <h2>New Chapter</h2>
                        <form onSubmit={handleCreateZone}>
                            <div className="form-group">
                                <label>Title</label>
                                <input
                                    value={newZone.title}
                                    onChange={e => setNewZone({ ...newZone, title: e.target.value })}
                                    placeholder="Chapter Title"
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Description</label>
                                <textarea
                                    value={newZone.description}
                                    onChange={e => setNewZone({ ...newZone, description: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Order Index</label>
                                <input
                                    type="number"
                                    value={newZone.order_index}
                                    onChange={e => setNewZone({ ...newZone, order_index: parseInt(e.target.value) })}
                                    required
                                />
                            </div>
                            <div className="modal-actions">
                                <button type="button" className="btn btn-ghost" onClick={() => setShowZoneModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Add Chapter</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CourseEditor;
