import pygame
import os
import random

def play_random_music():
    pygame.init()

    music_folder = './music/lofi'
    music_files = os.listdir(music_folder)
    max_index = len(music_files)

    pygame.mixer.init()

    current_song_index = random.randint(0, max_index - 1)
    print(music_files[current_song_index])  #Get the first song
    while True:
        music_path = os.path.join(music_folder, music_files[current_song_index])
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        current_song_index = (current_song_index + 1) % max_index  # Move to the next song, looping back to the first file if necessary
        print(music_files[current_song_index])  #get the next song and the rest

play_random_music()