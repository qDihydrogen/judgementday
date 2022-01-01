import pygame  # actual visuals
import random  # i sure wonder
import math
from sys import exit
import datetime
pygame.init()  # no preinit to lower buffer, this is a mediocre jam remember?

WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))  # no resizing capabilities because lazy
pygame.display.set_caption('judgement day hahahaha')

clock = pygame.time.Clock()
FPS = 60

with open('highscore.txt', 'r') as f:
    try:
        a = f.readlines()
        highscore = float(a[0])
        nohighscore = False
    except Exception:
        highscore = -1
        nohighscore = True

font_title = pygame.font.Font('assets/Verdana.ttf', 48)
font_small = pygame.font.Font('assets/Verdana.ttf', 20)
font_play = pygame.font.Font('assets/Verdana.ttf', 30)
font_tiny = pygame.font.Font('assets/Verdana.ttf', 14)

font_wink = pygame.font.Font('assets/Verdana.ttf', 200)

bg = pygame.image.load('assets/background.png').convert_alpha()


score = 0
class Judgement:
    def __init__(self, name, nickname, window, amount = 0,):
        self.name = name
        self.nickname = nickname
        self.amount = amount
        self.window = window

judgements = {"pixel": Judgement('Pixel', 'px', 0),  # good luck
              "brain": Judgement('Brain', 'br', 1),
              "heart": Judgement('Heart', 'hr', 3),
              "skin": Judgement('Skin', 'sk', 5),
              "lungs": Judgement('Lungs', 'ln', 8),
              "liver": Judgement('Liver', 'lv', 11),
              "kidneys": Judgement('Kidney', 'kd', 15),
              "stomach": Judgement('Stomach', 'st', 21),
              "intestine": Judgement('Intestine', 'in', 30)
              }

miss = 0

judgement_text = ''
judgement_pos = [0, 0]
judgement_alpha = 0

class Circle:
    target_radius = 30
    
    def __init__(self, radius = 0,
                 growth = .3,
                 pos = [WIDTH/2, HEIGHT/2],
                 speed = 0):
        self.radius = radius
        self.growth = growth
        self.pos = pos
        self.speed = speed
        
    def point_distance(self, pos):
        return math.sqrt((self.pos[0]-pos[0])**2 + (self.pos[1]-pos[1])**2)

circles = []
highest_timer_circles = 180
timer_circles = 30

class Button:
    def __init__(self, pos, color, dimensions, speed = 5, angle = 0):
        self.pos = pos
        self.color = color
        self.dimensions = dimensions
        self.speed = speed
        self.angle = angle
    
    def move(self):
        self.pos = [self.pos[0] + self.speed * math.cos(math.radians(self.angle)),
                    self.pos[1] + self.speed * math.sin(math.radians(self.angle))]
        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.angle = (-self.angle - 180) % 360
        
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.angle = (270 - self.angle - 270) % 360
            

play_button = Button([random.randint(0,WIDTH), random.randint(0, HEIGHT)],
                     list(random.randint(0,255) for i in range(3)),
                     [random.randint(10,200), random.randint(10,200)],
                     angle=random.randint(30, 150))

class Powerup():
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

powerups = []

amt_1 = 0
amt_2 = 0
amt_3 = 0

place = 'menu'

frames = 0
target_frames = 60*60*24*FPS

wink = font_wink.render(';)', True, (0, 0, 0))
wink_alpha = 0
wink.set_alpha(0)

def formattime(time):
    hour = str(math.floor(time / 3600))
    minute = str(math.floor(time / 60) % 60)
    second = str(time % 60)
    if float(hour) < 10:
        hour = '0' + hour
    if float(minute) < 10:
        minute = '0' + minute
    if float(second) < 10:
        return hour + ':' + minute + ':' + f'0{float(second):.3f}'
    else:
        return hour + ':' + minute + ':' + f'{float(second):.3f}'


def play_music(file: str = '', times = -1):
    if file == '': return  # if there is no file, don't do anything
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(file)
    pygame.mixer.music.queue(file)
    pygame.mixer.music.play(times)  # if 0, don't repeat. if -1, repeat indefinitely


