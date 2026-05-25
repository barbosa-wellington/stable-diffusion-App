const express = require('express');
const app = express();
const PORT = 3000;

// Allows your server to understand JSON data sent from the mobile app
app.use(express.json());

// A test route to make sure it works
app.get('/api/test', (req, res) => {
  res.json({ message: "Hello from the backend server!" });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
