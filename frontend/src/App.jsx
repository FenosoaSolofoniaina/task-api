import { BrowserRouter, Routes, Route } from 'react-router';

import Header from "./components/Header";
import Footer from "./components/Footer";

import LoginPage from "./pages/Login";
import RegisterPage from './pages/Register';
import ForgotPasswordPage from './pages/ForgotPassword';



function App() {
  

  return (
    <BrowserRouter>
      <main className="m-0 p-0 w-[100%] h-[100%] bg-[#FFEFC4]">
        <Header />

          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          </Routes>

        <Footer />
      </main>  
    </BrowserRouter>
  )
}

export default App;