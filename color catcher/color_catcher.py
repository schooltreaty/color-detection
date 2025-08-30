# color_catcher_blue.py
import cv2
import numpy as np
import pygame
import sys
import random

# ----------------------------
# Config / Tweakable settings
# ----------------------------
GAME_WIDTH, GAME_HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 160, 22
FPS = 60

# Camera capture resolution
CAPTURE_W, CAPTURE_H = 640, 480

# BLUE HSV range
LOWER_BLUE = np.array([100, 150, 0])
UPPER_BLUE = np.array([140, 255, 255])

# Smoothing factor for paddle movement (0..1)
SMOOTH_ALPHA = 0.35

# Falling items params
FALL_SPEED_BASE = 3.5
SPAWN_INTERVAL_MS = 1100
SPAWN_VARIANCE = 600

# Camera thumbnail size
CAM_PREVIEW_W, CAM_PREVIEW_H = 200, 150

# Minimum contour area to consider
MIN_CONTOUR_AREA = 600

# ----------------------------
# Helper classes
# ----------------------------
class FallingItem:
    def __init__(self, x, size, speed, color):
        self.rect = pygame.Rect(x, -size, size, size)
        self.speed = speed
        self.color = color

    def update(self):
        self.rect.y += self.speed

    def draw(self, surf):
        pygame.draw.ellipse(surf, self.color, self.rect)

# ----------------------------
# Main game
# ----------------------------
def main(cam_index=0):
    # Initialize camera
    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_H)
    if not cap.isOpened():
        print("ERROR: Could not open webcam. Try changing camera index (0/1/2).")
        return

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption("Color Catcher - Blue Object")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    bigfont = pygame.font.SysFont(None, 72)

    # Game state
    paddle = pygame.Rect((GAME_WIDTH - PADDLE_W) // 2, GAME_HEIGHT - 60, PADDLE_W, PADDLE_H)
    items = []
    score = 0
    lives = 3
    running = True
    game_over = False

    last_spawn_time = pygame.time.get_ticks()
    next_spawn_delay = SPAWN_INTERVAL_MS + random.randint(-SPAWN_VARIANCE//2, SPAWN_VARIANCE//2)

    prev_mapped_x = paddle.centerx

    while running:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    items.clear()
                    score = 0
                    lives = 3
                    game_over = False
                    prev_mapped_x = paddle.centerx
                elif event.key == pygame.K_q:
                    running = False

        # --- Read camera frame ---
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)

        # --- Color detection (OpenCV) ---
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected = False
        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            if area > MIN_CONTOUR_AREA:
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    mapped_x = int(cx * GAME_WIDTH / CAPTURE_W)
                    mapped_x_smoothed = int(SMOOTH_ALPHA * mapped_x + (1 - SMOOTH_ALPHA) * prev_mapped_x)
                    prev_mapped_x = mapped_x_smoothed
                    paddle.centerx = max(PADDLE_W // 2, min(GAME_WIDTH - PADDLE_W // 2, mapped_x_smoothed))
                    detected = True

        # --- Spawn new items ---
        now = pygame.time.get_ticks()
        if not game_over and (now - last_spawn_time) > next_spawn_delay:
            size = random.randint(18, 42)
            x = random.randint(0, GAME_WIDTH - size)
            speed = FALL_SPEED_BASE + random.random() * 2.5 + score * 0.03
            color = random.choice([(255,80,80), (80,200,100), (120,180,255), (255,215,80)])
            items.append(FallingItem(x, size, speed, color))
            last_spawn_time = now
            next_spawn_delay = max(250, SPAWN_INTERVAL_MS + random.randint(-SPAWN_VARIANCE//2, SPAWN_VARIANCE//2) - score*5)

        # --- Update items and collisions ---
        if not game_over:
            for item in items[:]:
                item.update()
                if item.rect.colliderect(paddle):
                    score += 1
                    try:
                        items.remove(item)
                    except ValueError:
                        pass
                elif item.rect.top > GAME_HEIGHT:
                    lives -= 1
                    try:
                        items.remove(item)
                    except ValueError:
                        pass
                    if lives <= 0:
                        game_over = True

        # --- Draw ---
        screen.fill((18, 20, 30))
        for item in items:
            item.draw(screen)
        pygame.draw.rect(screen, (240, 240, 240), paddle, border_radius=8)

        hud = font.render(f"Score: {score}   Lives: {lives}", True, (230, 230, 230))
        screen.blit(hud, (14, 10))

        # Camera preview
        try:
            small = cv2.resize(frame, (CAM_PREVIEW_W, CAM_PREVIEW_H))
            small_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            cam_surf = pygame.image.frombuffer(small_rgb.tobytes(), (CAM_PREVIEW_W, CAM_PREVIEW_H), 'RGB')
            screen.blit(cam_surf, (GAME_WIDTH - CAM_PREVIEW_W - 10, 10))
        except Exception:
            pass

        if not detected:
            hint = font.render("Show a BLUE object to control the paddle", True, (200, 200, 200))
            screen.blit(hint, (14, GAME_HEIGHT - 30))

        if game_over:
            over_txt = bigfont.render("GAME OVER", True, (220, 60, 60))
            restart_txt = font.render("Press R to restart or Q to quit", True, (200, 200, 200))
            screen.blit(over_txt, ((GAME_WIDTH - over_txt.get_width())//2, GAME_HEIGHT//2 - 60))
            screen.blit(restart_txt, ((GAME_WIDTH - restart_txt.get_width())//2, GAME_HEIGHT//2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main(cam_index=0)
