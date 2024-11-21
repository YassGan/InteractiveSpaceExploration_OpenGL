import math
import pathlib
import sys
import pygame
import random

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

class Example(Base):
    """ Render a main character box with camera control, sky, planets, and random moving boxes. """
    
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1100 / 700)
        
        pygame.init()

        # Setup the movement rig for the camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 4, 15])

        # Create the main character box (shipping box)
        width, height, depth = 0.05, 0.05, 0.05
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
       
        self.character_position = [29.0, -60, 157.0]
        geometry = BoxGeometry(width, height, depth)
        self.character = Mesh(geometry, material)
        self.character.set_position(self.character_position)
        self.scene.add(self.character)

        # Add random moving boxes
        self.moving_boxes = []
        self.box_positions = []
        self.box_velocities = []
        self.box_rotations = []
        
        # Create 20 random moving boxes
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
        sky_material = TextureMaterial(texture=Texture(file_name="skky.png"))
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
        self.camera_offset = [0, 0.1, 0.5]
        self.accelerate = 0.9
        self.move_speed = 0.50

    def update(self):
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
            
            # Random velocity changes
            if random.random() < 0.01:  # 1% chance each frame
                for j in range(3):
                    self.box_velocities[i][j] += random.uniform(-0.1, 0.1)
                    self.box_velocities[i][j] = max(min(self.box_velocities[i][j], 1.0), -1.0)

        # Handle speed boost
        if self.input.is_key_pressed('r'):
            self.accelerate = 2
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
            new_x = self.planet_distances[i] * math.cos(angle)
            new_z = self.planet_distances[i] * math.sin(angle)
            planet.set_position([new_x, 0, new_z])
            planet.rotate_y(self.planet_orbits[i] * 100 * self.delta_time)

        # Update rig and render
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

# Run the program
Example(screen_size=[1100, 700]).run()