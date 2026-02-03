import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, userAPI, teacherAPI } from '../api/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const role = localStorage.getItem('role') || sessionStorage.getItem('role') || 'user';

        if (token) {
            try {
                // Determine which API to call based on stored role
                const apiCall = role === 'teacher' ? teacherAPI.getMe : userAPI.getMe;
                const response = await apiCall();

                // Ensure we preserve the role in the user object
                setUser({ ...response.data, role });
                setIsAuthenticated(true);
            } catch (error) {
                console.error('Auth check failed:', error);
                // If teacher endpoint fails but we might be a user (or vice versa), 
                // we could try the other, but for now let's just fail safely.
                logout();
            } finally {
                setLoading(false);
            }
        } else {
            setLoading(false);
        }
    };

    const login = async (email, password, role = 'user', remember = false) => {
        try {
            const apiCall = role === 'teacher' ? authAPI.loginTeacher : authAPI.login;
            const response = await apiCall({ email, password });
            const { access_token } = response.data;

            if (remember) {
                localStorage.setItem('token', access_token);
                localStorage.setItem('role', role);
            } else {
                sessionStorage.setItem('token', access_token);
                sessionStorage.setItem('role', role);
            }

            // Fetch profile based on role
            // Note: We need a teacherAPI.getMe() equivalent.
            // For now, if role is teacher, we set user slightly differently or need that endpoint.
            // I will assume userAPI.getMe works for users, and I need to add teacher fetching.
            if (role === 'teacher') {
                // Temporary: We don't have teacherAPI.getMe yet in api.js, 
                // but we can decode token or just assume success for a moment 
                // until I add the API method in the next step.
                // Actually, to make this atomic, I should add the API method first? 
                // No, I can add logic here and it will just fail until I fix api.js 
                // BUT I am an agent, I can do it in order.
                // Let's modify this to fetch correct profile.
                const profileRes = await (role === 'teacher' ? teacherAPI.getMe() : userAPI.getMe());
                setUser({ ...profileRes.data, role });
            } else {
                const userResponse = await userAPI.getMe();
                setUser({ ...userResponse.data, role: 'user' });
            }

            setIsAuthenticated(true);
            return { success: true };
        } catch (error) {
            console.error('Login failed:', error);
            setLoading(false);
            return {
                success: false,
                error: error.response?.data?.detail || 'Login failed'
            };
        } finally {
            setLoading(false);
        }
    };

    const register = async (userData) => {
        try {
            await authAPI.register(userData);
            return await login(userData.email, userData.password, true); // Default to remember on register
        } catch (error) {
            console.error('Registration failed:', error);
            return {
                success: false,
                error: error.response?.data?.detail || 'Registration failed'
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        sessionStorage.removeItem('token');
        setUser(null);
        setIsAuthenticated(false);
    };

    const refreshUser = async () => {
        try {
            const response = await userAPI.getMe();
            setUser(response.data);
        } catch (error) {
            console.error('Failed to refresh user:', error);
        }
    };

    const value = {
        user,
        loading,
        isAuthenticated,
        login,
        register,
        logout,
        refreshUser,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

export default AuthContext;
