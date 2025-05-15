import numpy as np
import pyaudio
import pygame
import sys
import threading

# Frequency for notes
note_freq = {
    'C': 261.63,
    'C#': 277.18,
    'D': 293.66,
    'D#': 311.13,
    'E': 329.63,
    'F': 349.23,
    'F#': 369.99,
    'G': 392.00,
    'G#': 415.30,
    'A': 440.00,
    'A#': 466.16,
    'B': 493.88
}

def generate_note(freq, duration):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
    samples = (np.sin(2 * np.pi * np.arange(44100 * duration) * freq / 44100)).astype(np.float32)
    stream.write(samples)
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_melody(melody):
    for note, duration in melody:
        if note == 'rest':
            pygame.time.delay(int(duration * 1000))
        else:
            freq = note_freq[note]
            generate_note(freq, duration)

def main():
    pygame.init()

    # Game Variables
    gravity = 1
    screen_width = 800
    screen_height = 600
    fps = 60

    # Colors
    sky_blue = (135, 206, 235)
    grass_green = (0, 255, 0)

    class Yoshi(pygame.Rect):
        def __init__(self):
            super().__init__(100, 100, 30, 30)
            self.vy = 0
            self.vx = 0
            self.on_ground = False
            self.has_egg = False

        def move(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.vx = -5
            elif keys[pygame.K_RIGHT]:
                self.vx = 5
            else:
                self.vx = 0

            if keys[pygame.K_SPACE] and self.on_ground:
                self.vy = -20
                self.on_ground = False

            self.x += self.vx
            self.vy += gravity
            self.y += self.vy

            if self.bottom >= screen_height - 20:  # Ground collision
                self.bottom = screen_height - 20
                self.vy = 0
                self.on_ground = True

    class Platform(pygame.Rect):
        def __init__(self, x, y, width, height):
            super().__init__(x, y, width, height)

    class Egg(pygame.Rect):
        def __init__(self, x, y):
            super().__init__(x, y, 10, 10)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Yoshi\'s Island 1-1')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    yoshi = Yoshi()
    platforms = [Platform(0, screen_height - 20, screen_width, 20),  # Ground
                 Platform(200, 400, 200, 20),  # Simple platform
                 Platform(500, 300, 100, 20)]  # Simple platform
    enemies = [Egg(300, 350)]  # Simple enemy

    # Simplified Yoshi's Island DS-like melody
    melody = [
        ('C', 0.5),
        ('E', 0.5),
        ('G', 0.5),
        ('C', 0.5),
        ('E', 0.5),
        ('G', 0.5),
        ('C', 1),
        ('rest', 0.5),
        ('G', 0.5),
        ('F', 0.5),
        ('E', 0.5),
        ('D', 0.5),
        ('C', 1)
    ]

    # Start the melody in a separate thread
    melody_thread = threading.Thread(target=play_melody, args=(melody,))
    melody_thread.daemon = True  # So that the thread dies when main thread dies
    melody_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not yoshi.has_egg:
                    yoshi.has_egg = True
                    egg = Egg(yoshi.centerx, yoshi.centery)
                    # Simulate throwing an egg
                    print("Egg thrown!")

        yoshi.move()

        # Collision detection with platforms
        for platform in platforms:
            if yoshi.colliderect(platform):
                if yoshi.vy > 0:  # Hit from top
                    yoshi.bottom = platform.top
                    yoshi.on_ground = True
                elif yoshi.vy < 0:  # Hit from bottom
                    yoshi.top = platform.bottom
                yoshi.vy = 0

        screen.fill(sky_blue)

        # Draw ground and platforms
        for platform in platforms:
            pygame.draw.rect(screen, grass_green, platform)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), enemy)

        # Draw Yoshi
        pygame.draw.rect(screen, (0, 255, 0), yoshi)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