def play_sound(soundfile, volume):
    a = pygame.mixer.Sound(soundfile)
    a.set_volume(volume)
    pygame.mixer.Sound.play(a)


while True:
    events = pygame.event.get()
    mx, my = pygame.mouse.get_pos()
    
    lastplace = place
    
    window.fill((255, 255, 255))
    
    for event in events:
        if event.type == pygame.QUIT and not place == 'game':  # you can't quit during the game ;)
            pygame.quit()
            exit()
    
    window.blit(bg, (0,0))
    
    if place == 'menu':
        title = font_title.render('gugmend daie', True, (0, 0, 0))
        subtitle = font_small.render('the best game since Hotel Mario', True, (0, 0, 0))
        
        window.blit(title, title.get_rect(center=(WIDTH/2,HEIGHT/10)))
        window.blit(subtitle, subtitle.get_rect(center=(WIDTH/2, HEIGHT/10+.75*title.get_height())))
        
        play_text = font_play.render('play', True, (0, 0, 0))
        
        rect = pygame.Rect(play_button.pos, play_button.dimensions)
        pygame.draw.rect(window, play_button.color, rect)
        
        window.blit(play_text, play_text.get_rect(center=rect.center))
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint((mx,my)):
                    place = 'instruction'
        
        play_button.move()
    
    elif place == 'instruction':
        instructions = ['Every so often a circle will spawn somewhere.',
                        'Put your cursor as close to the center of the',
                        'circle as you can.',
                        ' ',
                        ' ',
                        'The game will JUDGE you based on how close you are',
                        'to the center of the circle, and the game lasts',
                        'an ENTIRE FUCKING DAY, hence the name:,,,,',
                        ' ',
                        ' ',
                        'JUDGEMENT DAY',
                        'fml',
                        ' ',
                        'The game progressively gets harder as you go on, so',
                        'click the pink boxes! They will help you on your way.',
                        ' ',
                        'Click your mouse to start the game btich']
        
        for i, instruction in enumerate(instructions):
            n = font_play.render(instruction, True, (0, 0, 0))
            window.blit(n,
                        n.get_rect(center=(WIDTH/2,
                                           .1*HEIGHT + (i * (.8*HEIGHT / len(instructions))))))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_music('assets/bgm.wav')
                place = 'game'
    
    elif place == 'game':
        score_text = font_small.render(f'Score: {score:.2f}', True, (0, 0, 0))
        judgement_surf = font_tiny.render(judgement_text, True, (0, 0, 0))
        judgement_surf.set_alpha(judgement_alpha)
        time_text = font_small.render(f'Time: {formattime((target_frames-frames)/60)}', True, (0, 0, 0))
        window.blit(time_text, (5, score_text.get_height() + 5))
        window.blit(score_text, (5, 5))
        
        if random.randint(0, FPS*30) == 69:
            powerups.append(Powerup([random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20)],
                                    random.randint(1,3)))
        
        removelist = []
        for i, circle in enumerate(circles):
            pygame.draw.circle(window,(0,0,0), circle.pos, circle.radius, width = 2)
            if circle.radius > Circle.target_radius:
                dist = circle.point_distance((mx,my))
                removelist.append(circle)
                
                for i in judgements:
                    if dist <= judgements[i].window:
                        judgements[i].amount += 1
                        judgement_text = judgements[i].name
                        judgement_alpha = 255
                        if judgements[i].name != 'Intestine':
                            play_sound('assets/hit.wav', .2)
                        else:
                            play_sound('assets/barely.wav', .2)
                        break
                else:
                    judgement_text = 'you missed dunce'
                    judgement_alpha = 255
                    play_sound('assets/miss.wav', .2)
                    miss += 1
                
                score += (Circle.target_radius - dist) * (1 + amt_1/20)

            
            circle.radius += circle.growth
        
        for i in removelist:
            circles.remove(i)
        judgement_pos = (mx, my)
        removelist = []
        for i in powerups:
            rect = pygame.Rect(i.pos, (20, 20))
            pygame.draw.rect(window, (255, 0, 255), rect)
            
            for event in events:
                if rect.collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN:
                    if i.type == 1:
                        amt_1 += 1
                    elif i.type == 2:
                        amt_2 += 1
                    else:
                        amt_3 += 1
                    
                    texts = ['Potentially more points',
                             'Circles spawn slower',
                             'Circles grow slower']
                    judgement_text = texts[i.type-1]
                    judgement_alpha = 255
                    
                    play_sound('assets/powerup.wav', .2)
                    
                    removelist.append(i)
        
        
        for i in removelist:
            powerups.remove(i)
        
        window.blit(judgement_surf, judgement_surf.get_rect(bottomright=judgement_pos))
        
        removelist = []
        timer_circles -= 1
        if timer_circles < 0:
            timer_circles = round(highest_timer_circles, 0)
            circles.append(Circle(0, (1/(.1*amt_3+1)) * (0.3 + frames*(1.3/target_frames)),
                                  [random.randint(Circle.target_radius, WIDTH-Circle.target_radius), random.randint(Circle.target_radius, HEIGHT-Circle.target_radius)]))
        highest_timer_circles = 180 - ((1/(.1*amt_2+1)) * (frames*(180/target_frames)))
        window.blit(wink, wink.get_rect(center=(WIDTH/2, HEIGHT/2)))
        for event in events:
            if event.type == pygame.QUIT:
                wink_alpha = 255
        wink.set_alpha(wink_alpha)
        wink_alpha -= 1
        frames += 1
        judgement_alpha -= 1
        if frames >= target_frames:
            if nohighscore:
                highscore = score
                nohighscore = False
                newhighscore = True
                with open('highscore.txt', 'w') as f:
                    f.write(f'{score}')
                
            else:
                if score > highscore:
                    highscore = score
                    with open('highscore.txt', 'w') as f:
                        f.write(f'{score}')
                    newhighscore = True
                else:
                    newhighscore = False
            
            words = ['Finally!',
                 'Why did you get this far?',
                 'Are you mentally in there?',
                 'Did you cheat? Fuck you',
                 'It\'s about time',
                 ':)',
                 'You\'re one of the 0 people here!!']
            
            word = random.choice(words)
            
            place = 'fuck they reached the end'
    
    elif place == 'fuck they reached the end':
        
        title = font_title.render(word, True, (0, 0, 0))
        window.blit(title, title.get_rect(midtop=(WIDTH/2, 0)))
        if newhighscore:
            highscore_text = f'(NEW BEST!)'
        else:
            highscore_text = f'(Best: {highscore:.2f})'
        
        left = []
        right = []
        for i in judgements:
            left.append(font_play.render(f'{judgements[i].name} (within {judgements[i].window} px)', True, (0, 0, 0)))
            right.append(font_play.render(f'{judgements[i].amount:,}', True, (0, 0, 0)))
        
        # fuck this shit i'm taking the easy way out
        left.append(font_play.render('Miss', True, (0, 0, 0)))
        right.append(font_play.render(f'{miss:,}', True, (0, 0, 0)))
        left.append(font_play.render(' ', True, (0, 0, 0)))
        right.append(font_play.render(' ', True, (0, 0, 0)))
        left.append(font_play.render('Score', True, (0, 0, 0)))
        left.append(font_play.render(' ', True, (255, 255, 255)))  # so it doesnt fucking kill me
        right.append(font_play.render(f'{score:.2f}', True, (0, 0, 0)))
        right.append(font_play.render(f'{highscore_text}', True, (0, 0, 0)))
        
        for i, val in enumerate(left):
            window.blit(val, (5, .15*HEIGHT + i*val.get_height()))
            window.blit(right[i], right[i].get_rect(topright=(WIDTH - 5, .15*HEIGHT + i*right[i].get_height())))
        
        
    
    pygame.display.update()
    clock.tick(FPS)
    