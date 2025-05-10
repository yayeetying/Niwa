import pygame
import sys
import pandas as pd

from player import Player
from map import Map
from dialoguebox import DialogueBox

# Initialize pygame and audio
pygame.init()
pygame.mixer.init() 

# Clock
clock = pygame.time.Clock()

# Screen settings
WIDTH, HEIGHT = 1200, 800
CHARACTER_WIDTH, CHARACTER_HEIGHT = 90, 90
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Niwa")

# Background image/map settings
WORLD_WIDTH = 2240 # 1792 * 1.25
WORLD_HEIGHT = 1280 # 1024 * 1.25

# Player settings
player = Player(435, 600, "assets/player.png")

# Initialize DialogueBox object (can have any dialogue in it)
dialogue_box = DialogueBox(x=50, y=HEIGHT - 140, width=WIDTH - 100, height=120)
showing_dialogue = False  # Flag to know if we’re in a dialogue state
showing_action = False # False to know if we're in action state
current_line_index = 0

# Load dialogues for each scene
with open('dialogues/lake.txt', 'r', encoding='utf-8') as file:
    LAKE_DIALOGUE = file.read().splitlines()
with open('dialogues/lake.txt', 'r', encoding='utf-8') as file:
    NOH_DIALOGUE = file.read().splitlines()
with open('dialogues/monastery.txt', 'r', encoding='utf-8') as file:
    MONASTERY_DIALOGUE = file.read().splitlines()
with open('dialogues/town.txt', 'r', encoding='utf-8') as file:
    TOWN_DIALOGUE = file.read().splitlines()

# Load additional action items for each scene
with open('dialogues/lake_action.txt', 'r', encoding='utf-8') as file:
    LAKE_ACTION_DIALOGUE = file.read().splitlines()
with open('dialogues/monastery_action.txt', 'r', encoding='utf-8') as file:
    MONASTERY_ACTION_DIALOGUE = file.read().splitlines()
'''
Background Image/Tile Representations:
0 (tile): Not walkable
1 (tile): Walkable
2: nohtheatre_img
3: lake_img
4: monastary_img
5: town_img
9 (tile): Trigger space for dialogue/scene progression
8 (tile): Trigger space for activity progression
'''
# Load background maps/images
# FIX COLLISION MAPS
TOWN = Map("town", "assets/tile.png", "collisionmaps/town.csv", (WORLD_WIDTH, WORLD_HEIGHT), TOWN_DIALOGUE)
NOH = Map("noh", "assets/nohtheatre.jpeg", "collisionmaps/noh.csv", (WORLD_WIDTH, WORLD_HEIGHT), NOH_DIALOGUE)
LAKE = Map("lake", "assets/lake.jpeg", "collisionmaps/lake.csv", (WORLD_WIDTH, WORLD_HEIGHT), LAKE_DIALOGUE, LAKE_ACTION_DIALOGUE)
MONASTERY = Map("lake", "assets/monastary.png", "collisionmaps/monastery.csv", (WORLD_WIDTH, WORLD_HEIGHT), MONASTERY_DIALOGUE, MONASTERY_ACTION_DIALOGUE)

# Default background/walkability matrix is town
current_background = TOWN
tile_size = 32

# Load other characters
zeami_img = pygame.image.load("assets/zeami.png").convert_alpha()
zeami_img = pygame.transform.scale(zeami_img, (256, 256))
ama_img = pygame.image.load("assets/amadiver.png").convert_alpha()
ama_img = pygame.transform.scale(ama_img, (256, 384))
dogen_img = pygame.image.load("assets/dogen.png").convert_alpha()
dogen_img = pygame.transform.scale(dogen_img, (256, 256))
terako_img = pygame.image.load("assets/terako.png").convert_alpha()
terako_img = pygame.transform.scale(terako_img, (256, 384))
# Default other sprite (interactable character) is town's Terako
current_other_sprite = terako_img
current_other_sprite_cords = (100, 375)

# Load and play music (originally, town's music)
pygame.mixer.music.load("music/town.mp3")
pygame.mixer.music.play(-1)

