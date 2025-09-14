import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spin the Wheel Game")

# Colors
BACKGROUND = (25, 25, 40)
WHEEL_COLORS = [
    (255, 100, 100),  # Red
    (100, 255, 100),  # Green
    (100, 100, 255),  # Blue
    (255, 255, 100),  # Yellow
    (255, 100, 255),  # Magenta
    (100, 255, 255),  # Cyan
    (255, 165, 0),    # Orange
    (128, 0, 128),    # Purple
    (0, 128, 128),    # Teal
    (255, 192, 203)   # Pink
]
TEXT_COLOR = (255, 255, 255)
WHEEL_BORDER = (50, 50, 70)
POINTER_COLOR = (255, 50, 50)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Wheel properties
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
WHEEL_RADIUS = 200
NUM_SECTIONS = 10
PRIZES = ["$100", "$200", "$500", "$1000", "Car", "Trip", "TV", "Phone", "Watch", "Nothing"]
SECTION_ANGLE = 2 * math.pi / NUM_SECTIONS

# Game variables
spinning = False
angle = 0
spin_speed = 0
result = None
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

# Button
button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 50)

def draw_wheel():
    # Draw wheel border
    pygame.draw.circle(screen, WHEEL_BORDER, WHEEL_CENTER, WHEEL_RADIUS + 10)
    
    # Draw wheel sections
    for i in range(NUM_SECTIONS):
        start_angle = angle + i * SECTION_ANGLE
        end_angle = start_angle + SECTION_ANGLE
        
        # Draw section
        points = [WHEEL_CENTER]
        for rad in [start_angle + (SECTION_ANGLE * j / 10) for j in range(11)]:
            points.append((
                WHEEL_CENTER[0] + WHEEL_RADIUS * math.cos(rad),
                WHEEL_CENTER[1] + WHEEL_RADIUS * math.sin(rad)
            ))
        
        pygame.draw.polygon(screen, WHEEL_COLORS[i], points)
        
        # Draw prize text
        text_angle = start_angle + SECTION_ANGLE / 2
        text_x = WHEEL_CENTER[0] + (WHEEL_RADIUS * 0.7) * math.cos(text_angle)
        text_y = WHEEL_CENTER[1] + (WHEEL_RADIUS * 0.7) * math.sin(text_angle)
        
        # Rotate text to align with section
        prize_text = small_font.render(PRIZES[i], True, TEXT_COLOR)
        rotated_text = pygame.transform.rotate(prize_text, 270 - math.degrees(text_angle))
        text_rect = rotated_text.get_rect(center=(text_x, text_y))
        screen.blit(rotated_text, text_rect)
    
    # Draw center circle
    pygame.draw.circle(screen, (200, 200, 200), WHEEL_CENTER, 20)
    pygame.draw.circle(screen, (100, 100, 100), WHEEL_CENTER, 15)

def draw_pointer():
    pointer_points = [
        (WHEEL_CENTER[0], WHEEL_CENTER[1] - WHEEL_RADIUS - 20),
        (WHEEL_CENTER[0] - 15, WHEEL_CENTER[1] - WHEEL_RADIUS + 10),
        (WHEEL_CENTER[0] + 15, WHEEL_CENTER[1] - WHEEL_RADIUS + 10)
    ]
    pygame.draw.polygon(screen, POINTER_COLOR, pointer_points)
    pygame.draw.polygon(screen, (200, 50, 50), pointer_points, 2)

def draw_button():
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, (50, 100, 150), button_rect, 3, border_radius=10)
    
    text = font.render("SPIN", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def get_prize():
    # Calculate which section is at the top
    normalized_angle = angle % (2 * math.pi)
    section_index = int(normalized_angle / SECTION_ANGLE)
    # Adjust for the way we draw sections (inverse order)
    return PRIZES[(NUM_SECTIONS - section_index) % NUM_SECTIONS]

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not spinning:
                spinning = True
                spin_speed = random.uniform(0.2, 0.4)
                result = None
    
    # Update wheel spin
    if spinning:
        angle += spin_speed
        spin_speed *= 0.995  # Gradually slow down
        
        if spin_speed < 0.001:
            spinning = False
            spin_speed = 0
            result = get_prize()
    
    # Draw everything
    screen.fill(BACKGROUND)
    
    # Draw decorative elements
    for i in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        pygame.draw.circle(screen, (80, 80, 100), (x, y), size)
    
    draw_wheel()
    draw_pointer()
    draw_button()
    
    # Draw result
    if result:
        result_text = font.render(f"You won: {result}!", True, (255, 255, 150))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 20))
    
    # Draw title
    title_text = font.render("SPIN THE WHEEL", True, (255, 215, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 60))
    
    pygame.display.flip()
    clock.tick(60)
