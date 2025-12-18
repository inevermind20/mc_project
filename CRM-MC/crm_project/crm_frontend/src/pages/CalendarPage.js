
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CalendarPage() {
  const [events, setEvents] = useState([]);
  const [form, setForm] = useState({ title: '', description: '', start_time: '', end_time: '' });

  useEffect(() => {
    axios.get('/calendar').then(res => setEvents(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/calendar', form).then(res => {
      setEvents([...events, res.data]);
      setForm({ title: '', description: '', start_time: '', end_time: '' });
    });
  };

  return (
    <div>
      <h2>Calendário</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Título" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} />
        <input placeholder="Descrição" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
        <input type="datetime-local" value={form.start_time} onChange={e => setForm({ ...form, start_time: e.target.value })} />
        <input type="datetime-local" value={form.end_time} onChange={e => setForm({ ...form, end_time: e.target.value })} />
        <button type="submit">Adicionar</button>
      </form>
      <ul>
        {events.map(ev => <li key={ev.id}>{ev.title} - {ev.start_time}</li>)}
      </ul>
    </div>
  );
}

export default CalendarPage;
