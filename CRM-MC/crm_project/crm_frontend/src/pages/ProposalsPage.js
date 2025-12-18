
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ProposalsPage() {
  const [proposals, setProposals] = useState([]);
  const [form, setForm] = useState({ title: '', description: '', client_id: '' });

  useEffect(() => {
    axios.get('/proposals').then(res => setProposals(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/proposals', form).then(res => {
      setProposals([...proposals, res.data]);
      setForm({ title: '', description: '', client_id: '' });
    });
  };

  return (
    <div>
      <h2>Propostas</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Título" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} />
        <input placeholder="Descrição" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
        <input placeholder="ID Cliente" value={form.client_id} onChange={e => setForm({ ...form, client_id: e.target.value })} />
        <button type="submit">Adicionar</button>
      </form>
      <ul>
        {proposals.map(p => <li key={p.id}>{p.title}</li>)}
      </ul>
    </div>
  );
}

export default ProposalsPage;
