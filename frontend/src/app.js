const express = require('express');
const axios = require('axios');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const FLASK_API_URL = process.env.FLASK_API_URL || 'http://backend:5000';

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../public')));  // CHANGED THIS LINE

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public', 'index.html'));  // CHANGED THIS LINE
});

app.get('/api/list', async (req, res) => {
  try {
    const response = await axios.get(`${FLASK_API_URL}/api`);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching from Flask backend:', error.message);
    res.status(500).json({ error: 'Failed to fetch data from backend' });
  }
});

app.post('/api/submit', async (req, res) => {
  try {
    const { name, email, message } = req.body;

    // Validate input
    if (!name || !email || !message) {
      return res.status(400).json({ 
        error: 'All fields are required (name, email, message)' 
      });
    }

    // Send data to Flask backend for MongoDB insertion
    const response = await axios.post(`${FLASK_API_URL}/api/submit`, {
      name,
      email,
      message
    });

    res.json({ success: true, data: response.data });
  } catch (error) {
    console.error('Error submitting data to Flask backend:', error.message);
    const errorMessage = error.response?.data?.error || 'Failed to submit data';
    res.status(error.response?.status || 500).json({ error: errorMessage });
  }
});

app.get('/success', (req, res) => {
  res.sendFile(path.join(__dirname, '../public', 'success.html'));  // CHANGED THIS LINE
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend server running on port ${PORT}`);
});