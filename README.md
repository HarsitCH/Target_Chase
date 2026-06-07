#  Target Chase

A fast-paced arcade game built with Python and Pygame where players collect moving targets while avoiding increasingly dangerous enemies.

##  Overview

<img width="468" height="392" alt="image" src="https://github.com/user-attachments/assets/9dc0c60c-1174-40f9-9349-d740f36ed6de" /> 
<img width="467" height="352" alt="image" src="https://github.com/user-attachments/assets/b5e8d1d4-bf28-4bc6-bf99-7b84cc98e8a6" />
<img width="479" height="382" alt="image" src="https://github.com/user-attachments/assets/4da3030d-e8d5-4a77-89b0-cedb3451c163" />



Target Chase is a reflex-based survival game where you must:

✅ Collect green targets to earn points  
✅ Avoid red enemies that chase you  
✅ Survive with only 3 lives  
✅ Progress through multiple difficulty levels  
✅ Beat your personal high score

As your score increases, enemies become faster and more aggressive, making every point harder to earn.

---

##  Features

- Smooth player movement (WASD / Arrow Keys)
- Dynamic moving targets
- Progressive level system
- Enemy pathfinding AI
- Health system with invincibility frames
- Particle effects when collecting targets
- Sound effects
- High score saving
- Menu and Game Over screens

---

## Controls

| Key | Action |
|-------|---------|
| W / ↑ | Move Up |
| S / ↓ | Move Down |
| A / ← | Move Left |
| D / → | Move Right |
| SPACE | Start Game |
| R | Restart After Game Over |

---

## Level Progression

| Score | Level |
|---------|---------|
| 0–4 | Level 1 |
| 5–9 | Level 2 |
| 10–14 | Level 3 |
| 15–19 | Level 4 |
| 20+ | Level 5 |

Each level introduces faster and more challenging enemies.

---

##  Game Rules

- Start with **3 lives**
- Collect green targets to increase your score
- Touching an enemy causes damage
- You receive temporary invincibility after being hit
- The game ends when:
  - Your health reaches 0, or
  - The 90-second timer expires

---

##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/target-chase.git
cd target-chase
```

### 2. Install Dependencies

```bash
pip install pygame
```

### 3. Run the Game

```bash
python main.py
```

---

##  Project Structure

```text
Target-Chase/
│
├── main.py
├── highscore.txt
├── hit.wav
├── Error.wav
└── README.md
```

---

##  Assets

The game uses custom sound effects:

- `hit.wav` → Target collected
- `Error.wav` → Player takes damage

---

##  Future Improvements

- Power-ups
- More enemy types
- Boss levels
- Animated sprites
- Leaderboards
- Background music
- Pause menu

---

##  Built With

- Python
- Pygame

---

##  License

This project is open source and available under the MIT License.

---
