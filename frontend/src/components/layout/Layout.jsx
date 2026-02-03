import { Outlet } from 'react-router-dom';
import Header from './Header';
import ThreeBackground from '../common/ThreeBackground';
import PageTransition from '../common/PageTransition';
import './Layout.css';

function Layout() {
    return (
        <div className="layout">
            <ThreeBackground />
            <Header />
            <main className="main-content">
                <PageTransition>
                    <Outlet />
                </PageTransition>
            </main>
        </div>
    );
}

export default Layout;
