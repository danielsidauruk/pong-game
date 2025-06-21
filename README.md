# Pong Game 🏓

A modern and vibrant take on the classic Pong game, featuring sophisticated colors, smooth animations, intelligent AI opponent, and dynamic sound effects.

## Features ✨

### Visual Features
- **Modern Color Palette**: Contemporary colors including electric cyan, hot pink, lime green, and golden yellow
- **Dynamic Ball Colors**: Ball cycles through 10 different modern colors when hitting paddles or walls
- **Glowing Effects**: Paddles and ball have subtle glow effects for a premium look
- **Sophisticated Background**: Dark slate background with clean center line divider
- **Professional UI**: Modern styling with electric purple accents and golden highlights

### Gameplay Features
- **Player vs AI**: Challenge an intelligent AI opponent with 70% accuracy
- **Dynamic Ball Speed**: Ball speed increases progressively during rallies (capped at maximum)
- **Smooth Controls**: Responsive keyboard (W/S or arrow keys) and mouse controls
- **Real-time Scoring**: Live score display with player names and current ball speed
- **Win Condition**: First player to reach 10 points wins

### Audio Features
- **Procedural Sound Effects**: Bounce sounds generated using mathematical sine waves
- **Score Notifications**: Special audio feedback when points are scored
- **Graceful Fallback**: Game continues to work even if audio fails

### Game System
- **Name Input**: Players enter their name before starting
- **High Score System**: Persistent leaderboard tracking top 10 scores
- **Game States**: Smooth transitions between name input, gameplay, and game over screens
- **Restart Functionality**: Easy game restart without closing the application

## Controls 🎮

### Keyboard Controls
- **W** or **↑**: Move paddle up
- **S** or **↓**: Move paddle down
- **ENTER**: Confirm name input and start game
- **SPACE**: Restart game (on game over screen)
- **ESC**: Quit game (on game over screen)

### Mouse Controls
- **Left Click + Mouse Movement**: Alternative paddle control method

## Installation & Setup 🚀

### Prerequisites
- Python 3.7 or higher
- Ubuntu/Debian-based Linux system (for system package installation)

### Quick Installation

1. **Navigate to project directory**
   ```bash
   cd game-project
   ```

2. **Install system dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3-pygame python3-numpy
   ```

3. **Run the game**
   ```bash
   python3 src/main.py
   ```

### Alternative Installation (Using pip)
If you prefer using pip with a virtual environment:
```bash
# Create virtual environment
python3 -m venv game_env
source game_env/bin/activate

# Install dependencies
pip install -r src/requirements.txt

