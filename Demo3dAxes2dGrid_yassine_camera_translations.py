import math
import pathlib
import sys
import pygame  # Import Pygame for mouse input handling

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
from py3d.geometry.sphere import SphereGeometry  # Import SphereGeometry for planets
from py3d.material.surface import SurfaceMaterial
from py3d.material.texture import TextureMaterial  # Import TextureMaterial
from py3d.core_ext.texture import Texture  # Import Texture for loading images
from py3d.extras.axes import AxesHelper
from py3d.extras.grid import GridHelper
from py3d.extras.movement_rig import MovementRig

class Example(Base):
    """ Render a main character box with camera control, sky, and planets. """
    
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1100 / 700)
        
        # Initialize Pygame for mouse handling
        pygame.init()

        # Setup the movement rig for the camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 4, 15])

        # Create the main character box (shipping box)
        width, height, depth = 1, 1, 1  # Set the dimensions of the box
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
       
        # Position for the main character box
        self.character_position = [0, 0, 0]  # Initial position of the main character
        geometry = BoxGeometry(width, height, depth)
        self.character = Mesh(geometry, material)
        self.character.set_position(self.character_position)
        self.scene.add(self.character)

        # Skybox setup
        sky_geometry = SphereGeometry(radius=550)  # Increased radius for the skybox
        sky_material = TextureMaterial(texture=Texture(file_name="skyy2.jpg"))  # Load the sky texture
        self.sky = Mesh(sky_geometry, sky_material)
        self.sky.set_position([0, 0, 0])  # Center the skysphere
        self.scene.add(self.sky)  # Add the skysphere to the scene

        # Add axes and grid helpers
        axes = AxesHelper(axis_length=8)
        self.scene.add(axes)
        grid = GridHelper(
            size=100,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        # Planets setup (Add two larger planets)
        self.planets = []  # Store the planets for easy manipulation
        self.planet_distances = [120, 30]  # Increased distances of planets from the character (in Z-axis)
        self.planet_sizes = [5, 10]  # Increased sizes of the planets (larger than the box)
        self.planet_orbits = [0.01, 0.005]  # Orbital speed (rotation speed)
        
        # Create planets and add them to the scene
        for i in range(2):
            planet_geometry = SphereGeometry(radius=self.planet_sizes[i])
            planet_material = TextureMaterial(texture=Texture(file_name=f"planet{i+1}.jpg"))  # Use different textures
            planet = Mesh(planet_geometry, planet_material)
            planet.set_position([self.planet_distances[i], 0, 0])  # Initial position in orbit
            self.planets.append(planet)
            self.scene.add(planet)

        # Maintain the current position of the rig (camera)
        self.camera_offset = [0, 4, 15]  # Camera offset to follow the character

    def update(self):
        # Handle the movement of the character based on keyboard input
        move_speed = 0.2

        if self.input.is_key_pressed('i'):
            self.character_position[1] -= move_speed  # Move character forward (on the Z-axis)
        elif self.input.is_key_pressed('o'):
            self.character_position[1] += move_speed  # Move character backward (on the Z-axis)

        if self.input.is_key_pressed('left'):
            self.character_position[0] -= move_speed  # Move character left (on the X-axis)
        elif self.input.is_key_pressed('right'):
            self.character_position[0] += move_speed  # Move character right (on the X-axis)

        # When 'z' is pressed, increase the position along the blue axis (Z-axis)
        if self.input.is_key_pressed('down'):
            self.character_position[2] += move_speed  # Move the character up the blue axis (positive Z)

        # When 's' is pressed, decrease the position along the blue axis (Z-axis)
        elif self.input.is_key_pressed('up'):
            self.character_position[2] -= move_speed  # Move the character down the blue axis (negative Z)

        # Update the position of the main character box
        self.character.set_position(self.character_position)

        # Update the camera position to follow the character
        camera_position = [
            self.character_position[0] + self.camera_offset[0],  # Camera follows the character's X
            self.character_position[1] + self.camera_offset[1],  # Camera follows the character's Y
            self.character_position[2] + self.camera_offset[2]   # Camera follows the character's Z
        ]
        self.rig.set_position(camera_position)

        # Update planets' positions to simulate orbital motion and their rotation on their own axis
        for i, planet in enumerate(self.planets):
            # Update the orbital position
            angle = self.planet_orbits[i] * self.delta_time  # Adjust the speed with delta_time
            new_x = self.planet_distances[i] * math.cos(angle)  # Orbital motion on X-axis
            new_z = self.planet_distances[i] * math.sin(angle)  # Orbital motion on Z-axis
            planet.set_position([new_x, 0, new_z])  # Update position in orbit
            
            # Add self-rotation (planet rotating on its own axis)
            planet.rotate_y(self.planet_orbits[i] * 100 * self.delta_time)  # Rotate around Y-axis for spinning effect

        # Update the rig and render the scene
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

# Instantiate this class and run the program
Example(screen_size=[1100, 700]).run()
