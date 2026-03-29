import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import VerifyPage from './VerifyPage.jsx'
import B2BDashboard from './B2BDashboard.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/verify/:sessionId" element={<VerifyPage />} />
        <Route path="/b2b" element={<B2BDashboard />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
