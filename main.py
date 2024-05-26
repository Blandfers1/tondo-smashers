import os
import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tondo Smashers")

# Set Framerate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
game_started = False

# Define initial y-coordinate position for fighters
initial_y_position = 400

# Define fighter variables
knight_size = 180
knight_scale = 3
knight_offset = [72, 56]
knight_data = [knight_size, knight_scale, knight_offset]
hero_size = 200
hero_scale = 4
hero_offset = [112, 80]
hero_data = [hero_size, hero_scale, hero_offset]
samurai_size = 220
samurai_scale = 3
samurai_offset = [100, 70]
samurai_data = [samurai_size, samurai_scale, samurai_offset]
king_size = 210
king_scale = 3
king_offset = [90, 70]
king_data = [king_size, king_scale, king_offset]

# Load music and sounds
current_dir = os.path.dirname(__file__)
music_file = os.path.join(current_dir, "assets/audio/music.mp3")
sword_fx_file = os.path.join(current_dir, "assets/audio/sword.wav")
samurai_fx_file = os.path.join(current_dir, "assets/audio/samurai.mp3")

pygame.mixer.music.load(music_file)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
sword_fx = pygame.mixer.Sound(sword_fx_file)
sword_fx.set_volume(0.5)
samurai_fx = pygame.mixer.Sound(samurai_fx_file)
samurai_fx.set_volume(0.75)

# Load new background image for the main menu and the game
bg_image = pygame.image.load(os.path.join(current_dir, "assets/images/background/background.jpg")).convert_alpha()
scaled_bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

# Load spritesheets
knight_sheet = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/Hero Knight/Sprites/sprite_sheet.png")).convert_alpha()
hero_sheet = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/Martial Hero/Sprites/sprite_sheet.png")).convert_alpha()
samurai_sheet = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/Samurai/Sprites/sprite_sheet.png")).convert_alpha()
king_sheet = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/King/Sprites/sprite_sheet.png")).convert_alpha()

# Load character icons
knight_icon = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/Hero Knight/Sprites/icon.png")).convert_alpha()
hero_icon = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/Martial Hero/Sprites/icon.png")).convert_alpha()
samurai_icon = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/Samurai/Sprites/icon.png")).convert_alpha()
king_icon = pygame.image.load(os.path.join(current_dir, "assets/images/sprites/King/Sprites/icon.png")).convert_alpha()

# Load main menu images
start_img = pygame.image.load(os.path.join(current_dir, "assets/icons/start.png")).convert_alpha()
option_img = pygame.image.load(os.path.join(current_dir, "assets/icons/option.png")).convert_alpha()
quit_img = pygame.image.load(os.path.join(current_dir, "assets/icons/quit.png")).convert_alpha()
title_img = pygame.image.load(os.path.join(current_dir, "assets/icons/title.png")).convert_alpha()

# Print the sprite sheet sizes for debugging
print(f"Knight sheet dimensions: {knight_sheet.get_size()}")
print(f"Hero sheet dimensions: {hero_sheet.get_size()}")
print(f"Samurai sheet dimensions: {samurai_sheet.get_size()}")
print(f"King sheet dimensions: {king_sheet.get_size()}")

# Define number of steps in each animation
knight_animation_steps = [11, 8, 3, 7, 7, 4, 11]
hero_animation_steps = [8, 8, 2, 6, 6, 4, 4, 6]
samurai_animation_steps = [4, 8, 2, 4, 4, 3, 7]
king_animation_steps = [8, 8, 2, 4, 4, 4, 4, 6]

count_font = pygame.font.Font(os.path.join(current_dir, "assets/fonts/tekken6.ttf"), 80)
score_font = pygame.font.Font(os.path.join(current_dir, "assets/fonts/tekken6.ttf"), 30)

# Load victory images
player1_wins_img = pygame.image.load(os.path.join(current_dir, "assets/icons/PLAYER-1-WINS.png")).convert_alpha()
player2_wins_img = pygame.image.load(os.path.join(current_dir, "assets/icons/PLAYER-2-WINS.png")).convert_alpha()

