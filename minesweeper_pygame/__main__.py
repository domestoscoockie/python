import pygame, random, time

def making_bomb_fields():
    list_of_bombs = []
    another_bomb = 0
    while len(list_of_bombs)<=8:
        another_bomb = random.randint(0,55) # tu powinno byc (0,64)
        if another_bomb not in list_of_bombs:
            list_of_bombs.append(another_bomb) 
    list_of_bombs.sort()
    return list_of_bombs    

def making_number(i_0): 
    if i_0 == 0 or i_0 % 8==0:
        list_of_numbers_1 = [i_0-8,i_0-7,i_0+1,i_0+8,i_0+9]
    elif (i_0+1) % 8 == 0:
        list_of_numbers_1 = [i_0-9,i_0-8,i_0-1,i_0+7,i_0+8]
    else:
        list_of_numbers_1 = [i_0-9,i_0-8,i_0-7,i_0-1,i_0+1,i_0+7,i_0+8,i_0+9]
        
    list_of_numbers_new = []   
    for i in list_of_numbers_1:
        if i <= 63 and i >= 0 :
                list_of_numbers_new.append(i)

    return list_of_numbers_new

def giving_place_number():
    dict_of_occurrence = {}
    for i in range(64):
        summary = 0
        path = "data/white.png"
        if i not in list_of_bombs:
            for el in list_of_occurrence:
                if i in el:
                    summary += 1
        if summary == 1:
            path = "data/1.png"
        elif summary == 2:
            path = "data/2.png"
        elif summary == 3:
            path = "data/3.png"
        elif summary == 4:
            path = "data/4.png"
        elif summary == 5:
            path = "data/5.png"
        elif summary == 6:
            path = "data/6.png"
        if i in list_of_bombs:
            path = "data/bomb.gif" 
        dict_of_occurrence.update({i : path})     
    return dict_of_occurrence

def placing_50x50_image(path,x,y):
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image,(49,49))
    screen.blit(image,(x,y))
def placing_image(path,x,y,scale):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image,(scale))
    screen.blit(image,(x,y))
       
def positions_and_rects():                     
    x = 0
    y = 150
    list_of_rect = []
    list_of_positions = []
    position_0 = (0,0)
    i_1 = 0
    for i in range(8):
        for i_0 in range(8):          
            list_of_rect.append(pygame.Rect(x,y,49,49))
            list_of_positions.append((([x,y],[x+50,y-50]),i_1))
            x += 50
            i_1 += 1
        y += 50
        x = 0
    return list_of_rect, list_of_positions

def process_whites(list_of_whites, every_white, dict_of_occurrence, depth=0, max_depth=6):
    if depth >= max_depth:
        return
    new_whites = set()
    for white in list_of_whites:
        processed = making_number(white)
        filtered = list(filter(lambda x: dict_of_occurrence[x] == 'data/white.png', processed))
        new_whites.update(filtered)
    every_white.update(new_whites)
    if new_whites:
        process_whites(new_whites, every_white, dict_of_occurrence, depth + 1, max_depth)
        
def clicking_button(path,x,y,scale):
    clicked = False
    action = False
    position = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x,y,scale[0],scale[1])
    if button_rect.collidepoint(position):
        if pygame.mouse.get_pressed()[0] == True and clicked == False:
            action = True
            clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            clicked = False
    print(action)
    return action
                
