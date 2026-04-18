import { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const ask = async () => {
    const res = await axios.post('http://localhost:8000/chat', { query });
    setAnswer(res.data.answer);
  };
  return (
    <div>
      <h1>Bapuji's Life in Multiverse AI</h1>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button onClick={ask}>Ask</button>
      <p>{answer}</p>
    </div>
  );
}
const [history, setHistory] = useState([]);
useEffect(() => {
  axios.get('http://localhost:8000/history').then(res => setHistory(res.data));
}, []);
const API_URL = "https://bapujiai.onrender.com";  // Your Render URL

// Chat
const res = await axios.post(`${API_URL}/chat`, { query });

// History
axios.get(`${API_URL}/history`).then(res => setHistory(res.data));
// Add <ul>{history.map(h => <li>Q: {h.query}<br/>{h.answer}</li>)}</ul>
