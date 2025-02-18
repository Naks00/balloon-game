# Hot air ballon game  
VERN' University  
Internet of Things Department, Code Ogranization class  
Professor: Mislav Đomlija, univ. bacc. ing. comp.  
Students: Ante Nakić, Antonio Šimunčić  
Zagreb, Croatia  
February, 2025  

---  

# 🎈 Hot Air Balloon Game 

A 2D Pygame-based survival game where you control a hot air balloon, avoid obstacles, collect power-ups, and climb as high as possible!    
The game was created for a university project with OOP and SOLID principles in mind, the task at hand: [task.md](https://github.com/antoniosimuncic/balloon-game/blob/main/documentation/task.md)  

<img src="https://github.com/antoniosimuncic/balloon-game/blob/main/documentation/screenshot.png">  

---

## 🚀 Features  
- **Fuel Management**: Keep your balloon airborne by managing depleting fuel.  
- **Power-Ups**:  
  - ⛽ **Fuel Canisters**: Refill your fuel tank.  
  - 🛡️ **Shields**: Temporarily avoid crash damage.  
- **Obstacles**:  
  - 🐦 **Birds**: Fast-moving horizontal threats.  
  - ☁️ **Clouds**: Slow-moving obstacles.  
- **Height Tracking**: Compete for your highest altitude (measured in meters).  
- **Collision System**: Shield mechanics and crash detection.  
- **HUD**: Real-time stats for height, fuel, and shield duration.  
- **Smooth Scrolling**: Simulated ascent via background movement.  

---

## 🛠️ Installation  
1. **Prerequisites**:  
   - Python 3.8+  
   - Pygame library

   ```bash
   pip install pygame
   ```
2. **Clone the Repository:**
   
    ```bash
    git clone https://github.com/antoniosimuncic/balloon-game.git
    cd balloon-game
    ```
3. **Run the Game:**

   ```bash
   python balloon_game.py
   ```

## 🎮 How to Play  

**Controls**
- **A / Left Arrow:** Move balloon left.
- **D / Right Arrow:** Move balloon right.
- **Close Window:** Quit the game.

**Objectives**
- Avoid crashing into birds and clouds.
- Collect fuel canisters to stay airborne longer.
- Use shields to survive unavoidable collisions.
- Achieve the highest possible altitude!

**Power-Up Effects**  

| Power-Up |	Effect	| Duration |
|----------|----------|----------|
| Fuel	   | +20 fuel units	| Instant |
| Shield	 | Invincibility	| 6 seconds |

## Code Structure

```
balloon-game/  
├── assets/                # Entity Images
│   ├── balloon.png
|   ├── balloon-shield.png       
│   ├── bird.png           
│   ├── cloud.png
|   ├── fuel.png           
│   └── shield.png           
├── core/                  
│   ├── entity.py          # Base Entity class
│   ├── game_managers.py   # ObstacleManager, PowerUpManager and CollisionManager
│   └── settings.py        # GameSettings constants
├── documentation/
|   ├── task.md            # University Course task
|   ├── uml-diagram.png    # UML diagram screenshot
|   ├── uml-diagram.drawio 
|   └── screenshot.png     # Game screenshot for README.md
├── objects/               
│   ├── balloon.py         # Player-controlled balloon
│   ├── obstacle.py        # Obstacle classes (Bird/Cloud)
│   └── power_up.py        # Power-up classes (Fuel/Shield)
└── balloon_game.py        # Main game loop and entry point
```  

**Key Design Patterns**
- **Factory Method:** Used in `ObstacleManager` and `PowerUpManager` for object spawning.
- **Mediator:** `CollisionManager` handles collision logic between unrelated components.
- **Template Method:** Used in `Entity` base class that subclasses inherit and override.
- **Object-Oriented Design:** Clear separation of entities (Balloon, Obstacle, PowerUp).

## Technical Details  
- **Delta Time:** Frame-rate independent movement using dt (time since last frame).
- **Collision Detection:** AABB (Axis-Aligned Bounding Box) via Entity.collides_with().
- **Scrolling Illusion:** Achieved by moving obstacles/power-ups downward while keeping the balloon fixed.

## UML Diagram

<img src="https://github.com/antoniosimuncic/balloon-game/blob/main/documentation/uml-diagram.png">