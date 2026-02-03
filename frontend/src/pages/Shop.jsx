import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { inventoryAPI } from '../api/api';
import TiltCard from '../components/common/TiltCard';
import './Shop.css';

const RARITY_COLORS = {
    COMMON: '#9ca3af',
    UNCOMMON: '#22c55e',
    RARE: '#3b82f6',
    EPIC: '#8b5cf6',
    LEGENDARY: '#fbbf24',
};

function Shop() {
    const { user, refreshUser } = useAuth();
    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [activeTab, setActiveTab] = useState('shop');
    const [loading, setLoading] = useState(true);
    const [purchasing, setPurchasing] = useState(null);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [shopRes, inventoryRes] = await Promise.all([
                inventoryAPI.getShop(),
                inventoryAPI.getMy(),
            ]);
            setItems(shopRes.data);
            setInventory(inventoryRes.data);
        } catch (error) {
            console.error('Failed to load shop data:', error);
        }
        setLoading(false);
    };

    const handleBuy = async (item) => {
        if (user.gold < item.price) {
            setMessage({ type: 'error', text: 'Not enough gold!' });
            setTimeout(() => setMessage(null), 3000);
            return;
        }

        setPurchasing(item.item_id);
        try {
            await inventoryAPI.buy(item.item_id);
            await refreshUser();
            await loadData();
            setMessage({ type: 'success', text: `Purchased ${item.name}!` });
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Purchase failed' });
        }
        setPurchasing(null);
        setTimeout(() => setMessage(null), 3000);
    };

    const handleEquip = async (itemId, equip) => {
        try {
            await inventoryAPI.equip(itemId, equip);
            await loadData();
            setMessage({ type: 'success', text: equip ? 'Item equipped!' : 'Item unequipped!' });
        } catch (error) {
            setMessage({ type: 'error', text: 'Failed to equip item' });
        }
        setTimeout(() => setMessage(null), 3000);
    };

    if (loading) {
        return (
            <div className="page-centered">
                <div className="spinner" />
            </div>
        );
    }

    return (
        <div className="shop-page">
            <div className="content-wrapper">
                <motion.div
                    className="page-header"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h1>🛒 Merchant's Guild</h1>
                    <div className="gold-display-large">
                        <span className="gold-icon-large">🪙</span>
                        <span>{user?.gold?.toLocaleString()} Gold</span>
                    </div>
                </motion.div>

                {message && (
                    <motion.div
                        className={`shop-message ${message.type}`}
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        {message.type === 'success' ? '✅' : '⚠️'} {message.text}
                    </motion.div>
                )}

                <div className="shop-tabs">
                    <button
                        className={`tab-btn ${activeTab === 'shop' ? 'active' : ''}`}
                        onClick={() => setActiveTab('shop')}
                    >
                        🏪 Shop
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'inventory' ? 'active' : ''}`}
                        onClick={() => setActiveTab('inventory')}
                    >
                        🎒 Inventory ({inventory.length})
                    </button>
                </div>

                {activeTab === 'shop' ? (
                    <motion.div
                        className="items-grid"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        {items.map((item, index) => (
                            <motion.div
                                key={item.item_id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.05 }}
                            >
                                <TiltCard
                                    className="item-card-wrapper"
                                    scale={1.05}
                                >
                                    <div
                                        className="item-card glass-card"
                                        style={{ '--rarity-color': RARITY_COLORS[item.rarity], margin: 0 }}
                                    >
                                        <div className="item-header">
                                            <span className="item-icon">
                                                {item.icon ? item.icon : (
                                                    <>
                                                        {item.item_type === 'weapon' && '⚔️'}
                                                        {item.item_type === 'armor' && '🛡️'}
                                                        {item.item_type === 'consumable' && '🧪'}
                                                        {item.item_type === 'potion' && '🧪'}
                                                        {item.item_type === 'cosmetic' && '✨'}
                                                        {item.item_type === 'boost' && '⚡'}
                                                    </>
                                                )}
                                            </span>
                                            <span className={`rarity-badge ${item.rarity}`}>
                                                {item.rarity}
                                            </span>
                                        </div>

                                        <h3>{item.name}</h3>
                                        <p className="item-desc">{item.description}</p>

                                        <div className="item-stats">
                                            {item.hp_bonus > 0 && (
                                                <span className="item-stat">❤️ +{item.hp_bonus} HP</span>
                                            )}
                                            {item.xp_multiplier > 1 && (
                                                <span className="item-stat">⭐ x{item.xp_multiplier} XP</span>
                                            )}
                                            {item.gold_multiplier > 1 && (
                                                <span className="item-stat">🪙 x{item.gold_multiplier} Gold</span>
                                            )}
                                        </div>

                                        <div className="item-footer">
                                            <span className="item-price">
                                                🪙 {item.price}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="buy-action">
                                        <button
                                            className="btn btn-gold btn-block"
                                            onClick={() => handleBuy(item)}
                                            disabled={purchasing === item.item_id || user.gold < item.price}
                                        >
                                            {purchasing === item.item_id ? 'Buying...' : 'Buy'}
                                        </button>
                                    </div>
                                </TiltCard>
                            </motion.div>
                        ))}
                    </motion.div>
                ) : (
                    <motion.div
                        className="items-grid"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        {inventory.length > 0 ? (
                            inventory.map((inv, index) => (
                                <motion.div
                                    key={inv.inventory_id}
                                    className={`item-card glass-card ${inv.is_equipped ? 'equipped' : ''}`}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    style={{ '--rarity-color': RARITY_COLORS[inv.item.rarity] }}
                                >
                                    {inv.is_equipped && <span className="equipped-badge">Equipped</span>}

                                    <div className="item-header">
                                        <span className="item-icon">
                                            {inv.item.icon ? inv.item.icon : (
                                                <>
                                                    {inv.item.item_type === 'weapon' && '⚔️'}
                                                    {inv.item.item_type === 'armor' && '🛡️'}
                                                    {inv.item.item_type === 'consumable' && '🧪'}
                                                    {inv.item.item_type === 'potion' && '🧪'}
                                                    {inv.item.item_type === 'cosmetic' && '✨'}
                                                    {inv.item.item_type === 'boost' && '⚡'}
                                                </>
                                            )}
                                        </span>
                                        <span className="quantity">x{inv.quantity}</span>
                                    </div>

                                    <h3>{inv.item.name}</h3>

                                    <div className="item-footer">
                                        {inv.item.item_type !== 'consumable' && (
                                            <button
                                                className={`btn ${inv.is_equipped ? 'btn-outline' : 'btn-primary'} btn-sm`}
                                                onClick={() => handleEquip(inv.item.item_id, !inv.is_equipped)}
                                            >
                                                {inv.is_equipped ? 'Unequip' : 'Equip'}
                                            </button>
                                        )}
                                        {inv.item.item_type === 'consumable' && (
                                            <button
                                                className="btn btn-green btn-sm"
                                                onClick={() => inventoryAPI.use(inv.item.item_id).then(() => loadData())}
                                            >
                                                Use
                                            </button>
                                        )}
                                    </div>
                                </motion.div>
                            ))
                        ) : (
                            <div className="empty-state glass-card">
                                <span className="empty-icon">🎒</span>
                                <p>Your inventory is empty. Visit the shop to buy items!</p>
                            </div>
                        )}
                    </motion.div>
                )}
            </div>
        </div>
    );
}

export default Shop;
