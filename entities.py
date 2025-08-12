"""
Game entities: Paddle and Ball classes.
"""
import math
import random
import pygame as pg
from config import *
from utils import clamp, sign


class Paddle:
    """Represents a paddle in the game."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0.0
        self.w = PADDLE_W
        self.h = PADDLE_H

    @property
    def rect(self):
        """Get the paddle's rectangle for collision detection."""
        return pg.Rect(int(self.x - self.w/2), int(self.y - self.h/2), self.w, self.h)

    def move(self, vy, dt):
        """Move the paddle with given vertical velocity."""
        self.vy = vy
        self.y += self.vy * dt
        self.y = clamp(self.y, TOP + self.h/2, BOTTOM - self.h/2)

    def draw(self, surf, color=FG):
        """Draw the paddle on the given surface."""
        pg.draw.rect(surf, color, self.rect, border_radius=6)


class Ball:
    """Represents the ball in the game."""
    
    def __init__(self):
        self.reset(direction=random.choice([-1, 1]))

    def reset(self, direction=1):
        """Reset the ball to center with random angle."""
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        angle = random.uniform(-0.30, 0.30)  # start mostly horizontal
        self.speed = BASE_BALL_SPEED
        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
        self.trail = []

    def update(self, dt):
        """Update ball position and handle wall bounces."""
        # Trail (store last N positions)
        self.trail.append((self.x, self.y))
        if len(self.trail) > 22:
            self.trail.pop(0)
        
        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Wall bounce
        if self.y <= TOP:
            self.y = TOP
            self.vy = -self.vy
        elif self.y >= BOTTOM:
            self.y = BOTTOM
            self.vy = -self.vy

    def collide_with_paddle(self, paddle: Paddle):
        """Handle collision with a paddle."""
        if self.rect().colliderect(paddle.rect):
            # Rewind to edge to avoid sticking
            if self.vx > 0:
                self.x = paddle.rect.left - BALL_R
            else:
                self.x = paddle.rect.right + BALL_R

            # Compute bounce angle based on contact point
            offset = (self.y - paddle.y) / (paddle.h / 2.0)
            offset = clamp(offset, -1.0, 1.0)
            angle = offset * MAX_BOUNCE_ANGLE
            
            # Increase speed with cap
            self.speed = min(self.speed * BALL_SPEED_GROWTH, BALL_SPEED_MAX)
            
            # New velocity (flip horizontal direction)
            direction = -sign(self.vx)
            self.vx = direction * self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)
            
            # Add a bit of spin from paddle movement
            self.vy += paddle.vy * SPIN_FROM_PADDLE_V

    def rect(self):
        """Get the ball's rectangle for collision detection."""
        return pg.Rect(int(self.x - BALL_R), int(self.y - BALL_R), BALL_R*2, BALL_R*2)

    def draw(self, surf):
        """Draw the ball and its trail on the given surface."""
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            t = i / max(1, len(self.trail)-1)
            alpha = int(30 + 140 * t)
            r = int(BALL_R * (0.5 + 0.5 * t))
            trail_color = (ACCENT[0], ACCENT[1], ACCENT[2], alpha)
            s = pg.Surface((r*2, r*2), pg.SRCALPHA)
            pg.draw.circle(s, trail_color, (r, r), r)
            surf.blit(s, (tx - r, ty - r))
        
        # Draw ball
        pg.draw.circle(surf, FG, (int(self.x), int(self.y)), BALL_R)
