# Neon Bounce 

A beautifully styled, modern HTML5 bouncing ball game disguised as a simple Python script.

This project uses Python's standard library to dynamically generate a web-based GUI and play the game directly in your default browser. This approach requires **zero external dependencies** (no Pygame, PyQt, or Tkinter required!).

## Features
- **Glassmorphism UI**: Beautiful, modern frosted glass UI components.
- **Dynamic Lighting**: Neon glow effects for the ball and paddle.
- **Particle System**: Burst effects on paddle hits and game over.
- **Responsive Gameplay**: Smooth physics and progressive difficulty scaling.
- **Zero Dependencies**: Uses nothing but Python standard libraries (`os`, `tempfile`, `webbrowser`).

## How to Play
1. Make sure you have Python installed.
2. Run the script from your terminal:
   ```bash
   python bouncing_ball.py
   ```
3. Your default web browser will automatically open the game.
4. Use your **mouse** (or touchscreen) to move the paddle left and right.
5. Keep the ball from falling! The speed increases every 5 hits.
## How It Works
Instead of using complex GUI frameworks like Tkinter or Pygame, this game leverages modern web technologies. The Python script contains the entire game logic written in HTML, CSS, and JavaScript. When executed, Python writes this string to a secure temporary file and opens it in your default web browser, giving you a beautiful game interface with hardware-accelerated animations.

## Customization
You can easily customize the game by opening `bouncing_ball.py` in your editor:
- **Colors**: Look for the CSS `:root` variables to change the neon accents (`--accent-1`, `--accent-2`, `--ball-color`, `--paddle-color`).
- **Speed**: Modify `baseSpeed` in the JavaScript section to make the game start faster or slower.

## Author
Designed by Dheeraj.
