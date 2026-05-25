// import { Image } from 'expo-image';
// import { Platform, StyleSheet } from 'react-native';

// import { HelloWave } from '@/components/hello-wave';
// import ParallaxScrollView from '@/components/parallax-scroll-view';
// import { ThemedText } from '@/components/themed-text';
// import { ThemedView } from '@/components/themed-view';
// import { Link } from 'expo-router';

// export default function HomeScreen() {
//   return (
//     <ParallaxScrollView
//       headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
//       headerImage={
//         <Image
//           source={require('@/assets/images/partial-react-logo.png')}
//           style={styles.reactLogo}
//         />
//       }>
//       <ThemedView style={styles.titleContainer}>
//         <ThemedText type="title">Welcome!</ThemedText>
//         <HelloWave />
//       </ThemedView>
//       <ThemedView style={styles.stepContainer}>
//         <ThemedText type="subtitle">Step 1: Try it</ThemedText>
//         <ThemedText>
//           Edit <ThemedText type="defaultSemiBold">app/(tabs)/index.tsx</ThemedText> to see changes.
//           Press{' '}
//           <ThemedText type="defaultSemiBold">
//             {Platform.select({
//               ios: 'cmd + d',
//               android: 'cmd + m',
//               web: 'F12',
//             })}
//           </ThemedText>{' '}
//           to open developer tools.
//         </ThemedText>
//       </ThemedView>
//       <ThemedView style={styles.stepContainer}>
//         <Link href="/modal">
//           <Link.Trigger>
//             <ThemedText type="subtitle">Step 2: Explore</ThemedText>
//           </Link.Trigger>
//           <Link.Preview />
//           <Link.Menu>
//             <Link.MenuAction title="Action" icon="cube" onPress={() => alert('Action pressed')} />
//             <Link.MenuAction
//               title="Share"
//               icon="square.and.arrow.up"
//               onPress={() => alert('Share pressed')}
//             />
//             <Link.Menu title="More" icon="ellipsis">
//               <Link.MenuAction
//                 title="Delete"
//                 icon="trash"
//                 destructive
//                 onPress={() => alert('Delete pressed')}
//               />
//             </Link.Menu>
//           </Link.Menu>
//         </Link>

//         <ThemedText>
//           {`Tap the Explore tab to learn more about what's included in this starter app.`}
//         </ThemedText>
//       </ThemedView>
//       <ThemedView style={styles.stepContainer}>
//         <ThemedText type="subtitle">Step 3: Get a fresh start</ThemedText>
//         <ThemedText>
//           {`When you're ready, run `}
//           <ThemedText type="defaultSemiBold">npm run reset-project</ThemedText> to get a fresh{' '}
//           <ThemedText type="defaultSemiBold">app</ThemedText> directory. This will move the current{' '}
//           <ThemedText type="defaultSemiBold">app</ThemedText> to{' '}
//           <ThemedText type="defaultSemiBold">app-example</ThemedText>.
//         </ThemedText>
//       </ThemedView>
//     </ParallaxScrollView>
//   );
// }

// const styles = StyleSheet.create({
//   titleContainer: {
//     flexDirection: 'row',
//     alignItems: 'center',
//     gap: 8,
//   },
//   stepContainer: {
//     gap: 8,
//     marginBottom: 8,
//   },
//   reactLogo: {
//     height: 178,
//     width: 290,
//     bottom: 0,
//     left: 0,
//     position: 'absolute',
//   },
// });

import React, { useState } from 'react';
import { StyleSheet, View, TextInput, Button, Alert, Image, Text } from 'react-native';

export default function Page() {
  // 1. Create a state variable to store the text input
  const [prompt, setPrompt] = useState('');

  // This state will hold our image data. It starts as null
  const [imageSource, setImageSource] = useState<string | null>(null);

  // creating hte asynchronous function to halde the API call
  const generateImage = async () => {

    try {
      
      
    // Alert.alert("Status","Starting the generation process...");

    const response = await fetch('http://192.168.4.32:3000/api/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ prompt: prompt}),
    });

    const data = await response.json();

    if (data.image){
        // 1. ADD THESE TWO LINES HERE:
      console.log("=== FRONTEND LOG ===");
      console.log("Image data received! String length:", data.image.length);
      console.log("Start of string looks like:", data.image.substring(0, 50));
      
      setImageSource(data.image);
    } else {
      Alert.alert("Error","No image was returned from the server.");
    }


    } catch (error) {
      Alert.alert("Connection Error","Could not connect to the backend server");

    }

  };

  return (
    <View style={styles.container}>
      {/* 2. Add the Input component */}
      <TextInput
        style={styles.input}
        placeholder="Type image prompt (e.g., futuristic forest)..."
        value={prompt}
        onChangeText={setPrompt} // Updates the 'prompt' variable instantly as you type
        placeholderTextColor="#888"
      />
      
      {/* Create a new button component */}
      <Button
      title='Generate Image'
      // onPress={()=> Alert.alert("Button Pressed"!, `You typed: ${prompt}`)}/>
      onPress={generateImage}/>

      {/* This is our new Image Display space container */}
      <View style={styles.imageContainer}>
        {imageSource ? (
          // if imagesource has dtaa, show the image component
          <Image source={{uri: imageSource}} style={styles.image} />
        ) : (
          // if imageSource is null, show this friendly text instead
          <Text style={styles.placeholderText}> Your masterpiece will appear here</Text>    
        )}
      </View>
    </View>
    
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    justifyContent: 'center', 
    padding: 20, 
    backgroundColor: '#fff' 
  },
  input: { 
    height: 50, 
    borderColor: '#ccc', 
    borderWidth: 1, 
    paddingHorizontal: 15, 
    borderRadius: 8,
    color: '#000',
    fontSize: 16,
    marginBottom:20,
  },
  // 4. Added styling patterns for our new image box elements
  imageContainer: {
    marginTop: 30,             // Cushion space above the box
    width: '100%',             // Stretch to the full width of the screen padding
    height: 300,               // Make it a nice big square area
    borderWidth: 1,            // Draw a subtle border
    borderColor: '#ddd',       // Light gray border color
    borderRadius: 12,          // Rounded corners
    borderStyle: 'dashed',     // Make the border a dashed line like a placeholder
    justifyContent: 'center',  // Center the text vertically inside
    alignItems: 'center',      // Center the text horizontally inside
    backgroundColor: '#f9f9f9' // Give it a soft background tint
  },
  placeholderText: {
    color: '#999',
    fontSize: 14,
  },
  image: {
    width: '100%',
    height: '100%',
    borderRadius: 12,
    resizeMode: 'cover',       // Make the image scale perfectly to fit the container boundaries
  }
});
