import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layout
import Layout from './components/layout/Layout';

// Pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Worlds from './pages/Worlds';
import WorldDetail from './pages/WorldDetail';
import ZoneDetail from './pages/ZoneDetail';
import Shop from './pages/Shop';
import Leaderboard from './pages/Leaderboard';
import QuestDetail from './pages/QuestDetail';
import TeacherLogin from './pages/TeacherLogin';
import TeacherDashboard from './pages/TeacherDashboard';
import AdminDashboard from './pages/AdminDashboard';
import CourseEditor from './pages/CourseEditor';
import LessonEditor from './pages/LessonEditor';
import Profile from './pages/Profile';
import Inventory from './pages/Inventory';
import Achievements from './pages/Achievements';
import Assignments from './pages/Assignments';
import AssignmentSubmission from './pages/AssignmentSubmission';
import { ThemeProvider } from './context/ThemeContext';

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="page-centered">
        <div className="spinner" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// Public Route Component (redirect if authenticated)
function PublicRoute({ children }) {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return (
      <div className="page-centered">
        <div className="spinner" />
      </div>
    );
  }

  if (isAuthenticated) {
    if (user?.role === 'teacher') {
      return <Navigate to="/teacher/dashboard" replace />;
    }
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ThemeProvider>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={
              <PublicRoute>
                <Landing />
              </PublicRoute>
            } />
            <Route path="/login" element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } />
            <Route path="/register" element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            } />
            <Route path="/teacher/login" element={
              <PublicRoute>
                <TeacherLogin />
              </PublicRoute>
            } />

            {/* Teacher Routes */}
            <Route path="/teacher/dashboard" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route index element={<TeacherDashboard />} />
            </Route>

            <Route path="/admin" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route index element={<AdminDashboard />} />
            </Route>

            {/* Let's keep them parallel for now to avoid weird nesting issues if not using Outlet correctly in Dashboard */}
            <Route path="/teacher/editor/world/:worldId" element={
              <ProtectedRoute>
                <Layout />
                <CourseEditor />
              </ProtectedRoute>
            } />
            <Route path="/teacher/editor/zone/:zoneId" element={
              <ProtectedRoute>
                <Layout />
                <LessonEditor />
              </ProtectedRoute>
            } />

            {/* Protected Routes with Layout */}
            <Route element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/worlds" element={<Worlds />} />
              <Route path="/worlds/:id" element={<WorldDetail />} />
              <Route path="/zones/:id" element={<ZoneDetail />} />
              <Route path="/quests/:id" element={<QuestDetail />} />
              <Route path="/shop" element={<Shop />} />
              <Route path="/leaderboard" element={<Leaderboard />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/achievements" element={<Achievements />} />
              <Route path="/achievements" element={<Achievements />} />
              <Route path="/assignments" element={<Assignments />} />
              <Route path="/assignment/:id" element={<AssignmentSubmission />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </ThemeProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
