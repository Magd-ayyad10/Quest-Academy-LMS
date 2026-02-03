import axios from 'axios';

// Use environment variable in production, fallback to /api for local dev (Vite proxy)
const API_BASE_URL = import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/api`
    : '/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            sessionStorage.removeItem('token');
            localStorage.removeItem('user');
            if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: (data) => api.post('/auth/register', data),
    login: (data) => {
        const formData = new URLSearchParams();
        formData.append('username', data.email);
        formData.append('password', data.password);
        return api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
    },
    registerTeacher: (data) => api.post('/auth/teacher/register', data),
    loginTeacher: (data) => {
        const formData = new URLSearchParams();
        formData.append('username', data.email);
        formData.append('password', data.password);
        return api.post('/auth/teacher/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
    },
};

// User API
export const userAPI = {
    getMe: () => api.get('/users/me'),
    updateMe: (data) => api.put('/users/me', data),
    getStats: () => api.get('/users/me/stats'),
    heal: () => api.post('/users/me/heal'),
    getUser: (id) => api.get(`/users/${id}`),
};

export const teacherAPI = {
    getMe: () => api.get('/teachers/me'),
};

// Worlds API
export const worldsAPI = {
    getAll: (publishedOnly = true) => api.get(`/worlds/?published_only=${publishedOnly}`),
    getOne: (id) => api.get(`/worlds/${id}`),
    create: (data) => api.post('/worlds/', data),
    update: (id, data) => api.put(`/worlds/${id}`, data),
    delete: (id) => api.delete(`/worlds/${id}`),
};

// Zones API
export const zonesAPI = {
    getByWorld: (worldId) => api.get(`/zones/world/${worldId}`),
    getOne: (id) => api.get(`/zones/${id}`),
    create: (data) => api.post('/zones', data),
    update: (id, data) => api.put(`/zones/${id}`, data),
    delete: (id) => api.delete(`/zones/${id}`),
};

// Quests API
export const questsAPI = {
    getByZone: (zoneId) => api.get(`/quests/zone/${zoneId}`),
    getOne: (id) => api.get(`/quests/${id}`),
    complete: (id) => api.post(`/quests/${id}/complete`),
    create: (data) => api.post('/quests', data),
    update: (id, data) => api.put(`/quests/${id}`, data),
    delete: (id) => api.delete(`/quests/${id}`),
};

// Monsters API
export const monstersAPI = {
    getBattle: (id) => api.get(`/monsters/${id}/battle`),
    submitAnswer: (id, answer) => api.post(`/monsters/${id}/battle`, { monster_id: id, selected_answer: answer }),
    create: (data) => api.post('/monsters', data),
    update: (id, data) => api.put(`/monsters/${id}`, data),
    delete: (id) => api.delete(`/monsters/${id}`),
};

// Progress API
export const progressAPI = {
    getMy: () => api.get('/progress'),
    getCompleted: () => api.get('/progress/completed'),
    getStats: () => api.get('/progress/stats'),
    getByWorld: (worldId) => api.get(`/progress/world/${worldId}`),
    getTranscript: () => api.get('/progress/transcript'), // New Endpoint
};

// Inventory API
export const inventoryAPI = {
    getShop: () => api.get('/inventory/shop'),
    getMy: () => api.get('/inventory/my'),
    getEquipped: () => api.get('/inventory/equipped'),
    buy: (itemId, quantity = 1) => api.post('/inventory/buy', { item_id: itemId, quantity }),
    equip: (itemId, equip = true) => api.post('/inventory/equip', { item_id: itemId, equip }),
    use: (itemId) => api.post(`/inventory/use/${itemId}`),
};

// Achievements API
export const achievementsAPI = {
    getAll: () => api.get('/achievements'),
    getMy: () => api.get('/achievements/my'),
    getProgress: () => api.get('/achievements/progress'),
};

export const battleAPI = {
    getState: (monsterId) => api.get(`/battle/${monsterId}`),
    attack: (dataset) => api.post('/battle/attack', dataset),
};

// Leaderboard API
export const leaderboardAPI = {
    getGlobal: (limit = 10, offset = 0) => api.get(`/leaderboard?limit=${limit}&offset=${offset}`),
    getByWorld: (worldId, limit = 10, offset = 0) => api.get(`/leaderboard/world/${worldId}?limit=${limit}&offset=${offset}`),
    getMyRank: (worldId = null) => api.get(`/leaderboard/my-rank${worldId ? `?world_id=${worldId}` : ''}`),
};

// Submissions API
export const submissionsAPI = {
    getMy: () => api.get('/submissions/my'),
    getByAssignment: (assignmentId) => api.get(`/submissions/assignment/${assignmentId}`),
    create: (data) => api.post('/submissions/', data),
    grade: (submissionId, data) => api.put(`/submissions/${submissionId}/grade`, data),
};

export const assignmentsAPI = {
    create: (data) => api.post('/assignments/', data),
    getOne: (id) => api.get(`/assignments/${id}`),
    getQuest: (questId) => api.get(`/assignments/quest/${questId}`),
    // Teacher endpoints
    getTeacherAssignments: () => api.get('/assignments/teacher/all'),
    // User endpoints  
    getUserPending: () => api.get('/assignments/user/pending'),
};

// Engagement API
export const engagementAPI = {
    getDashboard: () => api.get('/engagement/dashboard'),
    getMiniLeaderboard: () => api.get('/engagement/leaderboard/mini'),
    logActivity: (data) => api.post('/engagement/activity/log', data),
};

// Admin API - Complete CRUD for all entities
export const adminAPI = {
    getDashboard: () => api.get('/admin/dashboard'),

    // Users
    getAllUsers: () => api.get('/admin/users'),
    createUser: (data) => api.post('/admin/users', data),
    updateUser: (id, data) => api.put(`/admin/users/${id}`, data),
    deleteUser: (id) => api.delete(`/admin/users/${id}`),

    // Teachers
    getAllTeachers: () => api.get('/admin/teachers'),
    createTeacher: (data) => api.post('/admin/teachers', data),
    deleteTeacher: (id) => api.delete(`/admin/teachers/${id}`),

    // Worlds
    getAllWorlds: () => api.get('/admin/dashboard'), // Uses dashboard for world data
    createWorld: (data) => api.post('/admin/worlds', data),
    updateWorld: (id, data) => api.put(`/admin/worlds/${id}`, data),
    deleteWorld: (id) => api.delete(`/admin/worlds/${id}`),

    // Shop Items
    getAllItems: () => api.get('/admin/items'),
    createItem: (data) => api.post('/admin/items', data),
    updateItem: (id, data) => api.put(`/admin/items/${id}`, data),
    deleteItem: (id) => api.delete(`/admin/items/${id}`),

    // Leaderboard
    getLeaderboard: () => api.get('/admin/leaderboard'),
    recalculateLeaderboard: () => api.post('/admin/leaderboard/recalculate'),

    // Inventory
    getAllInventories: () => api.get('/admin/inventory'),
    grantItem: (data) => api.post('/admin/inventory/grant', data),
    removeInventory: (id) => api.delete(`/admin/inventory/${id}`),
};

// Upload API
export const uploadAPI = {
    uploadFile: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');

        // Use raw axios to avoid default Content-Type: application/json from 'api' instance
        return axios.post(`${API_BASE_URL}/upload/file`, formData, {
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                // Do NOT set Content-Type here; axios/browser will set it with boundary
            }
        });
    },
};

// Notifications API
export const notificationsAPI = {
    getAll: (limit = 20) => api.get(`/notifications/?limit=${limit}`),
    getUnreadCount: () => api.get('/notifications/unread-count'),
    markAsRead: (id) => api.put(`/notifications/${id}/read`),
    markAllAsRead: () => api.put('/notifications/read-all'),
    delete: (id) => api.delete(`/notifications/${id}`),
    clearAll: () => api.delete('/notifications/'),
};

export default api;

