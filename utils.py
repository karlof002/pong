"""
Utility functions for the Pong game.
"""
from config import TOP, BOTTOM


def clamp(v, lo, hi):
    """Clamp a value between lo and hi."""
    return lo if v < lo else hi if v > hi else v


def sign(x):
    """Return the sign of x (-1, 0, or 1)."""
    return -1 if x < 0 else 1


def predict_y_at_x(x0, y0, vx, vy, x_target):
    """
    Predict ball y at a given target x, simulating bounces on top/bottom.
    """
    # If ball not moving towards target, return current y to avoid overreacting
    if (x_target - x0) * vx <= 0 or abs(vx) < 1e-5:
        return y0
    
    # Step simulation in x to handle multiple bounces without heavy math
    step = max(1.5, abs(vx) * 0.002)  # adaptive step
    x, y = x0, y0
    slope = vy / vx
    direction = 1 if vx > 0 else -1
    
    while (x < x_target and direction > 0) or (x > x_target and direction < 0):
        next_x = x + direction * step
        if (direction > 0 and next_x > x_target) or (direction < 0 and next_x < x_target):
            next_x = x_target
        
        dx = next_x - x
        y += slope * dx
        
        # Reflect on bounds
        if y <= TOP:
            y = TOP + (TOP - y)
            slope = -slope
        elif y >= BOTTOM:
            y = BOTTOM - (y - BOTTOM)
            slope = -slope
        
        x = next_x
    
    return y
