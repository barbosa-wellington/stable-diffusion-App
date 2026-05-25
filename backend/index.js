const express = require('express');
const app = express();
const PORT = 3000;

// Allows server to understand json sent from the frontend
app.use(express.json());

// A test route to make sure it works
app.get('/api/test', (req, res) => {
    res.json({message: "Hello for Stable App"});
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});