# Game loop
running = True
while running:
    screen.fill((30, 30, 30))

    # Update camera position
    camera_x = max(0, min(WORLD_WIDTH - WIDTH, int(player.pos.x - WIDTH // 2)))
    camera_y = max(0, min(WORLD_HEIGHT - HEIGHT, int(player.pos.y - HEIGHT // 2)))
    camera_offset = (camera_x, camera_y)
    # Draw screen accounting for camera position
    screen.blit(current_background.get_background(), (-camera_offset[0], -camera_offset[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Specifically for Dogen's Monastery; if player presses any key other than space, restart
            if current_background == MONASTERY and showing_action and event.key != pygame.K_SPACE:
                current_line_index = 3
            if (event.key == pygame.K_SPACE and showing_dialogue) or (event.key == pygame.K_SPACE and showing_action):
                current_line_index += 1  # Go to the next line

    if not showing_dialogue and not showing_action:
        # Handle movement
        keys = pygame.key.get_pressed()
        background = player.handle_input(keys, current_background.get_walkability_matrix(), tile_size)
        # Handle background changes in conjunction with movement
        current_background.trigger = False
        current_background.action_trigger = False
        # Dialogue tile
        if background == '9': 
            current_background.trigger = True
        # Action tile
        elif background == '8':
            current_background.action_trigger = True
        elif background == '2':
            current_background = NOH
            player.manual_change_pos(1050, 1175)
            current_other_sprite = zeami_img
            current_other_sprite_cords = (100, 450)
            pygame.mixer.music.fadeout(200)
            pygame.mixer.music.load("music/ecruteak.mp3")
            pygame.mixer.music.play(-1)
        elif background == '3':
            current_background = LAKE
            player.manual_change_pos(1080, 1100)
            current_other_sprite = ama_img
            current_other_sprite_cords = (100, 375)
            pygame.mixer.music.fadeout(200)
            pygame.mixer.music.load("music/lake.mp3")
            pygame.mixer.music.play(-1)
        elif background == '4':
            current_background = MONASTERY
            current_other_sprite = dogen_img
            current_other_sprite_cords = (100, 450)
            player.manual_change_pos(1150, 1140)
            # Change music
            pygame.mixer.music.fadeout(200)
            pygame.mixer.music.load("music/burnedtower.mp3")
            pygame.mixer.music.play(-1)
        # Coming back to TOWN
        elif background == '5':
            if current_background == LAKE:
                # Coming back from Lake
                player.manual_change_pos(1100, 180)
            elif current_background == MONASTERY:
                player.manual_change_pos(1925, 550)
            current_background = TOWN
            current_other_sprite = terako_img
            current_other_sprite_cords = (100, 375)
            # Change music
            pygame.mixer.music.fadeout(200)
            pygame.mixer.music.load("music/town.mp3")
            pygame.mixer.music.play(-1)
        player.update(WORLD_WIDTH, WORLD_HEIGHT)

    # Draw player
    player.draw(screen, camera_offset)

    # Draw scene progression/dialogue in a map (if triggered)
    if current_background.get_trigger() and not current_background.get_scene_occurred():
        showing_dialogue = True

    # If dialogue is being shown
    if showing_dialogue:
        screen.blit(current_other_sprite, current_other_sprite_cords)
        dialogue = current_background.get_dialogue()
        if dialogue != None and current_line_index < len(dialogue):
            if dialogue[current_line_index][:2] == "!0": # Cue to change music in lake
                pygame.mixer.music.fadeout(200)
                pygame.mixer.music.load("music/omoikaze.mp3")
                pygame.mixer.music.play(-1)
                current_line_index += 1
            elif dialogue[current_line_index][:2] == "!1": # Cue to change music in town
                pygame.mixer.music.fadeout(200)
                pygame.mixer.music.load("music/ramwire.mp3")
                pygame.mixer.music.play(-1)
                current_line_index += 1
            elif dialogue[current_line_index][:2] == "!2": # Cue to change music in Noh theatre
                pygame.mixer.music.fadeout(200)
                pygame.mixer.music.load("music/emotion.mp3")
                pygame.mixer.music.play(-1)
                current_line_index += 1
            else:
                dialogue_box.show(dialogue[current_line_index])
                dialogue_box.draw(screen) # Player presses space bar --> next line is shown
        else:
            showing_dialogue = False  # End of dialogue
            current_background.scene_occurred = True
            current_line_index = 0

    # Draw action progression in a map (if triggered)
    if current_background.get_action_trigger():
        showing_action = True

    if showing_action:
        dialogue = current_background.get_action()
        if dialogue != None and current_line_index < len(dialogue):
            dialogue_box.show(dialogue[current_line_index])
            dialogue_box.draw(screen) # Player presses space bar --> next line is shown
        else:
            showing_action = False  # End of dialogue
            current_line_index = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
