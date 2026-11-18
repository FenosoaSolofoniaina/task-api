import { BrowserRouter, Routes, Route } from 'react-router';

import IndexPage from './pages/Index';
import LoginPage from "./pages/Login";
import ErrorPage from './pages/Error';
import ForgotPasswordPage from './pages/ForgotPassword';
import RegisterMePage from './pages/Register';


function App() {
  

  return (
    <BrowserRouter>
      <main className="m-0 p-0 w-[100%] h-[100%] bg-[#FFEFC4]">

        <Routes>
          <Route path="/" element={<IndexPage />} />
          <Route path="/error" element={<ErrorPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register/me" element={<RegisterMePage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Routes>

      </main>  
    </BrowserRouter>
  )
}

export default App;