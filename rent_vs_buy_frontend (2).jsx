// App.jsx
import React from 'react';
import RentVsBuyChat from './components/RentVsBuyChat';

function App() {
  return (
    <div className="app-container">
      <h1>🏡 Housekeepers: Rent vs Buy</h1>
      <RentVsBuyChat />
    </div>
  );
}

export default App;

// main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// RentVsBuyChat.jsx
import React, { useState } from 'react';

function RentVsBuyChat() {
  const [county, setCounty] = useState('New York, NY');
  const [downPayment, setDownPayment] = useState('');
  const [lifestyle, setLifestyle] = useState('');
  const [prediction, setPrediction] = useState(null);

  const calculateBreakevenFallback = () => {
    // Demo function for now
    return 'Buy';
  };

  const handleSubmit = async () => {
    // Replace fallback with actual Docker API call
    /*
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: JSON.stringify({ county, downPayment, lifestyle }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    setPrediction(data.prediction);
    */

    // Temporary fallback
    const result = calculateBreakevenFallback();
    setPrediction(result);
  };

  return (
    <div className="chat-container">
      <label>County:</label>
      <input value={county} onChange={(e) => setCounty(e.target.value)} />

      <label>Down Payment:</label>
      <input value={downPayment} onChange={(e) => setDownPayment(e.target.value)} />

      <label>Lifestyle:</label>
      <input value={lifestyle} onChange={(e) => setLifestyle(e.target.value)} />

      <button onClick={handleSubmit}>Ask the Housekeepers ✨</button>

      {prediction && <p>Prediction: {prediction}</p>}

      {/* Tableau embed example */}
      {/* <iframe src="YOUR_TABLEAU_DASHBOARD_URL" width="800" height="600"></iframe> */}
    </div>
  );
}

export default RentVsBuyChat;