# Run game
python3 src/main.py
```

## How to Play 🎯

1. **Launch**: Run `python3 src/main.py`
2. **Enter Name**: Type your name and press ENTER
3. **Control Paddle**: Use W/S keys, arrow keys, or mouse to move your paddle
4. **Score Points**: Hit the ball past the AI's paddle
5. **Win**: First to 10 points wins the match
6. **High Scores**: Check your ranking after the game
7. **Play Again**: Press SPACE to restart or ESC to quit

## Game Mechanics 🔧

### Ball Physics
- Starts with random direction at moderate speed
- Speed increases by 0.2 units each paddle hit
- Maximum speed capped at 12 units to maintain playability
- Color cycles through 10 modern colors on each bounce

### AI Behavior
- 70% accuracy rate for balanced difficulty
- Follows ball movement with slight imperfection
- Provides challenging but beatable gameplay experience

### Scoring System
- Points awarded when ball passes opponent's paddle
- Scores persist in `high_scores.json` file
- Top 10 scores displayed on game over screen

## Technical Architecture 💻

### File Structure
```
game-project/
├── src/                 # Main application code
│   ├── main.py              # Entry point - launches the game
│   ├── game.py              # Main game controller and state management
│   ├── constants.py         # Game constants and modern color definitions
│   ├── paddle.py            # Paddle class with movement and rendering
│   ├── ball.py              # Ball physics, movement, and color cycling
│   ├── ai_player.py         # AI opponent logic and behavior
│   ├── sound_manager.py     # Audio effects generation and playback
│   ├── score_manager.py     # High score persistence and management
│   ├── input_handler.py     # Keyboard and mouse input processing
│   ├── renderer.py          # All screen rendering and drawing functions
│   ├── pong_game.py         # Additional game logic
│   └── requirements.txt     # Python dependencies (for pip installation)
├── README.md           # This documentation
├── LICENSE             # Apache License 2.0
├── .gitignore          # Git ignore rules
└── high_scores.json    # Generated automatically for score storage
```

### Core Classes
- **Game**: Main controller managing game states and coordination
- **Paddle**: Player and AI paddle objects with movement and rendering
- **Ball**: Physics simulation with color cycling and speed progression
- **AIPlayer**: Intelligent opponent with configurable difficulty
- **SoundManager**: Procedural audio generation using sine waves
- **ScoreManager**: Persistent high score storage and retrieval
- **InputHandler**: Event processing for keyboard and mouse input
- **Renderer**: All visual rendering with modern color schemes

### Dependencies
- **pygame**: Game engine, graphics, and input handling
- **numpy**: Mathematical operations for procedural sound generation
- **json**: High score data persistence
- **random**: Game randomization and AI behavior
- **math**: Physics calculations and sound wave generation

## Color Customization 🎨

The modern color palette can be customized in `src/constants.py`:

### Current Color Scheme
```python
# Player Elements
PLAYER_COLOR = ELECTRIC_CYAN     # (0, 255, 255)
AI_COLOR = HOT_PINK              # (255, 105, 180)

# Background
DARK_SLATE = (25, 25, 35)       # Sophisticated dark background

# UI Accents
GOLDEN_YELLOW = (255, 215, 0)   # Titles and highlights
ELECTRIC_PURPLE = (191, 64, 191) # Input boxes and accents
LIME_GREEN = (50, 255, 50)      # Success messages
```

### Ball Color Cycle
10 modern colors including Electric Cyan, Lime Green, Hot Pink, Sunset Orange, Electric Purple, Golden Yellow, Mint Green, Lavender, Coral Orange, and Crimson Red.

## Performance & Compatibility 🔧

### System Requirements
- **OS**: Linux (Ubuntu/Debian tested)
- **Python**: 3.7+
- **RAM**: 100MB minimum
- **Display**: Any resolution (optimized for 1000x600)

### Performance Features
- **60 FPS**: Smooth gameplay capped at 60 frames per second
- **Efficient Rendering**: Optimized drawing with minimal resource usage
- **Graceful Degradation**: Continues working even if audio fails

### Troubleshooting
- **No pygame module**: Install with `sudo apt install python3-pygame`
- **No sound**: Game continues without audio - check system audio settings
- **Slow performance**: Close other applications, update graphics drivers

## Future Enhancements 🚀

Potential additions for future versions:
- **Multiplayer Mode**: Player vs Player local gameplay
- **Difficulty Levels**: Multiple AI difficulty settings
- **Power-ups**: Special effects and gameplay modifiers
- **Particle Effects**: Enhanced visual feedback
- **Custom Themes**: Multiple color scheme options
- **Tournament Mode**: Multi-game competitions
- **Background Music**: Ambient audio tracks

## Development 🛠️

### Code Organization
- **Modular Design**: Each component in separate files for maintainability
- **Clean Architecture**: Clear separation of concerns
- **Extensible**: Easy to add new features without breaking existing code
- **Documented**: Well-commented code for easy understanding

### Contributing
Areas for contribution:
- Additional visual effects and animations
- New game modes and features
- Performance optimizations
- Cross-platform compatibility
- Enhanced AI behaviors

## License 📄

This project is open source and available under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Credits 👏

- **Built with**: Python and Pygame
- **Inspired by**: Classic Pong arcade game
- **Audio**: Procedurally generated using mathematical sine waves
- **Design**: Modern interpretation with contemporary color palette

---

**Ready to play? Run `python3 src/main.py` and enjoy the modern Pong experience! 🏓✨**
