import { Reactlazy, lazy, Suspense} from 'react';
import { HashRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import DashboardPage from 'src/pages/Dasboard/Dashboard';
import LoginPage from 'src/pages/login';

const HomePage = lazy(() => import('src/pages/Home'));

const RouterComponent = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Dashboard />}>
                    <Route index element={<Navigate to="/home" replace />} />
                    <Route path="/home" element={<Suspense fallback={<div>Loading...</div>}><HomePage /></Suspense>} />
                    <Route path="/reports" element={<h2>Reports</h2>} />
                </Route>
                <Route path="/login" element={<Login />} />
            </Routes>
        </Router>
    );
};

const Dashboard = () => {
    const isLoggedIn = localStorage.getItem('token') !== null;

    console.log(isLoggedIn);
    if (!isLoggedIn) {
        return <Navigate to="/login"/>;
    }

    return <DashboardPage />;
};

const Login = () => {
    const isLoggedIn = localStorage.getItem('token') !== null;
    console.log(isLoggedIn);
    if (isLoggedIn) {
        return <Navigate to="/home" replace/>;
    }

    return <LoginPage />;
};

export default RouterComponent;
