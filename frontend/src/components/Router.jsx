import { Reactlazy, lazy, Suspense } from 'react';
import { HashRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import DashboardPage from 'src/pages/Dasboard/Dashboard';
import LoginPage from 'src/pages/login';
import UserAdministration from 'src/pages/user/UserAdministration';
import ProtectedRoute from 'src/components/ProtectedRoute';
import FirstLogin from 'src/pages/FirstLogin/FirstLogin';
import CredentialCreation from 'src/pages/Credentials/CredentialCreation';
import CredentialManagement from 'src/pages/Credentials/Credentialmanagement';
import Command from 'src/pages/Commands/Commands';
import RegisterServer from 'src/pages/Servers/RegisterServer';
import PendingRequests from 'src/pages/Credentials/AccessRequests';
const HomePage = lazy(() => import('src/pages/Home'));


const RouterComponent = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Dashboard />}>
                    
                    <Route index element={<Navigate to="/home" replace />} />
                    <Route path="/home" element={<Suspense fallback={<div>Loading...</div>}><HomePage /></Suspense>} />
                    <Route path="/reports" element={<h2>Reports</h2>} />
                    <Route path="/user" element={<Suspense fallback={<div>Loading...</div>}><UserAdministration /></Suspense>} />
                    <Route path="/user-creation" element={<ProtectedRoute allowedRoles={[7]}>
                        <Suspense fallback={<div>Loading...</div>}><UserAdministration /></Suspense>
                    </ProtectedRoute>} />

                    <Route path="/user-credential-creation" element={<ProtectedRoute allowedRoles={[7]}>
                        <Suspense fallback={<div>Loading...</div>}><CredentialCreation /></Suspense>
                    </ProtectedRoute>} />

                    <Route path="/user-credential-management" element={<ProtectedRoute allowedRoles={[7]}>
                        <Suspense fallback={<div>Loading...</div>}><CredentialManagement /></Suspense>
                    </ProtectedRoute>} />

                    <Route path="/server-creation" element={<ProtectedRoute allowedRoles={[7]}>
                        <Suspense fallback={<div>Loading...</div>}><RegisterServer isEditing={false} /></Suspense>
                    </ProtectedRoute>} />

                    <Route path="/server-management" element={<ProtectedRoute allowedRoles={[7]}>
                        <Suspense fallback={<div>Loading...</div>}><RegisterServer isEditing={true} /></Suspense>
                    </ProtectedRoute>} />

                    <Route path="/commands" element={<Suspense fallback={<div>Loading...</div>}><Command /></Suspense>} />
                    <Route path="/first-login/password/:token" element={<FirstLogin />} />


                    <Route path="/Acces-requets" element={<ProtectedRoute allowedRoles={[7,3]}>
                        <Suspense fallback={<div>Loading...</div>}><PendingRequests /></Suspense>
                    </ProtectedRoute>} />
                                    
                </Route>
                <Route path="/login" element={<Login />} />
                <Route path="/unauthorized" element={<Navigate to="/home" />} />
                
                
            </Routes>
        </Router>
    );
};
{}
const Dashboard = () => {
    const isLoggedIn = localStorage.getItem('token') !== null;

    console.log(isLoggedIn);
    if (!isLoggedIn) {
        return <Navigate to="/login" />;
    }

    return <DashboardPage />;
};

const Login = () => {
    const isLoggedIn = localStorage.getItem('token') !== null;
    console.log(isLoggedIn);
    if (isLoggedIn) {
        return <Navigate to="/home" replace />;
    }

    return <LoginPage />;
};

export default RouterComponent;
