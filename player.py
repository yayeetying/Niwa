import pygame

class Player:
    def __init__(self, x, y, sprite_path):
        # 2D Vector for position
        self.pos = pygame.Vector2(x, y)
        self.size = (100, 100)
        self.speed = 7
        self.direction = "down"
        self.moving = False
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 8  # Controls how fast animation cycles

        # Load and slice the sprite sheet
        self.frame_width = 64
        self.frame_height = 64
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()

        directions = ["down", "left", "right", "up"]
        self.frames = {d: [] for d in directions}

        for row, direction in enumerate(directions):
            for col in range(4):
                rect = pygame.Rect(col * self.frame_width, row * self.frame_height,
                                   self.frame_width, self.frame_height)
                image = self.sprite_sheet.subsurface(rect)
                self.frames[direction].append(image)

    def manual_change_pos(self, x, y):
        self.pos = pygame.Vector2(x, y)

    def handle_input(self, keys, collision_matrix, tile_size):
        self.moving = False
        proposed_pos = self.pos.copy()

        if keys[pygame.K_LEFT]:
            proposed_pos.x -= self.speed
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            proposed_pos.x += self.speed
            self.direction = "right"
            self.moving = True
        elif keys[pygame.K_UP]:
            proposed_pos.y -= self.speed
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_DOWN]:
            proposed_pos.y += self.speed
            self.direction = "down"
            self.moving = True
        
        # Move if target tile is movable to; also keep track of transitions to other maps
        tile = self.detect_collision(proposed_pos, collision_matrix, tile_size)
        if tile == '1' or tile == '9': # Move or dialogue trigger spaces
            self.pos = proposed_pos
            
        # Keeps track of which map player is on
        return tile

    def update(self, world_width, world_height):
        if self.moving:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
                self.frame_timer = 0
        else:
            self.current_frame = 0  # idle
        # Clamp player to world bounds accounting for player's frame
        self.pos.x = max(0 - self.frame_width/2, min(world_width - self.frame_width, self.pos.x))
        self.pos.y = max(0 - self.frame_height, min(world_height - self.frame_height, self.pos.y))
    
    # Detects collision with tiles
    def detect_collision(self, pos, collision_matrix, tile_size):
        row = int(pos.y // tile_size)
        col = int(pos.x // tile_size)

        if 0 <= row < len(collision_matrix) and 0 <= col < len(collision_matrix[0]):
            return collision_matrix[row][col]

    def draw(self, surface, camera_offset):
        frame = self.frames[self.direction][self.current_frame]
        frame = pygame.transform.scale(frame, self.size)
        draw_pos = (self.pos.x - camera_offset[0], self.pos.y - camera_offset[1])
        surface.blit(frame, draw_pos)
