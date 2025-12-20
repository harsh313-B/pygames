import pygame

pygame.init()

w_width = 500
w_height = 500
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Shooting Game")

clock = pygame.time.Clock()
bg_img = pygame.image.load("/home/raven/Public/pygames/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f"/home/raven/Public/pygames/soldier/{num}.png") for num in range(1, 10)]
walkLeft = [pygame.image.load(f"/home/raven/Public/pygames/soldier/L{num}.png") for num in range(1, 10)]
char = pygame.image.load("/home/raven/Public/pygames/soldier/standing.png")
moveLeft = [pygame.image.load(f'/home/raven/Public/pygames/enemy/L{i}.png') for i in range(1, 9)]
moveRight = [pygame.image.load(f'/home/raven/Public/pygames/enemy/R{i}.png') for i in range(1, 9)]
font = pygame.font.SysFont("helvetica", 30, 1, 1)
score = 0
bulletsound = pygame.mixer.Sound("/home/raven/Public/pygames/sounds/Bulletsound.ogg")
hitsound = pygame.mixer.Sound("/home/raven/Public/pygames/sounds/Hit.ogg")
music = pygame.mixer.music.load("/home/raven/Public/pygames/sounds/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

class player():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.facing = 1
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)

    def draw(self, screen):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                screen.blit(walkRight[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            # show the correct facing when standing (use first walk frame)
            if self.facing == 1:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        #pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 2)
        self.hit = pygame.Rect(self.hitbox)
    
    def touch(self):
        self.x = 0
        self.y = w_height - self.height


class projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class enemy():
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walk_count = 0
        self.vel = 3
        # patrol path: from given x to right edge minus enemy width
        self.path = [x, w_width - self.width]
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 10
        self.max_health = 10
        self.visible = True

    def draw(self, screen):
            if self.visible:
                # enemy has 8 frames; 8 * 3 = 24 animation ticks
                if self.walk_count + 1 >= 24:
                    self.walk_count = 0

                if self.vel > 0:
                    screen.blit(moveRight[self.walk_count // 3], (self.x, self.y))
                    self.walk_count += 1
                else:
                    screen.blit(moveLeft[self.walk_count // 3], (self.x, self.y))
                    self.walk_count += 1
                self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
                #pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 2)
                self.hit = pygame.Rect(self.hitbox)
                # draw health background and scaled health bar
                pygame.draw.rect(screen, (128, 128, 128), (self.hitbox[0], self.hitbox[1] + 3, 50, 10), 0)
                green_width = int(50 * max(self.health, 0) / self.max_health)
                if green_width > 0:
                    pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] + 3, green_width, 10), 0)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0
        else:
            if self.x > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0
    def touch(self):
        hitsound.play()
        if self.health > 0:
            self.health -= 1
            if self.health <= 0:
                self.visible = False
        

def DrawInGameloop():

    screen.blit(bg_img, (0, 0))
    clock.tick(25)
    solder.draw(screen)
    text = font.render("Score: " + str(score), 1, (255, 0, 0))
    screen.blit(text, (0, 10))
    # update enemy position along its patrol before drawing
    enemy_obj.move()
    enemy_obj.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

solder = player(210, 435, 64, 64)
enemy_obj = enemy(0, w_width - 64, 64, 64)
bullets = []
shoot = 0
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    if enemy_obj.visible:
        if solder.hit.colliderect(enemy_obj.hit):
            enemy_obj.vel = enemy_obj.vel * -1
            solder.touch()

    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    for bullet in bullets:
        if enemy_obj.visible:
            if bullet.y - bullet.radius < enemy_obj.hitbox[1] + enemy_obj.hitbox[3] and bullet.y + bullet.radius > enemy_obj.hitbox[1]:
                if bullet.x + bullet.radius > enemy_obj.hitbox[0] and bullet.x - bullet.radius < enemy_obj.hitbox[0] + enemy_obj.hitbox[2]:
                    #print("Hit!")
                    bullets.pop(bullets.index(bullet))
                    score += 1
                    enemy_obj.touch()

        if 0 < bullet.x < w_width:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shoot == 0:
        bulletsound.play()
        facing = solder.facing
        if len(bullets) < 5:
            bullets.append(projectile(round(solder.x + solder.width // 2), round(solder.y + solder.height // 2), 6, (19, 12, 22), facing))
        shoot = 1

    if keys[pygame.K_LEFT] and solder.x > 0:
        solder.x -= 5
        solder.left = True
        solder.right = False
        solder.facing = -1
        solder.standing = False

    elif keys[pygame.K_RIGHT] and solder.x < w_width - solder.width:
        solder.x += 5
        solder.left = False
        solder.right = True
        solder.facing = 1
        solder.standing = False

    else:
        solder.standing = True
        solder.left = False
        solder.right = False
        solder.walk_count = 0

    if not(solder.is_jump):
        if keys[pygame.K_UP]:
            solder.is_jump = True
            # preserve last facing while jumping
            solder.walk_count = 0
    
    else:
        if solder.is_jump:
            if solder.jump_count >= -10:
                neg = 1
                if solder.jump_count < 0:
                    neg = -1
                solder.y -= int((solder.jump_count ** 2) * 0.5 * neg)
                solder.jump_count -= 1
            else:
                solder.is_jump = False
                solder.jump_count = 10
    
    DrawInGameloop()
    #WIP test commit
    