def left_click():    
    if pygame.mouse.get_pressed()[0] == True:
       # Get the mouse position
        mouse_position = pygame.mouse.get_pos() 
        clicked_in_right_place = False
        print(mouse_position)
        for position in list_of_positions:
            if position[0][0][0] < mouse_position[0] < position[0][1][0] and  position[0][0][1] < mouse_position[1] > position[0][1][1]:
                clickied_button = position
                clicked_in_right_place = True
         
        if clicked_in_right_place == True:
            if clickied_button not in list_of_exposed:
                path, x, y = dict_of_occurrence.get(clickied_button[1]),clickied_button[0][0][0],clickied_button[0][0][1]
                placing_50x50_image(path,x,y)
                list_of_exposed.append(clickied_button)  
                
                if dict_of_occurrence.get(clickied_button[1]) == 'data/white.png':
                    white = clickied_button[1]
                    every_white = set()
                    list_of_whites = making_number(white)
                    list_of_whites = (list(filter(lambda x: dict_of_occurrence[x] == 'data/white.png',list_of_whites)))
                    every_white.update(list_of_whites)
                    process_whites(list_of_whites, every_white, dict_of_occurrence, depth=0, max_depth=20) #recurrency
                    for white in every_white:
                        path, x, y = dict_of_occurrence.get(white),list_of_positions[white][0][0][0],list_of_positions[white][0][0][1]
                        placing_50x50_image(path,x,y)
                        list_of_exposed.append(white)
                        
                if dict_of_occurrence.get(clickied_button[1]) == 'data/bomb.gif':   
                    path, x, y = dict_of_occurrence.get(clickied_button[1]),clickied_button[0][0][0],clickied_button[0][0][1]
                    placing_50x50_image(path,x,y)
                    for position in list_of_positions:
                        if dict_of_occurrence.get(position[1]) == 'data/bomb.gif':   
                            path, x, y = dict_of_occurrence.get(position[1]),position[0][0][0],position[0][0][1]
                            placing_50x50_image(path,x,y)                             
                    placing_image('data/game_over.png',73,170,(250,250))
                    placing_image('data/restart.png',0,2,(400,146))
                    game_over = -1
                    return game_over

                
def right_click(mark):
    if pygame.mouse.get_pressed()[2]:
        clicked_in_right_place = False
        mouse_position = pygame.mouse.get_pos()
        print(mouse_position)
        for position in list_of_positions:
            if position[0][0][0] < mouse_position[0] < position[0][1][0] and  position[0][0][1] < mouse_position[1] > position[0][1][1]:
                clickied_button = position
                clicked_in_right_place = True
        
        if clicked_in_right_place == True:
            if clickied_button not in list_of_exposed:
                if mark == '!':
                    placing_50x50_image('data/question_mark.jpg',clickied_button[0][0][0],clickied_button[0][0][1])
                        
                    mark = '?'
                elif mark == '?':
                    placing_50x50_image('data/grey.png',clickied_button[0][0][0],clickied_button[0][0][1])
                        
                    mark = ''
                else:
                    placing_50x50_image('data/exclamation_mark.jpg',clickied_button[0][0][0],clickied_button[0][0][1])
                    mark = '!' 
    return mark              

screen = pygame.display.set_mode((400,550))
clock = pygame.time.Clock()
running = True
screen.fill((200,200,200))
restarting = False
delta_time = 0
game_over = 0
mark = ''
list_of_bombs = making_bomb_fields()              
list_of_occurrence = list(map(making_number,list_of_bombs))
dict_of_occurrence = giving_place_number()            
list_of_rect = positions_and_rects()[0]
list_of_positions = positions_and_rects()[1]
list_of_exposed = []
for rect in list_of_rect:
    pygame.draw.rect(screen,(220,220,220),rect)  
list_of_marks = ['data/question_mark.jpg','data/exclamation_mark.jpg']

while running:  
    if game_over == -1:
        
        if clicking_button('data/restart.png',0,10,(400,130)) == True:
            screen.fill((200,200,200))
            game_over = 0
            mark = ''  
            list_of_exposed = []              
            list_of_bombs = making_bomb_fields()              
            list_of_occurrence = list(map(making_number,list_of_bombs))
            dict_of_occurrence = giving_place_number()            
            list_of_rect = positions_and_rects()[0]
            list_of_positions = positions_and_rects()[1]
            for rect in list_of_rect:
                pygame.draw.rect(screen,(220,220,220),rect)
                                
    for event in pygame.event.get():
        
        if left_click() == -1:
            for position in list_of_positions:
                list_of_exposed.append(position)
            game_over = -1
        mark = right_click(mark)
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000

pygame.quit()

