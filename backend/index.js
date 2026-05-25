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

    // extract the prompt or text provided by the user
    const { prompt } = req.body;

    // print it on the console
    console.log(`User requested image for "${prompt}"`);

    // using try catch to prevent the application request to crash
    try {

        // send the prompt to AUTOMATIC1111 API on port 7860
        // fetch is a function that send a JSON payload to the API
        // await allows the server to way for the request to be completed
        const response = await fetch('http://localhost:7860/sdapi/v1/txt2img', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                prompt: prompt,
                steps: 20,
                width: 512,
                height: 512
            })

        });

        
        // converting the raw response into a readable JSON object
        const data =await response.json();

        const base64Image = data.images[0];

        res.json({image: `data:image/png;based=64,${base64Image}`});
        console.log("Success! Image sent back to the phone.");
    } catch (error) {

        console.error("Something went wrong", error);
        res.status(500).json({error: "Failed to connect to Stable diffuion"})
        
    }
});



app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
