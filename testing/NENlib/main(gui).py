from NENlib import *
from library import *

W, H = 800, 800

root = Root("localhost", "root", "Fearless2023") 
try:
    print(root.nenlibdb.users.get_field_names())
except:
    print("err")

def update(dt, window):
    for ix in range(8):
        for iy in range(8):
            pygame.draw.rect(window, (255,255,255), [ix*100, iy*100, 100, 100])
            pygame.draw.rect(window, (0,0,0), [ix*100 + 1, iy*100 + 1, 98, 98])
    index = 0
    for fNames in root.nenlibdb.users.get_field_names():
        drawText(window, fNames, (255,255,255), [0 + index*100,0], 30)
        index += 1
    y = 1
    for entry in root.nenlibdb.users.get_entries():
        x = 0
        for ent in entry:
            drawText(window, str(ent), (255,255,255), [x*100,y*100], 30)
            x += 1
        y += 1
            


maxFPS = 10000
clock = pygame.time.Clock()

def main():
    window = init(W, H, "MySQL GUI test")

    pygame.key.start_text_input()

    running = True
    while running:
        dt = clock.tick(maxFPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.TEXTINPUT:
                pass
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pass

                if event.key == pygame.K_ESCAPE:
                    running = False

        window.fill((0, 0, 0))
        update(dt, window)
        pygame.display.flip()
        

    pygame.key.stop_text_input()
    print("Done")

main()