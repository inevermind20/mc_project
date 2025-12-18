import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <ul>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/clients">Clientes</Link></li>
        <li><Link to="/equipments">Equipamentos</Link></li>
        <li><Link to="/proposals">Propostas</Link></li>
        <li><Link to="/assistances">Assistências</Link></li>
        <li><Link to="/calendar">Calendário</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
