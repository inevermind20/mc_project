
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AssistancesPage() {
  const [assistances, setAssistances] = useState([]);
  const [form, setForm] = useState({ equipment_id: '', technician: '', description: '', date: '' });

  useEffect(() => {
    axios.get('/assistances').then(res => setAssistances(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/assistances', form).then(res => {
      setAssistances([...assistances, res.data]);
      setForm({ equipment_id: '', technician: '', description: '', date: '' });
    });
  };

  return (
    <div>
      <h2>Assistências Técnicas</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="ID Equipamento" value={form.equipment_id} onChange={e => setForm({ ...form, equipment_id: e.target.value })} />
        <input placeholder="Técnico" value={form.technician} onChange={e => setForm({ ...form, technician: e.target.value })} />
        <input placeholder="Descrição" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
        <input type="datetime-local" value={form.date} onChange={e => setForm({ ...form, date: e.target.value })} />
        <button type="submit">Adicionar</button>
      </form>
      <ul>
        {assistances.map(a => <li key={a.id}>{a.technician} - {a.description}</li>)}
      </ul>
    </div>
  );
}

export default AssistancesPage;