# Load the new "Select Your Player" image
select_player_img = pygame.image.load(os.path.join(current_dir, "assets/icons/character select.png")).convert_alpha()

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg():
    screen.blit(scaled_bg_image, (0, 0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Main menu function
def main_menu():
    draw_bg()  # Use the new background image

    # Calculate positions for the buttons
    title_x = (screen_width - title_img.get_width()) // 2
    title_y = screen_height // 8
    start_x = (screen_width - start_img.get_width()) // 2
    start_y = title_y + title_img.get_height() + 40
    option_x = (screen_width - option_img.get_width()) // 2
    option_y = start_y + start_img.get_height() + 40
    quit_x = (screen_width - quit_img.get_width()) // 2
    quit_y = option_y + option_img.get_height() + 40

    # Create rectangles for the buttons to detect collisions
    start_rect = start_img.get_rect(topleft=(start_x, start_y))
    option_rect = option_img.get_rect(topleft=(option_x, option_y))
    quit_rect = quit_img.get_rect(topleft=(quit_x, quit_y))

    menu_items = [start_rect, option_rect, quit_rect]
    current_selection = 0

    def draw_menu():
        draw_bg()
        screen.blit(title_img, (title_x, title_y))
        screen.blit(start_img, (start_x, start_y))
        screen.blit(option_img, (option_x, option_y))
        screen.blit(quit_img, (quit_x, quit_y))
        # Draw rectangle around current selection
        pygame.draw.rect(screen, YELLOW, menu_items[current_selection], 3)
        pygame.display.update()

    draw_menu()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if current_selection == 0:  # Start Game
                        waiting = False
                    elif current_selection == 1:  # Option
                        print("Option Button Clicked")
                        # Handle option button click
                    elif current_selection == 2:  # Quit
                        pygame.quit()
                        exit()
                draw_menu()

main_menu()

def character_selection():
    selected_characters = [0, 0]
    player_selected = [False, False]
    characters = ["knight", "hero", "samurai", "king"]
    character_icons = [knight_icon, hero_icon, samurai_icon, king_icon]

    # Set character icon size and positions
    char_icon_size = 128
    char_spacing_x = 150
    char_spacing_y = 200
    char_start_x = (screen_width - char_spacing_x * len(characters)) // 2
    char_start_y_p1 = screen_height // 4 + 50  # Adjusted position
    char_start_y_p2 = char_start_y_p1 + char_spacing_y

    # Scale character icons to fit the selection box
    scaled_character_icons = [pygame.transform.scale(icon, (char_icon_size, char_icon_size)) for icon in character_icons]

    # Use default Pygame font for the instructions
    instruction_font = pygame.font.SysFont(None, 40)  # None for default font, 40 is the font size

    while not (player_selected[0] and player_selected[1]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_characters[0] = (selected_characters[0] - 1) % len(characters)
                elif event.key == pygame.K_RIGHT:
                    selected_characters[0] = (selected_characters[0] + 1) % len(characters)
                elif event.key == pygame.K_a:
                    selected_characters[1] = (selected_characters[1] - 1) % len(characters)
                elif event.key == pygame.K_d:
                    selected_characters[1] = (selected_characters[1] + 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    player_selected[0] = True
                elif event.key == pygame.K_SPACE:
                    player_selected[1] = True

        draw_bg()  # Draw the background image
        screen.blit(select_player_img, ((screen_width - select_player_img.get_width()) // 2, 20))  # Adding the "Select Your Player" image

        # Position instructions at the bottom of the screen
        instructions_y_offset = screen_height - 80
        draw_text("Player 1: Use Arrow Keys, Enter to Select", instruction_font, WHITE, 20, instructions_y_offset)
        draw_text("Player 2: Use A/D Keys, Space to Select", instruction_font, WHITE, 20, instructions_y_offset + 40)

        # Draw player 1's character choices
        for i, char in enumerate(characters):
            char_x = char_start_x + i * char_spacing_x
            screen.blit(scaled_character_icons[i], (char_x, char_start_y_p1))

        # Draw player 2's character choices
        for i, char in enumerate(characters):
            char_x = char_start_x + i * char_spacing_x
            screen.blit(scaled_character_icons[i], (char_x, char_start_y_p2))

        # Highlight the selected character for player 1
        selected_char_x_p1 = char_start_x + selected_characters[0] * char_spacing_x
        pygame.draw.rect(screen, WHITE, (selected_char_x_p1, char_start_y_p1, char_icon_size, char_icon_size), 3)

        # Highlight the selected character for player 2
        selected_char_x_p2 = char_start_x + selected_characters[1] * char_spacing_x
        pygame.draw.rect(screen, WHITE, (selected_char_x_p2, char_start_y_p2, char_icon_size, char_icon_size), 3)

        pygame.display.update()

    game_started = True
    main(selected_characters)
    character_selection()




# Main function to initialize the game
def main(selected_characters):
    # Fighter instances based on selection
    if selected_characters[0] == 0:
        fighter_1 = Fighter(1, 200, initial_y_position, False, knight_data, knight_sheet, knight_animation_steps, sword_fx)
    elif selected_characters[0] == 1:
        fighter_1 = Fighter(1, 200, initial_y_position, False, hero_data, hero_sheet, hero_animation_steps, sword_fx)
    elif selected_characters[0] == 2:
        fighter_1 = Fighter(1, 200, initial_y_position, False, samurai_data, samurai_sheet, samurai_animation_steps, samurai_fx)
    elif selected_characters[0] == 3:
        fighter_1 = Fighter(1, 200, initial_y_position, False, king_data, king_sheet, king_animation_steps, sword_fx)
    
    if selected_characters[1] == 0:
        fighter_2 = Fighter(2, 800, initial_y_position, True, knight_data, knight_sheet, knight_animation_steps, sword_fx)
    elif selected_characters[1] == 1:
        fighter_2 = Fighter(2, 800, initial_y_position, True, hero_data, hero_sheet, hero_animation_steps, sword_fx)
    elif selected_characters[1] == 2:
        fighter_2 = Fighter(2, 800, initial_y_position, True, samurai_data, samurai_sheet, samurai_animation_steps, samurai_fx)
    elif selected_characters[1] == 3:
        fighter_2 = Fighter(2, 800, initial_y_position, True, king_data, king_sheet, king_animation_steps, sword_fx)
    
    run_game(fighter_1, fighter_2)

# Main game loop
def run_game(fighter_1, fighter_2):
    run = True
    while run:
        clock.tick(FPS)
        draw_bg()

        # Show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, screen_width - 420, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, screen_width - 80, 60)

        # Move fighters
        fighter_1.move(screen_width, screen_height, screen, fighter_2, round_over)
        fighter_2.move(screen_width, screen_height, screen, fighter_1, round_over)

        # Update fighters
        fighter_1.update()
        fighter_2.update()

        # Draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # Check for player defeat
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                fighter_1 = Fighter(1, 200, initial_y_position, False, knight_data, knight_sheet, knight_animation_steps, sword_fx)
                fighter_2 = Fighter(2, 800, initial_y_position, True, knight_data, knight_sheet, knight_animation_steps, sword_fx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    
    pygame.quit()

# Start the game
main_menu()
character_selection()
