"""
AI controller for the computer paddle.
"""
import random
from config import DIFFS, TOP, BOTTOM, BALL_R
from utils import clamp, predict_y_at_x
from entities import Paddle, Ball


class AI:
    """AI controller for computer-controlled paddle."""
    
    def __init__(self, paddle: Paddle, side="right"):
        self.paddle = paddle
        self.side = side
        self.set_difficulty("Medium")
        self.reaction_timer = 0.0
        self.target_y = paddle.y

    def set_difficulty(self, name):
        """Set the AI difficulty level."""
        d = DIFFS[name]
        self.name = name
        self.ai_speed = d["ai_speed"]
        self.noise = d["noise"]
        self.react = d["react"]

    def update(self, ball: Ball, dt):
        """Update AI paddle movement based on ball position."""
        # Reaction delay timer
        self.reaction_timer -= dt
        if self.reaction_timer <= 0.0:
            # Predict y at our x edge
            x_target = self.paddle.rect.left - BALL_R if self.side == "right" else self.paddle.rect.right + BALL_R
            py = predict_y_at_x(ball.x, ball.y, ball.vx, ball.vy, x_target)
            
            # Add slight noise to avoid perfection
            py += random.uniform(-self.noise, self.noise)
            
            # Clamp to playable range
            self.target_y = clamp(py, TOP + self.paddle.h/2, BOTTOM - self.paddle.h/2)
            
            # Reset reaction timer (shorter at higher difficulty)
            self.reaction_timer = self.react

        # Move towards target with capped speed
        delta = self.target_y - self.paddle.y
        desired_v = clamp(delta / max(dt, 1e-6), -self.ai_speed, self.ai_speed)
        self.paddle.move(desired_v, dt)
