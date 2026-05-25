const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Allows server to accept requests from a mobile device
app.use(cors());

// Allows your server to understand JSON data sent from the mobile app
app.use(express.json());

// A test route to make sure it works
app.get('/test', (req, res) => {
  res.json({ status: "The backend bridge is working!" });
});




//  stable diffusion endpoint
// create the post skeleton as the mobile will posting (send) the data to the server
// async for hte server to await for hte request
app.post('/api/generate', async (req, res) => {

})



app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
