import pygame
import pygame.midi

# Initialize Pygame
pygame.init()
pygame.midi.init()

# Set up the window
window_width, window_height = 800, 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Keyboard Piano")

# Set up the piano keys
keys = [
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m,
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j,
    pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE,
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u,
    pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET,
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
    pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS
]
notes = [
    36, 38, 40, 41, 43, 45, 47,
    48, 50, 52, 53, 55, 57, 59,
    60, 62, 64, 66,
    24, 26, 28, 29, 31, 33, 35,
    36, 38, 40, 42, 44,
    12, 14, 16, 17, 19, 21, 23,
    24, 26, 28, 30, 32
]

# Initialize the MIDI output
output = pygame.midi.Output(0)
output.set_instrument(0)

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Create a dictionary to keep track of the key states
key_states = {key: False for key in keys}

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in keys:
                note = notes[keys.index(event.key)]
                output.note_on(note, velocity=127)
                key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in keys:
                note = notes[keys.index(event.key)]
                output.note_off(note)
                key_states[event.key] = False

    # Clear the window
    window.fill(WHITE)

    # Draw the piano keys
    key_width = window_width // len(keys)
    for i, key in enumerate(keys):
        key_rect = pygame.Rect(i * key_width, 0, key_width, window_height)
        key_color = RED if key_states[key] else WHITE
        pygame.draw.rect(window, key_color, key_rect)
        pygame.draw.rect(window, BLACK, key_rect, 1)

    # Update the display
    pygame.display.flip()

# Clean up
output.close()
pygame.midi.quit()
pygame.quit()
