import os
import tempfile
import webbrowser

# This script generates a self-contained HTML5 Bouncing Ball game
# and automatically opens it in your default web browser.

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Bounce</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --glass-bg: rgba(30, 41, 59, 0.6);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --accent-1: #0ea5e9; /* Light blue */
            --accent-2: #8b5cf6; /* Purple */
            --ball-color: #f43f5e; /* Rose */
            --paddle-color: #10b981; /* Emerald */
        }

        * {
            box-sizing: border-box;
            user-select: none;
        }

        body {
            font-family: 'Outfit', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: var(--bg-color);
            background-image: 
                radial-gradient(at 20% 20%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 80% 0%, hsla(225,39%,30%,0.5) 0, transparent 50%), 
                radial-gradient(at 10% 80%, hsla(339,49%,30%,0.5) 0, transparent 50%);
            color: var(--text-main);
            overflow: hidden;
        }

        .container {
            text-align: center;
            background: var(--glass-bg);
            padding: 2rem 3rem;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            animation: fadeIn 1s ease-out;
            position: relative;
            z-index: 10;
        }

        h1 {
            margin-top: 0;
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(to right, var(--accent-1), var(--accent-2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            text-shadow: 0px 4px 20px rgba(139, 92, 246, 0.3);
        }

        .stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 700;
        }

        .score-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 8px 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .score-val {
            color: var(--accent-1);
            font-size: 1.5rem;
            text-shadow: 0 0 10px rgba(14, 165, 233, 0.6);
        }

        .canvas-container {
            position: relative;
            margin: 0 auto;
        }

        canvas {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 16px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8), 0 0 30px rgba(14, 165, 233, 0.2);
            border: 1px solid var(--glass-border);
            cursor: none; /* Hide cursor over canvas for better immersion */
            display: block;
        }

        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.85);
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(5px);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .overlay.active {
            opacity: 1;
            pointer-events: all;
        }

        .overlay h2 {
            font-size: 3rem;
            color: var(--ball-color);
            margin: 0 0 1rem 0;
            text-shadow: 0 0 20px rgba(244, 63, 94, 0.6);
        }

        .btn {
            padding: 12px 36px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
            margin-top: 10px;
        }

        .btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6);
        }

        .btn:active {
            transform: translateY(0) scale(0.95);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* Background floating orbs */
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            z-index: 1;
            opacity: 0.4;
            animation: floatOrb 25s infinite alternate ease-in-out;
        }

        .orb-1 {
            width: 350px;
            height: 350px;
            background: var(--accent-1);
            top: -100px;
            left: -100px;
        }

        .orb-2 {
            width: 450px;
            height: 450px;
            background: var(--ball-color);
            bottom: -150px;
            right: -100px;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .orb-3 {
            width: 300px;
            height: 300px;
            background: var(--accent-2);
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -10s;
        }

        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(100px, 100px) scale(1.1); }
            66% { transform: translate(-50px, 150px) scale(0.9); }
            100% { transform: translate(100px, -50px) scale(1.2); }
        }

        .watermark {
            position: fixed;
            bottom: 15px;
            right: 20px;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.3);
            pointer-events: none;
            z-index: 5;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    
    <div class="container">
        <h1>Neon Bounce</h1>
        <div class="stats">
            <div class="score-box">Level: <span id="levelVal" class="score-val" style="color: var(--accent-2)">1</span></div>
            <div class="score-box">Score: <span id="scoreVal" class="score-val">0</span></div>
        </div>
        
        <div class="canvas-container">
            <canvas id="gameCanvas" width="700" height="450"></canvas>
            
            <div id="startScreen" class="overlay active">
                <h2 style="color: white; text-shadow: 0 0 20px var(--accent-1);">Ready?</h2>
                <p style="margin-bottom: 2rem; font-size: 1.2rem; color: rgba(255,255,255,0.7);">Use your mouse to move the paddle.</p>
                <button id="startBtn" class="btn">Start Game</button>
            </div>

            <div id="gameOverScreen" class="overlay">
                <h2>GAME OVER</h2>
                <p style="font-size: 1.5rem; margin-bottom: 5px;">Final Score: <span id="finalScore" class="score-val">0</span></p>
                <p style="margin-bottom: 2rem; color: rgba(255,255,255,0.6);">You reached Level <span id="finalLevel">1</span></p>
                <button id="restartBtn" class="btn">Play Again</button>
            </div>
        </div>
    </div>
    
    <div class="watermark">Designed by Dheeraj</div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('scoreVal');
        const levelElement = document.getElementById('levelVal');
        
        const startScreen = document.getElementById('startScreen');
        const gameOverScreen = document.getElementById('gameOverScreen');
        const startBtn = document.getElementById('startBtn');
        const restartBtn = document.getElementById('restartBtn');
        const finalScoreEl = document.getElementById('finalScore');
        const finalLevelEl = document.getElementById('finalLevel');

        // Game Configuration
        const paddleHeight = 12;
        const paddleWidth = 100;
        const ballRadius = 10;
        const baseSpeed = 4;
        
        // Colors mapping from CSS vars (hex values)
        const cRose = '#f43f5e';
        const cEmerald = '#10b981';
        const cSky = '#0ea5e9';

        // State Variables
        let paddleX = (canvas.width - paddleWidth) / 2;
        let ballX, ballY, dx, dy;
        let score = 0;
        let level = 1;
        let hits = 0; // hits to next level
        let gameActive = false;
        let animationId;
        
        // Particles system for explosion effect
        let particles = [];

        // Track mouse position relative to canvas
        function mouseMoveHandler(e) {
            if (!gameActive) return;
            const relativeX = e.clientX - canvas.getBoundingClientRect().left;
            if(relativeX > 0 && relativeX < canvas.width) {
                paddleX = relativeX - paddleWidth / 2;
                
                // Keep paddle within bounds
                if(paddleX < 0) paddleX = 0;
                if(paddleX + paddleWidth > canvas.width) paddleX = canvas.width - paddleWidth;
            }
        }
        
        // Mobile touch support
        function touchMoveHandler(e) {
            if (!gameActive) return;
            e.preventDefault();
            const relativeX = e.touches[0].clientX - canvas.getBoundingClientRect().left;
            if(relativeX > 0 && relativeX < canvas.width) {
                paddleX = relativeX - paddleWidth / 2;
                if(paddleX < 0) paddleX = 0;
                if(paddleX + paddleWidth > canvas.width) paddleX = canvas.width - paddleWidth;
            }
        }

        document.addEventListener('mousemove', mouseMoveHandler, false);
        document.addEventListener('touchmove', touchMoveHandler, {passive: false});

        function createParticles(x, y, color) {
            for (let i = 0; i < 15; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 8,
                    vy: (Math.random() - 0.5) * 8,
                    life: 1,
                    color: color
                });
            }
        }

        function drawParticles() {
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.life * 3, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(${hexToRgb(p.color)}, ${p.life})`;
                ctx.fill();
                ctx.closePath();
                
                p.x += p.vx;
                p.y += p.vy;
                p.life -= 0.05;
                
                if (p.life <= 0) {
                    particles.splice(i, 1);
                }
            }
        }

        // Helper to convert hex to rgb for particle opacity
        function hexToRgb(hex) {
            let r = parseInt(hex.slice(1, 3), 16),
                g = parseInt(hex.slice(3, 5), 16),
                b = parseInt(hex.slice(5, 7), 16);
            return `${r}, ${g}, ${b}`;
        }

        function drawBall() {
            ctx.beginPath();
            ctx.arc(ballX, ballY, ballRadius, 0, Math.PI*2);
            ctx.fillStyle = cRose;
            ctx.shadowColor = cRose;
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.shadowBlur = 0; // reset
            ctx.closePath();
        }

        function drawPaddle() {
            ctx.beginPath();
            ctx.roundRect(paddleX, canvas.height - paddleHeight - 15, paddleWidth, paddleHeight, 6);
            ctx.fillStyle = cEmerald;
            ctx.shadowColor = cEmerald;
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.closePath();
        }

        function draw() {
            if (!gameActive) return;

            // Clear canvas completely to remove tail
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            drawBall();
            drawPaddle();
            drawParticles();

            // Wall collision (left/right)
            if (ballX + dx > canvas.width - ballRadius || ballX + dx < ballRadius) {
                dx = -dx;
                // Add minor variation
                dx += (Math.random() - 0.5) * 0.5;
            }
            
            // Wall collision (top)
            if (ballY + dy < ballRadius) {
                dy = -dy;
            } 
            // Bottom area (paddle or game over)
            else if (ballY + dy > canvas.height - ballRadius - 15 - paddleHeight/2) {
                // Check if ball is within paddle horizontal bounds
                if (ballX > paddleX - ballRadius && ballX < paddleX + paddleWidth + ballRadius && ballY < canvas.height - 15) {
                    // Bounce!
                    dy = -Math.abs(dy); // Ensure it goes up
                    
                    // Add "spin" based on where it hit the paddle
                    let hitPoint = ballX - (paddleX + paddleWidth / 2);
                    let normalizedHitPoint = hitPoint / (paddleWidth / 2); // -1 to 1
                    dx = dx + (normalizedHitPoint * 2); // Change horizontal speed based on hit location
                    
                    // Limit max horizontal speed
                    const maxDx = 8;
                    if (dx > maxDx) dx = maxDx;
                    if (dx < -maxDx) dx = -maxDx;
                    
                    score += 10;
                    hits++;
                    scoreElement.innerText = score;
                    createParticles(ballX, ballY + ballRadius, cEmerald);
                    
                    // Level up
                    if (hits >= 5) {
                        level++;
                        hits = 0;
                        levelElement.innerText = level;
                        // Increase speed but keep direction
                        let speedMultiplier = 1.1;
                        dx *= speedMultiplier;
                        dy *= speedMultiplier;
                    }
                }
                else if (ballY + dy > canvas.height - ballRadius) {
                    // Passed the paddle -> Game Over
                    gameOver();
                    return;
                }
            }

            ballX += dx;
            ballY += dy;

            animationId = requestAnimationFrame(draw);
        }

        function initGame() {
            // Reset state
            paddleX = (canvas.width - paddleWidth) / 2;
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            score = 0;
            level = 1;
            hits = 0;
            scoreElement.innerText = score;
            levelElement.innerText = level;
            particles = [];
            
            // Initial random speed
            dx = (Math.random() > 0.5 ? 1 : -1) * baseSpeed;
            dy = baseSpeed;

            startScreen.classList.remove('active');
            gameOverScreen.classList.remove('active');
            
            // Clear canvas completely
            ctx.fillStyle = 'rgba(15, 23, 42, 1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            gameActive = true;
            draw();
        }

        function gameOver() {
            gameActive = false;
            cancelAnimationFrame(animationId);
            createParticles(ballX, ballY, cRose);
            
            // Draw one last frame with explosion
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawParticles();
            
            setTimeout(() => {
                finalScoreEl.innerText = score;
                finalLevelEl.innerText = level;
                gameOverScreen.classList.add('active');
            }, 500);
        }

        startBtn.addEventListener('click', initGame);
        restartBtn.addEventListener('click', initGame);
    </script>
</body>
</html>
"""

def launch_game():
    # Create a temporary HTML file securely
    fd, path = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, 'w') as f:
        f.write(HTML_CONTENT)
    
    # Open the file in the default web browser
    print("Launching Neon Bounce GUI in your web browser...")
    webbrowser.open('file://' + os.path.realpath(path))

if __name__ == "__main__":
    # In some IDEs or setups, we might want to keep the terminal open briefly
    try:
        launch_game()
        print("Game running! You can close this terminal window once the browser opens.")
    except Exception as e:
        print(f"Error launching game: {e}")
