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
keys = {
    pygame.K_z: 36, pygame.K_x: 38, pygame.K_c: 40, pygame.K_v: 41, pygame.K_b: 43, pygame.K_n: 45, pygame.K_m: 47,
    pygame.K_a: 48, pygame.K_s: 50, pygame.K_d: 52, pygame.K_f: 53, pygame.K_g: 55, pygame.K_h: 57, pygame.K_j: 59,
    pygame.K_k: 60, pygame.K_l: 62, pygame.K_SEMICOLON: 64, pygame.K_QUOTE: 66,
    pygame.K_q: 24, pygame.K_w: 26, pygame.K_e: 28, pygame.K_r: 29, pygame.K_t: 31, pygame.K_y: 33, pygame.K_u: 35,
    pygame.K_i: 36, pygame.K_o: 38, pygame.K_p: 40, pygame.K_LEFTBRACKET: 42, pygame.K_RIGHTBRACKET: 44,
    pygame.K_1: 12, pygame.K_2: 14, pygame.K_3: 16, pygame.K_4: 17, pygame.K_5: 19, pygame.K_6: 21, pygame.K_7: 23,
    pygame.K_8: 24, pygame.K_9: 26, pygame.K_0: 28, pygame.K_MINUS: 30, pygame.K_EQUALS: 32
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

# Get the list of available MIDI output devices
midi_output_count = pygame.midi.get_count()
available_output_names = [
    pygame.midi.get_device_info(i)[1].decode("utf-8")
    for i in range(midi_output_count)
]

# Select the default MIDI output device
output_device_id = 0
selected_instrument = 0

# Define the slider menu variables
slider_rect = pygame.Rect(10, 40, 200, 30)
slider_min_value = 0
slider_max_value = 127
slider_value = selected_instrument
slider_dragging = False
font = pygame.font.Font(None, 24)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in keys:
                note = keys[event.key]
                output.note_on(note, velocity=127)
                key_states[event.key] = True
            elif event.key == pygame.K_LEFT:
                slider_value = max(slider_value - 1, slider_min_value)
                selected_instrument = slider_value
                output.set_instrument(selected_instrument)
            elif event.key == pygame.K_RIGHT:
                slider_value = min(slider_value + 1, slider_max_value)
                selected_instrument = slider_value
                output.set_instrument(selected_instrument)
        elif event.type == pygame.KEYUP:
            if event.key in keys:
                note = keys[event.key]
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
    for i, (key, note) in enumerate(keys.items()):
        key_rect = pygame.Rect(i * key_width, 0, key_width, window_height)
        key_color = RED if key_states[key] else WHITE
        pygame.draw.rect(window, key_color, key_rect)
        pygame.draw.rect(window, BLACK, key_rect, 1)

    # Draw the slider menu
    pygame.draw.rect(window, GRAY, slider_rect)
    pygame.draw.rect(window, BLACK, slider_rect, 1)
    slider_handle_x = int((slider_value / (slider_max_value - slider_min_value)) * slider_rect.width)
    slider_handle_rect = pygame.Rect(
        slider_rect.x + slider_handle_x - 5, slider_rect.y, 10, slider_rect.height
    )
    pygame.draw.rect(window, BLACK, slider_handle_rect)
    value_text = font.render(str(selected_instrument), True, BLACK)
    value_text_rect = value_text.get_rect(center=slider_rect.center)
    window.blit(value_text, value_text_rect)

    # Update the display
    pygame.display.flip()

# Clean up
output.close()
pygame.midi.quit()
pygame.quit()
