"""
Main game class and logic.
"""
import random
import sys
import pygame as pg
from config import *
from entities import Paddle, Ball
from ai import AI


class Game:
    """Main game class that handles game logic, rendering, and events."""
    
    def __init__(self):
        pg.init()
        pg.display.set_caption("Pong game")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 26)
        self.small = pg.font.SysFont("consolas", 18)

        self.left = Paddle(40 + PADDLE_W/2, HEIGHT/2)
        self.right = Paddle(WIDTH - 40 - PADDLE_W/2, HEIGHT/2)
        self.ball = Ball()
        self.ai = AI(self.right, "right")

        self.score_l = 0
        self.score_r = 0
        self.paused = False

    def reset_rally(self, direction=None):
        """Reset the ball for a new rally."""
        if direction is None:
            direction = random.choice([-1, 1])
        self.ball.reset(direction)

    def update(self, dt):
        """Update game state."""
        # Input
        keys = pg.key.get_pressed()
        vy = 0.0
        if keys[pg.K_w]:
            vy -= PLAYER_SPEED
        if keys[pg.K_s]:
            vy += PLAYER_SPEED
        self.left.move(vy, dt)

        if not self.paused:
            # Ball and AI updates
            self.ball.update(dt)
            self.right.move(0.0, 0.0)  # keep last vy if needed
            self.ai.update(self.ball, dt)

            # Collisions
            self.ball.collide_with_paddle(self.left)
            self.ball.collide_with_paddle(self.right)

            # Scoring
            if self.ball.x < LEFT - 30:
                self.score_r += 1
                self.reset_rally(direction=1)
            elif self.ball.x > RIGHT + 30:
                self.score_l += 1
                self.reset_rally(direction=-1)

    def draw_net(self):
        """Draw the center net."""
        y = 0
        x = WIDTH // 2
        while y < HEIGHT:
            pg.draw.rect(self.screen, DIM, (x - 2, y, 4, NET_DASH))
            y += NET_DASH + NET_GAP

    def draw_hud(self):
        """Draw the heads-up display (scores, controls, etc.)."""
        # Scores
        s_txt = self.font.render(f"{self.score_l}", True, FG)
        self.screen.blit(s_txt, (WIDTH * 0.25 - s_txt.get_width()/2, 24))
        s2_txt = self.font.render(f"{self.score_r}", True, FG)
        self.screen.blit(s2_txt, (WIDTH * 0.75 - s2_txt.get_width()/2, 24))
        
        # Difficulty
        d_txt = self.small.render(f"Difficulty: {self.ai.name}  [1/2/3]", True, DIM)
        self.screen.blit(d_txt, (12, HEIGHT - 24))
        
        # Pause hint
        p_txt = self.small.render("W/S move | P pause | R reset | Esc quit", True, DIM)
        self.screen.blit(p_txt, (WIDTH - p_txt.get_width() - 12, HEIGHT - 24))

        if self.paused:
            t = self.font.render("PAUSED", True, ACCENT)
            self.screen.blit(t, (WIDTH/2 - t.get_width()/2, HEIGHT/2 - t.get_height()/2))

    def draw_bounds(self):
        """Draw the game field boundaries."""
        # Side walls
        pg.draw.rect(self.screen, DIM, (6, 6, WIDTH-12, HEIGHT-12), width=2, border_radius=8)

    def render(self):
        """Render the entire game screen."""
        self.screen.fill(BG)
        self.draw_bounds()
        self.draw_net()
        self.left.draw(self.screen)
        self.right.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_hud()
        pg.display.flip()

    def handle_events(self):
        """Handle pygame events."""
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)
                elif e.key == pg.K_p:
                    self.paused = not self.paused
                elif e.key == pg.K_r:
                    self.reset_rally()
                elif e.key == pg.K_1:
                    self.ai.set_difficulty("Easy")
                elif e.key == pg.K_2:
                    self.ai.set_difficulty("Medium")
                elif e.key == pg.K_3:
                    self.ai.set_difficulty("Hard")

    def run(self):
        """Main game loop."""
        while True:
            dt = self.clock.tick(FPS) / 1000.0  # seconds
            self.handle_events()
            self.update(dt)
            self.render()
