import pygame
import pygame.midi

# Initialize Pygame
pygame.init()
pygame.midi.init()

# Set up the window
window_width, window_height = 800, 200
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Keyboard Piano")

# Set up the piano keys
keys = {
    pygame.K_z: (36, 'Z'), pygame.K_x: (38, 'X'), pygame.K_c: (40, 'C'), pygame.K_v: (41, 'V'),
    pygame.K_b: (43, 'B'), pygame.K_n: (45, 'N'), pygame.K_m: (47, 'M'),
    pygame.K_a: (48, 'A'), pygame.K_s: (50, 'S'), pygame.K_d: (52, 'D'), pygame.K_f: (53, 'F'),
    pygame.K_g: (55, 'G'), pygame.K_h: (57, 'H'), pygame.K_j: (59, 'J'), pygame.K_k: (60, 'K'),
    pygame.K_l: (62, 'L'), pygame.K_SEMICOLON: (64, ';'), pygame.K_QUOTE: (66, "'"),
    pygame.K_q: (24, 'Q'), pygame.K_w: (26, 'W'), pygame.K_e: (28, 'E'), pygame.K_r: (29, 'R'),
    pygame.K_t: (31, 'T'), pygame.K_y: (33, 'Y'), pygame.K_u: (35, 'U'),
    pygame.K_i: (36, 'I'), pygame.K_o: (38, 'O'), pygame.K_p: (40, 'P'),
    pygame.K_LEFTBRACKET: (42, '['), pygame.K_RIGHTBRACKET: (44, ']'),
    pygame.K_1: (12, '1'), pygame.K_2: (14, '2'), pygame.K_3: (16, '3'),
    pygame.K_4: (17, '4'), pygame.K_5: (19, '5'), pygame.K_6: (21, '6'),
    pygame.K_7: (23, '7'), pygame.K_8: (24, '8'), pygame.K_9: (26, '9'),
    pygame.K_0: (28, '0'), pygame.K_MINUS: (30, '-'), pygame.K_EQUALS: (32, '=')
}

# Initialize the MIDI output
output = pygame.midi.Output(0)

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Create a dictionary to keep track of the key states
key_states = {key: False for key in keys}

# Define the slider menu variables
slider_rect = pygame.Rect(10, 40, 200, 30)
slider_min_value = 0
slider_max_value = 127
slider_handle_width = 20
slider_handle_color = (100, 100, 100)
slider_handle_drag_color = (150, 150, 150)
font = pygame.font.Font(None, 24)
value_text_color = (0, 0, 0)

# Main loop
running = True
slider_dragging = False
selected_instrument = 0
slider_value = selected_instrument

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in keys:
                note, key_text = keys[event.key]
                output.note_on(note, velocity=127)
                key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in keys:
                note, key_text = keys[event.key]
                output.note_off(note)
                key_states[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if slider_rect.collidepoint(event.pos):
                    slider_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if slider_dragging:
                mouse_x = event.pos[0]
                normalized_mouse_x = mouse_x - slider_rect.x
                slider_value = int(
                    (normalized_mouse_x / slider_rect.width) * (slider_max_value - slider_min_value)
                )
                slider_value = max(min(slider_value, slider_max_value), slider_min_value)
                selected_instrument = slider_value
                output.set_instrument(selected_instrument)

    # Clear the window
    window.fill(WHITE)

    # Draw the piano keys
    key_width = window_width // len(keys)
    for i, (key, (note, key_text)) in enumerate(keys.items()):
        key_rect = pygame.Rect(i * key_width, 0, key_width, window_height)
        key_color = RED if key_states[key] else WHITE
        pygame.draw.rect(window, key_color, key_rect)
        pygame.draw.rect(window, BLACK, key_rect, 1)
        text_surface = font.render(key_text, True, BLACK)
        text_rect = text_surface.get_rect(center=key_rect.center)
        window.blit(text_surface, text_rect)

    # Draw the slider menu
    pygame.draw.rect(window, GRAY, slider_rect)
    pygame.draw.rect(window, BLACK, slider_rect, 2)

    # Calculate slider handle position
    slider_handle_x = slider_rect.x + ((slider_value - slider_min_value) / (slider_max_value - slider_min_value)) * (slider_rect.width - slider_handle_width)

    # Draw slider handle
    slider_handle_rect = pygame.Rect(slider_handle_x, slider_rect.y, slider_handle_width, slider_rect.height)
    pygame.draw.rect(window, slider_handle_color if not slider_dragging else slider_handle_drag_color, slider_handle_rect)

    # Draw value text
    value_text = font.render(str(selected_instrument), True, value_text_color)
    value_text_rect = value_text.get_rect(center=(slider_handle_rect.centerx, slider_handle_rect.centery))
    window.blit(value_text, value_text_rect)

    # Update the display
    pygame.display.flip()

# Clean up
output.close()
pygame.midi.quit()
pygame.quit()
