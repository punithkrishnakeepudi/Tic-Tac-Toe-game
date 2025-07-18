# 🧠 Tic-Tac-Toe AI — Pygame Edition

A fun and challenging **Tic-Tac-Toe game** built with **Python and Pygame**, featuring a **smart AI opponent** with three difficulty levels:

- 🟢 **Easy**: Random moves for a relaxed game
- 🟡 **Medium**: Blocks player wins + random moves
- 🔴 **Hard**: Minimax algorithm for unbeatable play 💡

---

## 🎮 Features

- 🧠 **Smart AI**: Depth-aware minimax algorithm in Hard mode
- 🤖 **Single-player** mode vs AI or 👥 **Two-player** mode
- 🎨 **Pygame UI**: Smooth hover effects, winning line animations, and clean interface
- 📝 **Player Names & Scores**: Input names and track scores across rounds
- 🔊 **Sound Support**: Placeholders for move, win, and click sounds (add `.wav` files to enable)

---

## 📦 Requirements

- Python 3.6+
- Pygame

Install dependencies:
```bash
pip install pygame
```

---

## 🚀 How to Run

1. Clone or download this repository.
2. Navigate to the project directory containing `v2.py`.
3. Run the game:
   ```bash
   python v2.py
   ```

---

## 🎲 How to Play

1. **Main Menu**: Click "Start Game" to begin or "Exit" to quit.
2. **Choose Mode**: Select 🕹️ Single-player (vs AI) or 👥 Two-player.
3. **Set Difficulty** (Single-player): Pick 🟢 Easy, 🟡 Medium, or 🔴 Hard.
4. **Enter Names**: Type player name(s) and press Enter to start.
5. **Gameplay**: Click on the 3x3 grid to place X or O. AI moves automatically in Single-player.
6. **Game Over**: See the winner or draw, then choose "Play Again" or "Main Menu."

---

## 🔧 Notes

- Add `.wav` files (e.g., `move.wav`, `win.wav`, `click.wav`) to the project directory to enable sound effects.
- Game runs in an 800x600 window.
- Hard mode AI may have a slight delay due to minimax calculations.

---

## 🌟 Future Enhancements

- 🔊 Add sound effects for moves and wins
- 🎨 Customizable themes or board sizes
- 📊 Save game statistics

---

## 📜 License

MIT License
