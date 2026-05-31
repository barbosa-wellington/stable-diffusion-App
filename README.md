
# stable-diffusion-App
Stable diffusion app allows users to generate images based on an initial prompt.

<p align='center'>
<img src='mobile/assets/images/sd1-image-new.png' width="500" height="500" alt="App logo" />
</p>


# API

This endpoint allows the user to access the application via network app


# mobile

The mobile folder contains the application frontend and all expo components. You can initialize it by running the command

    npx expo start
    
# backend

The backend contains all the endpoint to access the stable diffusion API

    # ensure to run and initialize the server by runing the command

        node index.js

# Repository directories
```

stable-diffusion-app/
├── mobile/                  <-- Cross-Platform React Native App with Expo 54
│   ├── src/
│   │   └── app/
│   │       └── index.tsx    <-- Core Screen View, Input controls & Render engine hooks
│   ├── tsconfig.json        <-- TypeScript Compilation Configurations 
│   └── package.json         <-- Target Expo Module Dependencies (SDK 54 Compatibility Node)
└── backend/                  <-- Express API Gateway Bridge
    ├── index.js             <-- Network routing server, CORS policies, & Fetch protocols
    └── package.json         <-- Managed runtime modules (Express 5.x & CORS)

```

# Critical Code Architecture References

The Backend Route Engine (server/index.js)

```
app.post('/api/generate', async (req, res) => {
  const { prompt } = req.body;
  try {
    const response = await fetch('http://localhost:7860/sdapi/v1/txt2img', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, steps: 20, width: 512, height: 512 })
    });

    const data = await response.json();
    const base64Image = data.images[0]; 

    // Explicit Base64 formatting passed over raw HTTP JSON wrappers [w6]
    res.json({ image: `data:image/png;base64,${base64Image}` });
  } catch (error) {
    res.status(500).json({ error: "Failed to process image computation" });
  }
});
```


The Client Network Logic Fragment (mobile/src/app/index.tsx)

```
const generateImage = async () => {
  try {
    // Dynamic explicit IP matching ensures packet paths clear standard subnets
    const response = await fetch('http://<YOUR_COMPUTER_LOCAL_IP>:3000/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: prompt }),
    });

    const data = await response.json();
    if (data.image) setImageSource(data.image); // Updates state and initiates rendering [w6]
  } catch (error) {
    Alert.alert("Network Error", "Connection drop intercepted.");
  }
};
```