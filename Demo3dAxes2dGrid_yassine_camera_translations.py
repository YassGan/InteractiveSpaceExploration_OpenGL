#!/usr/bin/python3
import math
import pathlib
import sys

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
from py3d.material.texture import TextureMaterial  # Import TextureMaterial
from py3d.core_ext.texture import Texture  # Import Texture for loading images

import pygame  # Import Pygame for audio


class Example(Base):
    """ Render two boxes with camera control and a sky. """
    
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
 
        # Initialize Pygame mixer
        pygame.mixer.init()
        
        # Load your audio file here
        pygame.mixer.music.load("audio.mp3")  # Make sure the path is correct
        pygame.mixer.music.play(-1)  # Play the audio indefinitely

        # Setup the movement rig for the camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 4, 15])

        # Create the first box
        width, height, depth = 1, 1, 1  # Set the dimensions of the box
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
       
        # Position for the first box
        box1_position = [0.5, 0, 0]
        geometry1 = BoxGeometry(width, height, depth)
        self.mesh1 = Mesh(geometry1, material)
        self.mesh1.set_position(box1_position)
        self.scene.add(self.mesh1)

        # Create the second box
        box2_position = [-0.5, 2, 0]  # Position for the second box
        geometry2 = BoxGeometry(width, height, depth)
        self.mesh2 = Mesh(geometry2, material)
        self.mesh2.set_position(box2_position)
        self.scene.add(self.mesh2)

        # # Skybox setup
        # sky_geometry = BoxGeometry(500, 500, 500)  # Large box for the sky
        # sky_material = TextureMaterial(texture=Texture(file_name="skky.png"))  # Load the sky texture
        # self.sky = Mesh(sky_geometry, sky_material)
        # self.sky.set_position([0, 0, 0])  # Center the sky
        # self.scene.add(self.sky)  # Add the sky mesh to the scene


        ## for a sphere container rather then a box
        from py3d.geometry.sphere import SphereGeometry  # Import SphereGeometry

        # Replace this with the correct import path for SphereGeometry in your library
        from py3d.geometry.sphere import SphereGeometry  

        # Skysphere setup
        sky_geometry = SphereGeometry(radius=850)  # Define the skysphere with a radius
        sky_material = TextureMaterial(texture=Texture(file_name="skky.png"))  # Load the sky texture
        self.sky = Mesh(sky_geometry, sky_material)
        self.sky.set_position([0, 0, 0])  # Center the skysphere
        self.scene.add(self.sky)  # Add the skysphere to the scene














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

        # Maintain the current position of the rig
        self.current_position = [0, 4, 15]

    def update(self):
        # Handle camera position changes based on keyboard input
        if self.input.is_key_pressed('up'):
            self.current_position[1] += 0.1  # Move up
        elif self.input.is_key_pressed('down'):
            self.current_position[1] -= 0.1  # Move down
        elif self.input.is_key_pressed('left'):
            self.current_position[0] -= 0.1  # Move left
        elif self.input.is_key_pressed('right'):
            self.current_position[0] += 0.1  # Move right

        # Zoom in and out with 'I' and 'O' keys
        if self.input.is_key_pressed('i'):
            self.current_position[2] -= 0.1  # Zoom in
        elif self.input.is_key_pressed('o'):
            self.current_position[2] += 0.1  # Zoom out

        # Update the rig position
        self.rig.set_position(self.current_position)

        # Update the rig and render the scene
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
