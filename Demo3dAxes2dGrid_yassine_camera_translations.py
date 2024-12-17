import math
import pathlib
import sys
import pygame
import random
import pyaudio
import wave
import threading
import speech_recognition as sr
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.box import BoxGeometry
from py3d.geometry.sphere import SphereGeometry
from py3d.material.surface import SurfaceMaterial
from py3d.material.texture import TextureMaterial
from py3d.core_ext.texture import Texture
from py3d.extras.movement_rig import MovementRig

# Audio Recording Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "output.wav"

class Example(Base):
    """ Render a main character box with camera control, sky, planets, and random moving boxes. """
    
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene() # The container of our 3d objects
        self.camera = Camera(aspect_ratio=1100 / 800)
        
        pygame.init()

        # Setup the movement rig for the camera
        self.rig = MovementRig() #This allows the camera to move
        self.rig.add(self.camera)

        # Create the main character box (shipping box)
        width, height, depth = 0.05, 0.05, 0.05
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
       
        self.character_position = [29.0, -60, 407.0]
        geometry = BoxGeometry(width, height, depth)
        self.character = Mesh(geometry, material)
        self.character.set_position(self.character_position)
        self.scene.add(self.character)

        # Add random moving boxes
        self.moving_boxes = []
        self.box_positions = []
        self.box_velocities = []
        self.box_rotations = []
        
        # Create random moving boxes
        for _ in range(150):
            # Random size for each box
            box_size = random.uniform(0.2, 1.0)
            box_geometry = BoxGeometry(box_size, box_size, box_size)
            
            # Random color for each box - simplified material properties
            box_color = [random.random(), random.random(), random.random()]
            box_material = SurfaceMaterial(property_dict={
                "baseColor": box_color,
                "useVertexColors": False
            })
            
            box = Mesh(box_geometry, box_material)
            
            # Random initial position
            pos = [
                random.uniform(-100, 100),
                random.uniform(-100, 100),
                random.uniform(-100, 100)
            ]
            box.set_position(pos)
            
            # Random velocity for movement
            velocity = [
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5)
            ]
            
            # Random rotation speeds
            rotation = [
                random.uniform(-0.02, 0.02),
                random.uniform(-0.02, 0.02),
                random.uniform(-0.02, 0.02)
            ]
            
            self.moving_boxes.append(box)
            self.box_positions.append(pos)
            self.box_velocities.append(velocity)
            self.box_rotations.append(rotation)
            self.scene.add(box)

        # Skybox setup
        sky_geometry = SphereGeometry(radius=550)
        sky_material = TextureMaterial(texture=Texture(file_name="sky.jpg"))
        self.sky = Mesh(sky_geometry, sky_material)
        self.sky.set_position([0, 0, 0])
        self.scene.add(self.sky)

        # Planets setup
        self.planets = []

        # Scaling factors
        self.planet_distances = [15, 22, 30, 40, 5, 60]  # Distances for Venus, Earth, Mars, Jupiter, Moon, Sun
        self.planet_sizes = [1.0, 1.0, 0.5, 3.5, 0.27, 10]  # Scaled sizes
        self.planet_orbits = [0.01, 0.01, 0.008, 0.005, 0.1, 0.002]  # Orbital speeds
        
        # Planet textures
        self.planet_textures = {
            "venus": "venus.jpg",
            "earth": "earth.jpg",
            "moon": "moon.jpg",
            "mars": "mars.jpg",
            "jupiter": "jupiter.jpg",
            "sun": "sun.jpg"
        }

        # Create planets
        for i, planet_name in enumerate(self.planet_textures.keys()):
            planet_geometry = SphereGeometry(radius=self.planet_sizes[i]*1.2)
            planet_material = TextureMaterial(texture=Texture(file_name=self.planet_textures[planet_name]))
            planet = Mesh(planet_geometry, planet_material)
            
            x_pos = 1.2 * self.planet_distances[i] * math.cos(i)
            z_pos = 1.2 * self.planet_distances[i] * math.sin(i)
            planet.set_position([x_pos, 0, z_pos])
            self.planets.append(planet)
            self.scene.add(planet)

        # Camera setup
        self.camera_offset = [0, 0.2, 0.5]
        self.accelerate = 0.9
        self.move_speed = 0.50
        
        self.paused = False
        
        # Audio Setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.transcribed_text = ""

        # Earth movement setup
        self.moving_to_earth = False
        self.earth_target = None
        self.movement_speed = 0.5  # Slow movement speed
        

    def start_recording(self):
         if not self.recording:
            self.recording = True
            self.frames = []
            self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            threading.Thread(target=self.record_audio).start()
            
    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            self.save_audio()

    def record_audio(self):
        start_time = time.time()
        while self.recording and (time.time() - start_time) < 5:
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        
        self.stop_recording()

    def save_audio(self):
       with wave.open(OUTPUT_FILENAME, 'wb') as wf:
           wf.setnchannels(CHANNELS)
           wf.setsampwidth(self.audio.get_sample_size(FORMAT))
           wf.setframerate(RATE)
           wf.writeframes(b''.join(self.frames))
       print(f"Audio file saved as {OUTPUT_FILENAME}")
       self.transcribe_and_generate_response()
       
    def transcribe_and_generate_response(self):
        audio_file = OUTPUT_FILENAME
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(audio_file) as source:
                print("Listening...")
                audio_data = recognizer.record(source)

                print("Recognizing...")
                text = recognizer.recognize_google(audio_data)
                self.transcribed_text = text.lower()  # Convert to lowercase for easier matching
                print(f"Transcribed Text: {text}")
                
                # Check if 'earth' is in the transcribed text
                if 'earth' in self.transcribed_text:
                    # Find the Earth planet
                    for i, planet_name in enumerate(list(self.planet_textures.keys())):
                        if self.planet_textures[planet_name] == 'earth.jpg':
                            # Use the stored planet position from initialization
                            self.earth_target = [
                                1.2 * self.planet_distances[i] * math.cos(i),
                                0,
                                1.2 * self.planet_distances[i] * math.sin(i)
                            ]
                            self.moving_to_earth = True
                            print(f"Moving to Earth at position: {self.earth_target}")
                            break

        except sr.UnknownValueError:
                self.transcribed_text = "Could not understand the audio."
        except sr.RequestError as e:
                self.transcribed_text = "Request error. Please try again later."
        
    
    def update(self):
            # Check for pause input
            if self.input.is_key_pressed('space'):
                self.paused = not self.paused
            
            if self.paused:
                return # Skip update if paused
            
            if self.input.is_key_pressed('y'):
                self.start_recording()

            # New logic for moving to Earth
            if self.moving_to_earth and self.earth_target is not None:
                # Calculate direction to Earth
                current_pos = self.character_position  # Use stored position directly
                direction = [
                    self.earth_target[0] - current_pos[0],
                    self.earth_target[1] - current_pos[1],
                    self.earth_target[2] - current_pos[2]
                ]
                
                # Normalize direction
                magnitude = math.sqrt(sum(d**2 for d in direction))
                if magnitude > 0:
                    normalized_direction = [d/magnitude for d in direction]
                
                    # Move towards Earth
                    move_vector = [d * self.movement_speed for d in normalized_direction]
                    self.character_position[0] += move_vector[0]
                    self.character_position[1] += move_vector[1]
                    self.character_position[2] += move_vector[2]
                    
                    # Update character position
                    self.character.set_position(self.character_position)
                    
                    # Check if close to Earth (within a small threshold)
                    if magnitude < 5:  # Increased threshold for easier targeting
                        print("Reached Earth!")
                        self.moving_to_earth = False
                        self.earth_target = None

            # (Rest of the update method remains the same)

            # Update moving boxes
            for i, box in enumerate(self.moving_boxes):
                # Update position based on velocity
                for j in range(3):
                    self.box_positions[i][j] += self.box_velocities[i][j]
                
                # Boundary checking - wrap around
                for j in range(3):
                    if self.box_positions[i][j] > 100:
                        self.box_positions[i][j] = -100
                    elif self.box_positions[i][j] < -100:
                        self.box_positions[i][j] = 100
                
                # Apply position
                box.set_position(self.box_positions[i])
                
                # Apply rotation
                box.rotate_x(self.box_rotations[i][0])
                box.rotate_y(self.box_rotations[i][1])
                box.rotate_z(self.box_rotations[i][2])

            # Handle speed boost
            if self.input.is_key_pressed('r'):
                self.accelerate = 5
            else:
                self.accelerate = 1

            # Character movement
            if self.input.is_key_pressed('i'):
                self.character_position[1] -= self.move_speed * self.accelerate
            elif self.input.is_key_pressed('o'):
                self.character_position[1] += self.move_speed * self.accelerate

            if self.input.is_key_pressed('left'):
                self.character_position[0] -= self.move_speed * self.accelerate
            elif self.input.is_key_pressed('right'):
                self.character_position[0] += self.move_speed * self.accelerate

            if self.input.is_key_pressed('down'):
                self.character_position[2] += self.move_speed * self.accelerate
            elif self.input.is_key_pressed('up'):
                self.character_position[2] -= self.move_speed * self.accelerate

            # Update character position
            self.character.set_position(self.character_position)

            # Update camera position
            camera_position = [
                self.character_position[0] + self.camera_offset[0],
                self.character_position[1] + self.camera_offset[1],
                self.character_position[2] + self.camera_offset[2]
            ]
            self.rig.set_position(camera_position)

            # Update planets
            for i, planet in enumerate(self.planets):
                angle = self.planet_orbits[i] * self.delta_time
                new_x = self.planet_distances[i] 
                new_z = self.planet_distances[i]
                planet.set_position([new_x, 0, new_z])
                planet.rotate_y(self.planet_orbits[i] * 100 * self.delta_time)

            # Update rig and render
            self.rig.update(self.input, self.delta_time)
            self.renderer.render(self.scene, self.camera)


