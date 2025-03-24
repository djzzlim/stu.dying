import pygame
from moviepy import VideoFileClip
import os
import shutil  # For removing a directory
import datetime
import random
import subprocess
import sys

# Function to convert a GIF to individual frames
def convert_gif_to_frames(gif_path, frames_directory, screen_size):
    for filename in os.listdir(frames_directory):
        file_path = os.path.join(frames_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    clip = VideoFileClip(gif_path)
    clip_resized = clip.resized(height=screen_size[1], width=screen_size[0])
    # Use %04d to represent a four-digit integer with leading zeros
    clip_resized.write_images_sequence(
        frames_directory + '/frame%04d.png', fps=clip.fps)

# Initialize Pygame
pygame.init()

# Get screen size and create a resizable Pygame window
screen_info = pygame.display.Info()
pygame_icon = pygame.image.load('./media/logo/fishfish.png')
pygame.display.set_icon(pygame_icon)
screen_size = (screen_info.current_w, screen_info.current_h - 50)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption('Stu.dying')  # Set the window caption
clock = pygame.time.Clock()

gif_path = './media/background/1.gif'  # Update with the actual path to your animated GIF

# Check if the frame folder exists, if not create it
if not os.path.exists("frame_folder"):
    os.mkdir("frame_folder")

frames_directory = './frame_folder'  # Update with the directory where frames will be saved

# Convert the GIF to frames
convert_gif_to_frames(gif_path, frames_directory, screen_size)

frame_index = 0
frame_files = sorted(os.listdir(frames_directory))
max_frame_index = len(frame_files)
button_pressed = 0
spacebar = False
leftkey = False
rightkey = False
running = True
subprocess_running = False
pomodoro_button_clicked = False
# Function to display the current time on the screen
themes = ['white', 'black', 'monowhite', 'monoblack']
theme_index = 0
def display_time(screen, theme_index, mouse_pos=None):
    current_time = datetime.datetime.now().strftime("%#I:%M %p")
    font = pygame.font.SysFont("SF Pro Display", 82, bold=True)
    
    theme = themes[theme_index]

    text_rect = None  # Initialize the text_rect variable

    if theme == 'white':
        text = font.render(current_time, True, 'white')
        text_rect = text.get_rect(topright=(screen.get_width() - 10, 15))
        pygame.draw.rect(screen, '#191919', text_rect, border_radius=8)
    elif theme == 'black':
        text = font.render(current_time, True, 'black')
        text_rect = text.get_rect(topright=(screen.get_width() - 10, 15))
        pygame.draw.rect(screen, 'white', text_rect, border_radius=8)
    elif theme == 'monowhite':
        text = font.render(current_time, True, 'white')
        text_rect = text.get_rect(topright=(screen.get_width() - 10, 15))
    elif theme == 'monoblack':
        text = font.render(current_time, True, 'black')
        text_rect = text.get_rect(topright=(screen.get_width() - 10, 15))

    if mouse_pos is not None and text_rect is not None:
        if text_rect.collidepoint(mouse_pos) and button_pressed:
            theme_index = (theme_index + 1) % len(themes)
            pygame.time.wait(150)
    
    if text_rect is not None:
        screen.blit(text, text_rect)

    return theme_index



is_fullscreen = False

# Function to handle the exit button
def exit():
    global running
    exit_surf = pygame.image.load('./media/exit.png')
    exit_surf = pygame.transform.scale(exit_surf, (50, 50))
    if is_fullscreen == False:
        exit_rect = exit_surf.get_rect(topright=(screen_info.current_w - 20, screen_info.current_h - 150), width=60, height=60)
    else:
        exit_rect = exit_surf.get_rect(topright=(screen_info.current_w - 20, screen_info.current_h - 100), width=60, height=60)

    try:
        pygame.draw.rect(screen, 'white', exit_rect, border_radius=8)
        # Check if exit button is clicked
        if exit_rect.collidepoint(mouse_pos) and button_pressed:
            # Remove the frame folder and exit the program
            shutil.rmtree("frame_folder")
            pygame.mixer.music.stop()
            pygame.quit()
            running = False
            if subprocess_running:
                process.terminate()
            raise SystemExit
        # Calculate the coordinates to center the icon within the rectangle
        icon_x = exit_rect.centerx - exit_surf.get_width() // 2
        icon_y = exit_rect.centery - exit_surf.get_height() // 2


        screen.blit(exit_surf, (icon_x, icon_y))
        
    except pygame.error:
        # Handle pygame.error if drawing operations are performed after pygame.quit()
        pass



# Function to handle the maximize/minimize button
def maximize_minimize():
    global is_fullscreen, screen, screen_size

    if is_fullscreen == False:
        # Load and scale the maximize button image
        minmax_surf = pygame.image.load('./media/maximize.png')
        minmax_surf = pygame.transform.scale(minmax_surf, (50, 50))
        # Create a rectangle for the button with specified dimensions and position
        minmax_rect = minmax_surf.get_rect(topright=(screen_info.current_w - 100, screen_info.current_h - 150), width=60, height=60)
        # Draw a white rectangle as the background for the button
        pygame.draw.rect(screen, 'white', minmax_rect, border_radius=8)
        # Calculate the coordinates to center the icon within the rectangle
        icon_x = minmax_rect.centerx - minmax_surf.get_width() // 2
        icon_y = minmax_rect.centery - minmax_surf.get_height() // 2

    else:
        # Load and scale the minimize button image
        minmax_surf = pygame.image.load('./media/minimize.png')
        minmax_surf = pygame.transform.scale(minmax_surf, (50, 50))
        # Create a rectangle for the button with specified dimensions and position
        minmax_rect = minmax_surf.get_rect(topright=(screen_info.current_w - 100, screen_info.current_h - 100), width=60, height=60)
        # Draw a white rectangle as the background for the button
        pygame.draw.rect(screen, 'white', minmax_rect, border_radius=8)
        # Calculate the coordinates to center the icon within the rectangle
        icon_x = minmax_rect.centerx - minmax_surf.get_width() // 2
        icon_y = minmax_rect.centery - minmax_surf.get_height() // 2

    # Toggle fullscreen mode when the button is clicked
    if minmax_rect.collidepoint(mouse_pos) and button_pressed:
        if is_fullscreen == False:
            is_fullscreen = True
            screen_size = (screen_info.current_w, screen_info.current_h)
            screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            is_fullscreen = False
            screen_size = (screen_info.current_w, screen_info.current_h - 50)
            screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    screen.blit(minmax_surf, (icon_x, icon_y))


#to do list
all_task = sys.argv[1:]
todo_pos = (100,70)
checkbox_radius = 10
checkbox_posx = 30
checkbox_posy = 38
spacing = 40
checkboxes = []
checkbox_checked = False
checked = []
task = all_task.copy()
task_completed = []

for i in range(len(all_task)):
    checkbox_rect = pygame.Rect(todo_pos[0] + checkbox_posx - checkbox_radius, todo_pos[1] + checkbox_posy + (40*i) - checkbox_radius, checkbox_radius * 2, checkbox_radius * 2)
    checkboxes.append(checkbox_rect)


pause_current = True
is_running = False
current_song = 0
paused_position = 0
music_folder = './music/lofi'
music_files = os.listdir(music_folder)
max_index = len(music_files)
music_name = ''

def load_song(index):
    # Load and play the song at the specified index
    global music_name
    music_path = os.path.join(music_folder, music_files[index])
    pygame.mixer.music.load(music_path)
    print("Now playing:", music_files[index][:-4])
    music_name = music_files[index][:-4]
    pygame.mixer.music.play()

def music():
    global current_song, pause_current, is_running, paused_position

    if not is_running:
        # Initialize the mixer if it's not already running
        pygame.mixer.init()

        if pygame.mixer.music.get_busy():
            # If music is already playing, wait for it to finish
            pygame.time.Clock().tick(10)
        else:
            # Start playing a random song
            current_song = random.randint(0, max_index - 1)
            is_running = True

    if pause_current:
        if pygame.mixer.music.get_busy() and paused_position is None:
            # Pause the current song if it's playing
            pygame.mixer.music.pause()
            paused_position = pygame.mixer.music.get_pos()
    else:
        if paused_position is not None:
            # Unpause the current song if it's paused
            pygame.mixer.music.unpause()
            paused_position = None
        elif not pygame.mixer.music.get_busy() and previous_button == False and skip_button == False:
            # If no button is pressed and the current song is not playing, skip to the next song
            current_song = (current_song + 1) % max_index
            load_song(current_song)

previous_button = False
def previous_song():
    global current_song, previous_button
    # Play the previous song
    current_song = (current_song - 1) % max_index
    previous_button = True
    load_song(current_song)
    if pause_current == True:
        pygame.mixer.music.pause()
    previous_button = False

skip_button = False
def skip():
    global current_song, skip_button
    # Skip to the next song
    current_song = (current_song + 1) % max_index
    skip_button = True
    load_song(current_song)
    if pause_current == True:
        pygame.mixer.music.pause()
    skip_button = False

random_index = 0
def background_change():
    global gif_path, frame_files, frame_index, frame_path, random_index
    
    background_files = os.listdir('./media/background')
    max_index = len(background_files) - 1
    
    random_index = (random_index + 1) % (max_index + 1)
    gif_path = './media/background/' + background_files[random_index]
    
    # Convert the new GIF to frames
    convert_gif_to_frames(gif_path, frames_directory, screen_size)
    frame_files = sorted(os.listdir(frames_directory))
    
    # Reset the frame index to start from the beginning
    frame_index = 0

font = pygame.font.SysFont(None, 20)
# Main game loop
while True:
    for event in pygame.event.get():
        button_pressed = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_pressed = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spacebar = True
            if event.key == pygame.K_LEFT:
                leftkey = True
            if event.key == pygame.K_RIGHT:
                rightkey = True
            
        
        try:
            if event.type == pygame.QUIT:
                # Remove the frame folder and exit the program
                shutil.rmtree("frame_folder")
                pygame.mixer.music.stop()
                pygame.quit()
                running = False
                if subprocess_running:
                    process.terminate()
                raise SystemExit
        except pygame.error:
            # Handle pygame.error if drawing operations are performed after pygame.quit()
            pass

    mouse_pos = pygame.mouse.get_pos()
    frame_index %= len(frame_files)
    frame_path = os.path.join(frames_directory, frame_files[frame_index])
    frame = pygame.image.load(frame_path)
    frame_resized = pygame.transform.scale(frame, screen_size)

    screen.blit(frame_resized, (0, 0))
    theme_index = display_time(screen, theme_index, mouse_pos)
    maximize_minimize()
    exit()

    #music
    song_font = pygame.font.SysFont("SF Pro Display", 20, bold=True)
    song_text = song_font.render(music_name, True, 'white')
    song_text_rect = song_text.get_rect(topleft=(3, 5))
    screen.blit(song_text, song_text_rect)
    music()


    #to do list
    for i, checkbox in enumerate(checkboxes): 
        if checkbox.collidepoint(mouse_pos) and button_pressed:
            button_pressed = False
            selected_task = all_task[i]
            if selected_task in task_completed:
                task_completed.remove(selected_task)
                task.append(selected_task)
            else: 
                task_completed.append(selected_task)
                task.remove(selected_task)
    todo_frame = pygame.Surface((550,550), pygame.SRCALPHA)
    pygame.draw.rect(todo_frame, (255, 255, 255, 60), (0, 0, 550, 550), border_radius=15)
    todo_font = pygame.font.SysFont("SF Pro Display", 18, bold=True)
    all_task = task + task_completed
    for i, text in enumerate(all_task):
        pygame.draw.circle(todo_frame, "white", (checkbox_posx, checkbox_posy + (spacing*i)), checkbox_radius, 2)
        text_surface = todo_font.render(text, True, "white")
        text_rect = text_surface.get_rect(topleft=(50, 23 + (spacing*i)))
        if text in task_completed: 
            pygame.draw.circle(todo_frame, "white", (checkbox_posx, checkbox_posy + (spacing*i)), checkbox_radius - 4)
            line_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            pygame.draw.rect(line_surface, (255, 255, 255, 200), pygame.Rect(0, (text_surface.get_height()//2), text_surface.get_width(), 2))
            text_surface.blit(line_surface, (0, 0))
        todo_frame.blit(text_surface, text_rect)
    screen.blit(todo_frame, todo_pos)


    #pomodoro
    pomodoro_surf = pygame.image.load("./media/timer.png")
    if is_fullscreen == False:
        pomodoro_rect = pomodoro_surf.get_rect(topright=(screen_info.current_w - 20, screen_info.current_h - 222), width=60, height=60)
    else:
        pomodoro_rect = pomodoro_surf.get_rect(topright=(screen_info.current_w - 20, screen_info.current_h - 172), width=60, height=60)
    pygame.draw.rect(screen, 'white', pomodoro_rect, border_radius=8)
    pomodoro_x = pomodoro_rect.centerx - pomodoro_surf.get_width() // 2
    pomodoro_y = pomodoro_rect.centery - pomodoro_surf.get_height() // 2
    screen.blit(pomodoro_surf,(pomodoro_x, pomodoro_y))

    # Check if the timer button is clicked and the subprocess is not already running
    if pomodoro_rect.collidepoint(mouse_pos) and button_pressed and not pomodoro_button_clicked and not subprocess_running:
        pomodoro_button_clicked = True
        button_pressed = False
        process = subprocess.Popen(['python', './pomodoro.py'])
        subprocess_running = True

    # Check if the subprocess has finished running
    if subprocess_running:
        return_code = process.poll()
        if return_code is not None:
            # Subprocess has finished running
            subprocess_running = False
            pomodoro_button_clicked = False
        
    
    # Check if current music is paused
    if pause_current == True:
        play_surf = pygame.image.load("./media/light_play.png")
        play_rect = play_surf.get_rect(midtop=(screen_info.current_w // 2, 5), width=55, height=55)
        pygame.draw.rect(screen, 'white', play_rect, border_radius=8)
        playicon_x = play_rect.centerx - play_surf.get_width() // 2
        playicon_y = play_rect.centery - play_surf.get_height() // 2
        screen.blit(play_surf,(playicon_x, playicon_y))
        
        # If the play button is clicked, resume playing
        if play_rect.collidepoint(mouse_pos) and button_pressed or spacebar:
            pause_current = False
            button_pressed = False
            spacebar = False
            pygame.time.wait(100)
    else:
        play_surf = pygame.image.load("./media/light_pause.png")
        play_rect = play_surf.get_rect(midtop=(screen_info.current_w // 2, 5), width=55, height=55)
        pygame.draw.rect(screen, 'white', play_rect, border_radius=8)
        playicon_x = play_rect.centerx - play_surf.get_width() // 2
        playicon_y = play_rect.centery - play_surf.get_height() // 2
        screen.blit(play_surf,(playicon_x, playicon_y))
        
        # If the pause button is clicked, pause the current music
        if play_rect.collidepoint(mouse_pos) and button_pressed or spacebar:
            pause_current = True
            button_pressed = False
            spacebar = False
            pygame.time.wait(100)
    
    # Previous track and skip track buttons
    previous_surf = pygame.image.load("./media/light_previous.png")
    previous_rect = previous_surf.get_rect(midtop=(screen_info.current_w // 2 - 58, 5), width=55, height=55)
    pygame.draw.rect(screen, 'white', previous_rect, border_radius=8)
    previous_x = previous_rect.centerx - previous_surf.get_width() // 2
    previous_y = previous_rect.centery - previous_surf.get_height() // 2
    screen.blit(previous_surf,(previous_x, previous_y))
    
    # If the previous track button is clicked, go to the previous song
    if previous_rect.collidepoint(mouse_pos) and button_pressed or leftkey:
        previous_song()
        leftkey = False
        pygame.time.wait(100)

    skip_surf = pygame.image.load("./media/light_skip.png")
    skip_rect = skip_surf.get_rect(midtop=(screen_info.current_w // 2 + 58, 5), width=55, height=55)
    pygame.draw.rect(screen, 'white', skip_rect, border_radius=8)
    skip_x = skip_rect.centerx - skip_surf.get_width() // 2
    skip_y = skip_rect.centery - skip_surf.get_height() // 2
    screen.blit(skip_surf,(skip_x, skip_y))
    
    # If the skip track button is clicked, skip to the next song
    if skip_rect.collidepoint(mouse_pos) and button_pressed or rightkey:
        skip()
        rightkey = False
        pygame.time.wait(100)

    bg_surf = pygame.image.load("./media/bg_change.png")
    if is_fullscreen == False:
        bg_rect = skip_surf.get_rect(topleft=(20, screen_info.current_h - 150), width=60, height=60)
    else:
        bg_rect = skip_surf.get_rect(topleft=(20, screen_info.current_h - 100), width=60, height=60)
    pygame.draw.rect(screen, 'white', bg_rect, border_radius=8)
    bg_x = bg_rect.centerx - bg_surf.get_width() // 2
    bg_y = bg_rect.centery - bg_surf.get_height() // 2
    screen.blit(bg_surf,(bg_x, bg_y))
    
    # If the skip track button is clicked, skip to the next song
    if bg_rect.collidepoint(mouse_pos) and button_pressed:
        background_change()
        button_pressed = False


    # Update frame
    frame_index += 1
    if frame_index > max_frame_index:
        frame_index = 0
    
    pygame.display.flip()
    clock.tick(12)
