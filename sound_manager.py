import pygame
import math

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.create_sounds()
    
    def create_sounds(self):
        """Create simple sound effects using pygame's sound generation"""
        try:
            # Create bounce sound (short beep)
            bounce_sound = pygame.sndarray.make_sound(
                self.generate_tone(440, 0.1, 44100)
            )
            self.sounds['bounce'] = bounce_sound
            
            # Create score sound (higher pitch)
            score_sound = pygame.sndarray.make_sound(
                self.generate_tone(880, 0.3, 44100)
            )
            self.sounds['score'] = score_sound
            
        except:
            # If sound generation fails, create dummy sounds
            self.sounds['bounce'] = None
            self.sounds['score'] = None
    
    def generate_tone(self, frequency, duration, sample_rate):
        """Generate a simple sine wave tone"""
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            arr[i][0] = wave
            arr[i][1] = wave
        
        return arr.astype(pygame.int16)
    
    def play(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass
