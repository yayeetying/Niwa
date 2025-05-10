import pygame
import pandas as pd

class Map:
    def __init__(self, name, background_path, walkability_matrix, world_size, dialogue=None, action=None):
        self.name = name
        self.background_path = background_path
        self.collision_map_path = walkability_matrix
        self.world_width, self.world_height = world_size
        self.dialogue = dialogue
        self.action = action

        # For dialogue/storyline progression in a Map
        self.scene_occurred = False # Keeps track of if storyline has been shown already
        self.trigger = False # Trigger for showing storyline scene
        self.action_trigger = False # Trigger for progressing to action in storyline

        # Load and scale background
        self.background = pygame.image.load(self.background_path).convert()
        self.background = pygame.transform.scale(self.background, (self.world_width, self.world_height))

        # Load walkability matrix
        self.walkability_matrix = pd.read_csv(self.collision_map_path, header=None, dtype=str).values.flatten().tolist()

    def get_background(self):
        return self.background

    def get_walkability_matrix(self):
        return self.walkability_matrix
    
    def get_scene_occurred(self):
        return self.scene_occurred

    def get_trigger(self):
        return self.trigger
    
    def get_action_trigger(self):
        return self.action_trigger
    
    def get_dialogue(self):
        return self.dialogue
    
    def get_action(self):
        return self.action
    