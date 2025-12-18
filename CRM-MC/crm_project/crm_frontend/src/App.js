import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ClientsPage from './pages/ClientsPage';
import EquipmentsPage from './pages/EquipmentsPage';
import ProposalsPage from './pages/ProposalsPage';
import AssistancesPage from './pages/AssistancesPage';
import CalendarPage from './pages/CalendarPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/clients" element={<ClientsPage />} />
        <Route path="/equipments" element={<EquipmentsPage />} />
        <Route path="/proposals" element={<ProposalsPage />} />
        <Route path="/assistances" element={<AssistancesPage />} />
        <Route path="/calendar" element={<CalendarPage />} />
      </Routes>
    </Router>
  );
}

export default App;
