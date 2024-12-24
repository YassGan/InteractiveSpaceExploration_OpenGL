# Space Travel Simulator 🌌

An interactive 3D project of space environment using keyboard and voice controls. This simulator utilizes **Pygame**, **Py3D**, and voice recognition with the **Google Speech API** to deliver an immersive experience.

## 🛠️ Features

- **3D Rendering**: Simulation of objects like planets, the sky, and moving cubes.
- **Keyboard Controls**: Free movement in space.
- **Voice Recognition**: Voice command to return to planet Earth.
- **Pinhole Projection**: Visualization of 3D objects on a 2D screen.
- **Transformation Management**:
  - **Translation**: Moving objects.
  - **Rotation**: Rotating around X, Y, Z axes.
- **Clipping and Filling**: Handling out-of-view data and rendering polygons.

## 🎯 Objective

To create an immersive 3D space exploration experience combining advanced graphics and voice interaction.

## 🎮 Usage

1. **Launch**: Run the program with Python.
2. **Explore**: Use keyboard controls to navigate freely.
3. **Voice Command**:
   - Press `Y` to activate voice recognition.
   - Say "Earth" to return to planet Earth.

## 📖 Video Overview

🎥 See the simulation in action on YouTube: [Watch the video](https://youtu.be/5Dm7mlKho_E)

## 🖼️ Technical Details

1. **Modeling and Rendering System**:
   - Geometric modeling using primitives like `BoxGeometry` and `SphereGeometry`.
   - Rendering transforms 3D objects into 2D images.
2. **Projection and Clipping**:
   - Perspective projection with `Camera`.
   - Automatic removal of out-of-view data by Py3D.
3. **Voice Recognition**:
   - Processes voice commands to trigger actions.

## 🚀 Technologies

- **Python**
- **Pygame**
- **Py3D**
- **Google Speech API**

## 📚 Technical Documentation

### Voice Recognition
1. Press `Y` to activate recording.
2. Audio is captured (5 seconds) and stored in a temporary file.
3. The audio is transcribed using the Google Speech API.
4. The keyword "Earth" triggers the return action.

### Clipping and Filling
- Automatically handled by Py3D to optimize image rendering.

## 📈 Future Improvements

- **Planned enhancements**:
  - Integration of an interactive map.
  - Adding animations for movements.
  - Expanding voice command functionality.
