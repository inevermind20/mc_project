
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ClientsPage() {
  const [clients, setClients] = useState([]);
  const [form, setForm] = useState({ name: '', email: '', phone: '', company: '' });

  useEffect(() => {
    axios.get('/clients').then(res => setClients(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/clients', form).then(res => {
      setClients([...clients, res.data]);
      setForm({ name: '', email: '', phone: '', company: '' });
    });
  };

  return (
    <div>
      <h2>Clientes</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Nome" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <input placeholder="Email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
        <input placeholder="Telefone" value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} />
        <input placeholder="Empresa" value={form.company} onChange={e => setForm({ ...form, company: e.target.value })} />
        <button type="submit">Adicionar</button>
      </form>
      <ul>
        {clients.map(c => <li key={c.id}>{c.name} - {c.company}</li>)}
      </ul>
    </div>
  );
}

export default ClientsPage;
