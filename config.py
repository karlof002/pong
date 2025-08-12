"""
Configuration constants for the Pong game.
"""
import math

# ----------------------------
# Display Settings
# ----------------------------
WIDTH, HEIGHT = 960, 540
FPS = 120

# ----------------------------
# Colors
# ----------------------------
BG = (12, 12, 20)           # Background
FG = (240, 240, 255)        # Foreground
ACCENT = (100, 170, 255)    # Accent color
DIM = (120, 120, 140)       # Dimmed color

# ----------------------------
# Game Object Sizes
# ----------------------------
PADDLE_W, PADDLE_H = 14, 110
BALL_R = 9

# ----------------------------
# Physics Settings
# ----------------------------
PLAYER_SPEED = 640.0           # px/s
BASE_BALL_SPEED = 420.0        # px/s
BALL_SPEED_GROWTH = 1.035      # per paddle hit
BALL_SPEED_MAX = 1200.0        # cap
MAX_BOUNCE_ANGLE = math.radians(50)  # max deflection angle from horizontal
SPIN_FROM_PADDLE_V = 0.22      # how much paddle vertical velocity influences ball vy

# ----------------------------
# Visual Elements
# ----------------------------
NET_DASH = 14
NET_GAP = 14

# ----------------------------
# AI Difficulty Settings
# ----------------------------
DIFFS = {
    "Easy":   {"ai_speed": 520.0, "noise": 42.0, "react": 0.11},
    "Medium": {"ai_speed": 720.0, "noise": 18.0, "react": 0.06},
    "Hard":   {"ai_speed": 940.0, "noise": 6.0,  "react": 0.03},
}
DIFF_ORDER = ["Easy", "Medium", "Hard"]

# ----------------------------
# Play Field Bounds
# ----------------------------
# Play field bounds for ball center (account for radius)
TOP = BALL_R + 10
BOTTOM = HEIGHT - BALL_R - 10
LEFT = 10 + BALL_R
RIGHT = WIDTH - 10 - BALL_R
