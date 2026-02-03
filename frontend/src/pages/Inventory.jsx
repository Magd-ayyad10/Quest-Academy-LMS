import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { inventoryAPI as apiInv } from '../api/api';
import { useAuth } from '../context/AuthContext';
import './Inventory.css';


function Inventory() {
    const { refreshUser } = useAuth();
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('all');

    useEffect(() => {
        loadInventory();
    }, []);

    const loadInventory = async () => {
        try {
            const res = await apiInv.getMy();
            setItems(res.data);
        } catch (error) {
            console.error(error);
        }
        setLoading(false);
    };

    const handleEquip = async (itemId, isEquipped) => {
        try {
            await apiInv.equip(itemId, !isEquipped); // Toggle
            await loadInventory();
            await refreshUser(); // Update avatar stats if needed
        } catch (error) {
            console.error(error);
        }
    };

    const filteredItems = activeTab === 'all'
        ? items
        : items.filter(i => i.item.item_type === activeTab);

    if (loading) return <div className="page-centered"><div className="spinner" /></div>;

    return (
        <div className="inventory-page">
            <div className="page-header-simple">
                <h1>🎒 Inventory</h1>
                <p>Manage your gear and consumables</p>
            </div>

            <div className="inventory-tabs">
                {['all', 'weapon', 'armor', 'consumable'].map(tab => (
                    <button
                        key={tab}
                        className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab)}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                ))}
            </div>

            <div className="inventory-grid">
                {filteredItems.length > 0 ? (
                    filteredItems.map((slot) => (
                        <motion.div
                            key={slot.inventory_id}
                            className={`item-card glass-card ${slot.is_equipped ? 'equipped' : ''}`}
                            initial={{ scale: 0.9 }}
                            animate={{ scale: 1 }}
                        >
                            <div className={`item-rarity-strip rarity-${slot.item.rarity}`} />
                            <div className="item-icon">{slot.item.icon}</div>
                            <div className="item-info">
                                <h3>{slot.item.name}</h3>
                                <div className="item-stats">
                                    {slot.item.hp_bonus > 0 && <span>❤️ +{slot.item.hp_bonus} HP</span>}
                                    {slot.item.xp_multiplier > 1 && <span>⭐ +{(slot.item.xp_multiplier - 1) * 100}% XP</span>}
                                </div>
                                <span className="item-qty">x{slot.quantity}</span>
                            </div>
                            <div className="item-actions">
                                {slot.item.item_type !== 'consumable' && (
                                    <button
                                        className={`btn btn-sm ${slot.is_equipped ? 'btn-secondary' : 'btn-primary'}`}
                                        onClick={() => handleEquip(slot.item_id, slot.is_equipped)}
                                    >
                                        {slot.is_equipped ? 'Unequip' : 'Equip'}
                                    </button>
                                )}
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="empty-state">
                        <p>Your inventory is empty. Visit the Shop to buy gear!</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Inventory;