def display_start_screen():
    pygame.init()
    screen = pygame.display.set_mode([1100, 700])
    pygame.display.set_caption("Space Scene")
    
    try:
        # Load and scale the start image
        start_image = pygame.image.load('skky.png')
        start_image = pygame.transform.scale(start_image, (1100, 700))
        
        # Display the image
        screen.blit(start_image, (0, 0))

        # --- Add welcome text ---
        welcome_font = pygame.font.Font(None, 60)  # Larger font for welcome text
        welcome_text = welcome_font.render("Welcome to the space ship game", True, (255, 255, 255))
        welcome_text_rect = welcome_text.get_rect(center=(1100//2, 700//2 - 100)) # Position above "Click to start"
        screen.blit(welcome_text, welcome_text_rect)
        # --- End welcome text ---
        
        # --- Add click to start text ---
        start_font = pygame.font.Font(None, 36)
        start_text = start_font.render("Click to start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(1100//2, 700//2 + 200)) # Position below welcome text
        screen.blit(start_text, start_text_rect)
        # --- End click to start text ---
        
        # Update the display
        pygame.display.flip()
        
        # Wait for mouse click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
        
        return True
    
    except pygame.error as e:
        print(f"Could not load start image: {e}")
        return True  # Still allow the game to run


# Run the program
if display_start_screen():
    Example(screen_size=[1100, 700]).run()