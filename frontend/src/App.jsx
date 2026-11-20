import { BrowserRouter, Routes, Route } from 'react-router';
import { useNavigate, Navigate } from 'react-router';

import IndexPage from './pages/Index';
import LoginPage from "./pages/Login";
import ErrorPage from './pages/Error';
import ForgotPasswordPage from './pages/ForgotPassword';
import RegisterMePage from './pages/RegisterMe';
import RegisterAccountPage from './pages/RegisterAccount';
import Dashboard from './pages/Tasks';

import getEnvData from './config';



function App() {

    function PublicRoute({ children }) {
        let result = children;

        const settings = getEnvData();
        const LS_SESSION = settings.LS_SESSION;
        const LS_USER_INFO_KEY = settings.LS_USER_INFO_KEY;

        const isAuthenticated = localStorage.getItem(LS_SESSION);
        const hasCreateAccount = localStorage.getItem(LS_USER_INFO_KEY);

        if(isAuthenticated) {
            result = <Navigate to="/dashboard/id?redirection=true" replace />
        }
        else if(hasCreateAccount) {
            result = <Navigate to="/register/account?redirection=true" replace />
        }

        return result;
    }


    function AuthentifiedRoute({ children }) {
        let result = children;

        const settings = getEnvData();
        const LS_SESSION = settings.LS_SESSION;
        const isAuthenticated = localStorage.getItem(LS_SESSION);

        if(!isAuthenticated) {
            result = <Navigate to="/login?redirection=true" replace />
        }

        return result;
    }


    function HasCreatedUserAccountRoute({ children }) {
        let result = children;

        const settings = getEnvData();
        const LS_USER_INFO_KEY = settings.LS_USER_INFO_KEY;
        const hasCreateAccount = localStorage.getItem(LS_USER_INFO_KEY);

       if(!hasCreateAccount) {
            result = <Navigate to="/register/me?redirection=true" replace />
        }

        return result;
    }



    return (
        <BrowserRouter>
            <main className="m-0 p-0 w-[100%] h-[100%] bg-[#FFEFC4]">

                <Routes>
                <Route path="/" element={<IndexPage />} />
                <Route path="/error" element={<ErrorPage />} />
                
                <Route path="/login" element={
                    <PublicRoute>
                        <LoginPage />
                    </PublicRoute>
                    }
                />
                <Route path="/register/me" element={
                    <PublicRoute>
                        <RegisterMePage />
                    </PublicRoute>
                    }
                />
                <Route path="/forgot-password" element={
                    <PublicRoute>
                        <ForgotPasswordPage />
                    </PublicRoute>
                    }
                />
                <Route path="/register/account" element={
                    <HasCreatedUserAccountRoute>
                        <RegisterAccountPage />
                    </HasCreatedUserAccountRoute>
                    }
                />
                <Route path="/dashboard/id" element={
                    <AuthentifiedRoute>
                        <Dashboard />
                    </AuthentifiedRoute>
                    }
                />
                </Routes>

            </main>  
        </BrowserRouter>
    )

}

export default App;