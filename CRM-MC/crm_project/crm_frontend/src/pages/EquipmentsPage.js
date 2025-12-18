
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function EquipmentsPage() {
  const [equipments, setEquipments] = useState([]);
  const [form, setForm] = useState({ name: '', serial_number: '', client_id: '' });

  useEffect(() => {
    axios.get('/equipments').then(res => setEquipments(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/equipments', form).then(res => {
      setEquipments([...equipments, res.data]);
      setForm({ name: '', serial_number: '', client_id: '' });
    });
  };

  return (
    <div>
      <h2>Equipamentos</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Nome" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <input placeholder="Nº Série" value={form.serial_number} onChange={e => setForm({ ...form, serial_number: e.target.value })} />
        <input placeholder="ID Cliente" value={form.client_id} onChange={e => setForm({ ...form, client_id: e.target.value })} />
        <button type="submit">Adicionar</button>
      </form>
      <ul>
        {equipments.map(eq => <li key={eq.id}>{eq.name} - SN: {eq.serial_number}</li>)}
      </ul>
    </div>
  );
}

export default EquipmentsPage;
