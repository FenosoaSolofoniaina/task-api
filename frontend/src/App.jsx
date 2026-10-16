import { BrowserRouter, Routes, Route } from 'react-router';

import HeaderPage from "./pages/Header";
import FooterPage from "./pages/Footer";

import LoginPage from "./pages/Login";
import RegisterPage from './pages/Register';
import ForgotPasswordPage from './pages/ForgotPassword';



function App() {
  

  return (
    <BrowserRouter>
      <main className="m-0 p-0 w-[100%] h-[100%] bg-[#FFEFC4]">
        <HeaderPage />

        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Routes>

        <FooterPage />
      </main>  
    </BrowserRouter>
  )
}

export default App;