import pygame

class DialogueBox:
    def __init__(self, x, y, width, height, font_size=32, 
                 bg_color=(0, 0, 0), text_color=(255, 255, 255), border_color=(255, 255, 255), border_width=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.text = ""
        self.visible = False

    def show(self, text):
        self.text = text
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, surface):
        if self.visible:
            # Draw box
            pygame.draw.rect(surface, self.bg_color, self.rect)
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

            # Word wrapping logic
            words = self.text.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] < self.rect.width - 20:  # Leave some padding
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)  # Add the last line

            # Render each line
            y_offset = 10
            for line in lines:
                rendered_line = self.font.render(line.strip(), True, self.text_color)
                surface.blit(rendered_line, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += self.font.get_height() + 4
