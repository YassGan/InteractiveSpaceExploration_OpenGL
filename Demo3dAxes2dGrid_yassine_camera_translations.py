#!/usr/bin/python3
import math
import pathlib
import sys
import time  # Import time for oscillation

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
from py3d.material.surface import SurfaceMaterial
from py3d.extras.axes import AxesHelper
from py3d.extras.grid import GridHelper
from py3d.extras.movement_rig import MovementRig
from py3d.material.texture import TextureMaterial
from py3d.core_ext.texture import Texture
from py3d.geometry.sphere import SphereGeometry
import pygame  # Import Pygame for audio


class Example(Base):
    """ Render a box as the main character with camera follow and floating effect. """
    
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)

        # Setup the movement rig for the camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 4, 15])

        # Create the main character box
        char_geometry = BoxGeometry(1, 1, 1)  # Character dimensions
        char_material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.character = Mesh(char_geometry, char_material)
        self.character_position = [0, 0, 0]  # Start position of the character
        self.character.set_position(self.character_position)
        self.scene.add(self.character)

        # Skysphere setup
        sky_geometry = SphereGeometry(radius=850)
        sky_material = TextureMaterial(texture=Texture(file_name="skky.png"))
        self.sky = Mesh(sky_geometry, sky_material)
        self.sky.set_position([0, 0, 0])
        self.scene.add(self.sky)

        # Add axes and grid helpers
        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)
        grid = GridHelper(
            size=100,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        # Maintain initial camera offset relative to the character
        self.camera_offset = [0, 4, 15]

        # Initialize time for oscillation
        self.time_start = time.time()

    def update(self):
        # Handle main character movement input
        if self.input.is_key_pressed('up'):
            self.character_position[2] -= 0.1  # Move forward
        elif self.input.is_key_pressed('down'):
            self.character_position[2] += 0.1  # Move backward
        if self.input.is_key_pressed('left'):
            self.character_position[0] -= 0.1  # Move left
        elif self.input.is_key_pressed('right'):
            self.character_position[0] += 0.1  # Move right

        # Time-based oscillation for character's floating effect
        elapsed_time = time.time() - self.time_start
        oscillation_amplitude = 0.007
        oscillation_speed = 2.0
        floating_offset = [
            oscillation_amplitude * math.sin(oscillation_speed * elapsed_time),  # Horizontal oscillation
            oscillation_amplitude * math.sin(oscillation_speed * elapsed_time),  # Vertical oscillation
            0
        ]

        # Apply oscillation to the character's position
        self.character_position[0] += floating_offset[0]  # Apply the horizontal oscillation (X-axis)
        self.character_position[1] += floating_offset[1]  # Apply the vertical oscillation (Y-axis)

        # Update the character's position
        self.character.set_position(self.character_position)

        # Calculate the camera position to follow the character
        camera_position = [
            self.character_position[0] + self.camera_offset[0],
            self.character_position[1] + self.camera_offset[1],
            self.character_position[2] + self.camera_offset[2]
        ]

        # Update the rig to follow the character
        self.rig.set_position(camera_position)
        self.rig.look_at(self.character_position)  # Keep the camera focused on the character

        # Update the rig and render the scene
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
