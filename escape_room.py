import pygame
import sys


WIDTH = 1400
HEIGHT = 800
FPS = 60
TITLE = " Escape Room"
FONT_NAME = "NanumGothic.ttf"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREY = (50, 50, 50)

class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        super().__init__()
        self.game = game
        self.name = name
        self.image = pygame.Surface((w, h))
        self.image.set_alpha(0)  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        pass

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = FONT_NAME
        self.load_assets()
        self.state = 'start_screen'
        self.current_room = 1
        
        self.room_inventories = {1: [], 2: [], 3: [], 4:[], 5:[]} 
        
        self.current_dialogue = ""
        self.password_input = ""
        self.password_target = ""
        self.next_state = None
        self.dialogue_queue = []

    def load_assets(self):
        try:
            self.room1_bg = pygame.image.load("room1.png").convert()
            self.room1_bg = pygame.transform.scale(self.room1_bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.room1_bg = pygame.Surface((WIDTH, HEIGHT))
            self.room1_bg.fill(BLACK)

        try:
            self.room2_bg = pygame.image.load("room2.png").convert()
            self.room2_bg = pygame.transform.scale(self.room2_bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.room2_bg = pygame.Surface((WIDTH, HEIGHT))
            self.room2_bg.fill(DARK_GREY)

        try:
            self.room3_bg = pygame.image.load("room3.png").convert()
            self.room3_bg = pygame.transform.scale(self.room3_bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.room3_bg = pygame.Surface((WIDTH, HEIGHT))
            self.room3_bg.fill(GREEN)

        try:
            self.room4_bg = pygame.image.load("room4.png").convert()
            self.room4_bg = pygame.transform.scale(self.room4_bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.room4_bg = pygame.Surface((WIDTH, HEIGHT))
            self.room4_bg.fill(BLUE)

        try:
            self.room5_bg = pygame.image.load("room5.png").convert()
            self.room5_bg = pygame.transform.scale(self.room5_bg, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.room5_bg = pygame.Surface((WIDTH, HEIGHT))
            self.room5_bg.fill(YELLOW)

    def setup_room(self, room_number):
        self.all_sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.current_room = room_number
        
        if not self.room_inventories[room_number]:
            self.room_inventories[room_number] = []
        
        self.state = 'explore'
        if room_number == 1:
            desk = InteractiveObject(self, 210, 540, 560, 220, "desk")
            painting = InteractiveObject(self, 400, 240, 350, 240, "painting")
            locked_door = InteractiveObject(self, 1050, 290, 250, 470, "room1_door")
            clock = InteractiveObject(self, 50, 240, 130, 540, "clock")
            self.all_sprites.add(desk, painting, locked_door, clock)
            self.objects.add(desk, painting, locked_door, clock)
            self.show_dialogue("클릭하여 상호작용하세요. 같은 물건은 다시 클릭하여 자세히 볼 수 있습니다")

        elif room_number == 2:
            chair = InteractiveObject(self, 550, 560, 250, 220, "chair")
            lock = InteractiveObject(self, 160, 420, 130, 130, "lock")
            large_painting = InteractiveObject(self, 370, 80, 600, 300, "large_painting")
            desk_pictures = InteractiveObject(self, 650, 470, 400, 200, "desk_pictures")
            self.all_sprites.add(chair, lock, large_painting, desk_pictures)
            self.objects.add(chair, lock, large_painting, desk_pictures)
            
        elif room_number == 3:
            grandfather_clock = InteractiveObject(self, 65, 140, 190, 680, "grandfather_clock")
            globe = InteractiveObject(self, 270, 480, 240, 300, "globe")
            desk_books = InteractiveObject(self, 570, 600, 400, 250, "desk_books")
            keypad = InteractiveObject(self, 1185, 355, 100, 100, "keypad") 

            self.all_sprites.add(grandfather_clock, globe, desk_books, keypad)
            self.objects.add(grandfather_clock, globe, desk_books, keypad)
            
        elif room_number == 4:
            lock = InteractiveObject(self,780, 500, 350, 350, "lock")
            desk = InteractiveObject(self, 280, 440, 880, 360, "desk")
            knight_armor_left = InteractiveObject(self, 170, 250, 240, 480, "knight_armor_left")
            knight_armor_right = InteractiveObject(self, 680, 250, 240, 480, "knight_armor_right")

            self.all_sprites.add(lock, desk, knight_armor_left, knight_armor_right)
            self.objects.add(lock, desk, knight_armor_left, knight_armor_right)
    


        elif room_number == 5:
            self.show_dialogue("축하합니다! 탈출하셨습니다!")
            self.next_state = 'game_clear'
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
       
            if self.state == 'explore':
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.handle_click(event.pos)
       
            elif self.state == 'dialogue':
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if self.dialogue_queue:
                        self.current_dialogue = self.dialogue_queue.pop(0)
                    else:
                        if self.next_state == 'password':
                            self.prompt_password("4자리 비밀번호를 입력하세요", "room1_door_pw")
                            self.next_state = None
                        elif self.next_state == 'password_room2':
                            self.prompt_password("네자리 비밀번호를 입력하세요", "room2_lock_pw")
                            self.next_state = None
                        
                        elif self.next_state == 'password_clockroom3':
                            self.prompt_password("바꿀 시간을 입력하세요", "room3_clock_pw")
                            self.next_state = None

                        elif self.next_state == 'password_room3':
                            self.prompt_password("네 자리 비밀번호를 입력하세요", "room3_keypad_pw")
                            self.next_state = None

                        elif self.next_state == 'password_room4':
                            self.prompt_password("네자리 비밀번호를 입력하세요", "room4_lock_pw")
                            self.next_state = None

                        elif self.next_state == 2:
                            self.playing = False
                            self.setup_room(2)
                            self.next_state = None
           
                        elif self.next_state == 3:
                            self.playing = False
                            self.setup_room(3)
                            self.next_state = None
           
                        elif self.next_state == 4:
                            self.playing = False
                            self.setup_room(4)
                            self.next_state = None
           
                        elif self.next_state == 5:
                            self.playing = False
                            self.setup_room(5)
                            self.next_state = None

                        elif self.next_state == 'game_clear':
                            self.state = 'game_clear'
                            self.playing = False
                        else:
                            self.state = 'explore'
                            self.current_dialogue = ""
            
            
            elif self.state == 'password':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.check_password()
                    elif event.key == pygame.K_BACKSPACE:
                        self.password_input = self.password_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        pygame.key.stop_text_input() 
                        self.state = 'explore'
                        self.password_input = ""
                
                elif event.type == pygame.TEXTINPUT:
                    self.password_input += event.text

    def update(self):
        self.all_sprites.update()

    def draw(self):
        if self.current_room == 1:
            self.screen.blit(self.room1_bg, (0, 0))
        elif self.current_room == 2:
            self.screen.blit(self.room2_bg, (0, 0))
        elif self.current_room == 3:
            self.screen.blit(self.room3_bg, (0, 0))
        elif self.current_room == 4:
            self.screen.blit(self.room4_bg, (0, 0))
        elif self.current_room == 5:
            self.screen.blit(self.room5_bg, (0, 0))
        
        if self.state == 'dialogue':
            self.draw_dialogue_box()
        elif self.state == 'password':
            self.draw_password_box()
            
        self.draw_inventory() 
        
        pygame.display.flip()

    def handle_click(self, pos):
        clicked_object = None
        for obj in self.objects:
            if obj.rect.collidepoint(pos):
                clicked_object = obj
                break
        if clicked_object:
            self.run_story(clicked_object.name)



###스토리핵심
    def run_story(self, object_name):
        
        if self.current_room == 1:
            if object_name == "desk":
                if "열쇠" not in self.room_inventories[self.current_room]:
                    self.show_dialogue("지저분한 책상이다. 서랍안에 열쇠가 있다.")
                    self.room_inventories[self.current_room].append("열쇠")
                else:
                    self.show_dialogue("이미 열쇠를 챙긴 빈 서랍이다.")
           
            elif object_name == "clock":
                if "시계 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["오래된 괘종시계다. 시계는 멈춰있다... 자세히 봐볼까?","자세히 보니 시침은 [1], 분침은 [8]을 가리킨다."])
                    self.room_inventories[self.current_room].append("시계 단서")
                else:
                    self.show_dialogue("자세히 보니 시침은 [1], 분침은 [8]을 가리킨다.")
           
            elif object_name == "painting":
                if "그림 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["오래된 범선 그림이다. 뭔가 의미가 있지 않을까?", "그림을 보니 4개의 돛대가 있는 범선이 2척 있다."])
                    self.room_inventories[self.current_room].append("그림 단서")
                else:
                    self.show_dialogue("그림을 보니 4개의 돛대가 있는 범선이 2척 있다.")
           
            elif object_name == "room1_door":
                if "열쇠" in self.room_inventories[self.current_room]:
                    self.show_dialogue(["열쇠를 사용했지만 2중잠금인거 같다.","옆에 키패드가 있다."])
                    self.next_state = 'password'
                else:
                    self.show_dialogue("문이 잠겨있다. 열쇠가 필요할 것 같다.")
                    
        elif self.current_room == 2:
            if object_name == "chair":
                if "의자 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["낡은 의자다. 앉아볼까?", "앉으려고 보니 쪽지가 있다","[첫번째 방의 비밀번호] &@& [2225]= 1511"])
                    self.room_inventories[self.current_room].append("의자 단서")
                else:
                    self.show_dialogue("[첫번째 방의 비밀번호] &@& [2225]= 1511")

            elif object_name == "large_painting":
                if "그림 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["큰 그림이다"," 뒤에 뭔가 적혀있는 것 같다", "쪽지에는 [2009] &@& [1112] = 비밀번호 라고 적혀있다"])
                    self.room_inventories[self.current_room].append("그림 단서")
                else:
                    self.show_dialogue("쪽지에는 [2009] &@& [1112] = 비밀번호 라고 적혀있다")
           
            elif object_name == "desk_pictures":
                if "사진 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["사진속을 자세히보니 작은 메모가 있다","&@& 기호의 의미:  [A] &@& [B]= A의 숫자들의 덧셈 B의 숫자들의 덧셈   이라고 적혀있다"])
                    self.room_inventories[self.current_room].append("사진 단서")
                else:
                    self.show_dialogue("&@& 기호의 의미:  [A] &@& [B]= 앞의 두자리=A의 숫자들의 덧셈 뒤의 두자리=B의 숫자들의 덧셈   이라고 적혀있다")
           
            elif object_name == "lock":
                self.show_dialogue(["자물쇠가 잠겨있다.", "네자리 비밀번호가 필요할 것 같다."])
                self.next_state = 'password_room2'

        elif self.current_room == 3:
            if object_name == "grandfather_clock":
                if "괘종시계 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["오래된 괘종시계다. 시계는 멈춰있다... 자세히 봐볼까?","시계의 시간을 바꿔볼까?"])
                    self.room_inventories[self.current_room].append("괘종시계 단서")
                    self.next_state= 'password_clockroom3'
                else:
                    
                    self.show_dialogue("시계의 시간을 바꿔볼까?")
                    self.next_state = 'password_clockroom3'

            elif object_name == "globe":
                if "지구본 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["큰 지구본이다. 자세히 보니...","현재의 시간이라고 적혀있다.","현재 시간을 써둔 종이가 어딘가 있지 않을까?"])
                    self.room_inventories[self.current_room].append("지구본 단서")
                else:
                    self.show_dialogue(["현재 시간을 써둔 종이가 어딘가 있지 않을까?"])

            elif object_name == "desk_books":
                if "책 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["책상 위에 여러권의 책이 있다.","책에 종이가 끼워져 있다", "현재 시간 = 13시 27분"])
                    self.room_inventories[self.current_room].append("책 단서")
                else:
                    self.show_dialogue("현재 시간 = 13시 27분")

            elif object_name == "keypad":
                self.show_dialogue(["키패드가 있다.", "비밀번호가 필요할 것 같다."]) 
                self.next_state = 'password_room3'

        elif self.current_room == 4:
            if object_name == "knight_armor_left":
                if "왼쪽 갑옷 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["기사 갑옷이다"," 갑옷안에 {벽의 문장의 개수 + ???}라는 쪽지가 있다"])
                    self.room_inventories[self.current_room].append("왼쪽 갑옷 단서")
                else:
                    self.show_dialogue("갑옷안에 {벽의 문장의 개수 + ???}라는 쪽지가 있다")

            elif object_name == "knight_armor_right":
                if "오른쪽 갑옷 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["기사 갑옷이다","갑옷 안에 {??? + 촛불의 개수}라는 쪽지가 있다"])
                    self.room_inventories[self.current_room].append("오른쪽 갑옷 단서")
                else:
                    self.show_dialogue("갑옷 안에 {??? + 촛불의 개수}라는 쪽지가 있다")

            elif object_name == "desk":
                if "책상 단서" not in self.room_inventories[self.current_room]:
                    self.show_dialogue(["책상에 여러권의 책이 있다","책들 사이에 종이가 끼워져있다","비밀번호= 갑옷단서들을 통해 얻은 숫자*100"])
                    self.room_inventories[self.current_room].append("책상 단서")
                else:
                    self.show_dialogue("비밀번호= 갑옷단서들을 통해 얻은 숫자*100")

            elif object_name == "lock":
                self.show_dialogue(["자물쇠가 잠겨있다.", "비밀번호가 필요할 것 같다."])
                self.next_state = 'password_room4'
        



    def show_dialogue(self, text_or_list):
        if isinstance(text_or_list, str):
            self.dialogue_queue = [text_or_list]
        elif isinstance(text_or_list, list):
            self.dialogue_queue = text_or_list.copy()
        self.state = 'dialogue'
        if self.dialogue_queue:
            self.current_dialogue = self.dialogue_queue.pop(0)
        else:
            self.state = 'explore'

    def prompt_password(self, prompt_text, target_name):
        self.current_dialogue = prompt_text
        self.password_target = target_name
        self.password_input = ""
        self.state = 'password'
        pygame.key.start_text_input() 

    
    def check_password(self):
        pygame.key.stop_text_input() 
        
        if self.password_target == "room1_door_pw":
            if self.password_input == "1842":
                self.show_dialogue("철컥! 문이 열렸다.")
                self.next_state = 2
            else:
                self.show_dialogue("비밀번호가 틀렸다. (입력: " + self.password_input + ")")
                self.state = 'explore'
        elif self.password_target == "room2_lock_pw":
            if self.password_input == "1105":
                self.show_dialogue("철컥! 자물쇠가 열렸다.")
                self.next_state = 3
            else:
                self.show_dialogue("비밀번호가 틀렸다. (입력: " + self.password_input + ")")
                self.state = 'explore'

        elif self.password_target == "room3_clock_pw":
            if self.password_input == "1327":
                self.show_dialogue("비밀 번호 = 1112")
            else:
                self.show_dialogue("비밀번호가 틀렸다. (입력: " + self.password_input + ")")
                self.state = 'explore'


        elif self.password_target == "room3_keypad_pw":
            if self.password_input == "1112":

                self.show_dialogue("키패드가 열렸다. 방을 탈출했다!")
                self.next_state = 4 
            else:
                self.show_dialogue("비밀번호가 틀렸다. (입력: " + self.password_input + ")")
                self.state = 'explore'         

        elif self.password_target == "room4_lock_pw":
            if self.password_input == "1800":
                self.show_dialogue("철컥! 자물쇠가 열렸다.")
                self.next_state = 5
            else:
                self.show_dialogue("비밀번호가 틀렸다. (입력: " + self.password_input + ")")
                self.state = 'explore'


        self.password_input = ""

    def draw_dialogue_box(self):
        box_height = 150
        box_rect = pygame.Rect(0, HEIGHT - box_height - 50, WIDTH, box_height)
        pygame.draw.rect(self.screen, BLACK, box_rect)
        pygame.draw.rect(self.screen, WHITE, box_rect, 3)
        self.draw_text(self.current_dialogue, 24, WHITE, WIDTH / 2, HEIGHT - box_height - 50 + 75)
        self.draw_text("(다음: 아무 키나 클릭)", 18, YELLOW, WIDTH / 2, HEIGHT - 50 - 25) 

    def draw_password_box(self):
        box_w, box_h = 400, 200
        box_x = (WIDTH - box_w) / 2
        box_y = (HEIGHT - box_h) / 2
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, BLACK, box_rect)
        pygame.draw.rect(self.screen, WHITE, box_rect, 3)
        self.draw_text(self.current_dialogue, 22, WHITE, WIDTH / 2, box_y + 40)
        input_rect = pygame.Rect(box_x + 50, box_y + 100, box_w - 100, 40)
        pygame.draw.rect(self.screen, DARK_GREY, input_rect)
        self.draw_text(self.password_input, 30, YELLOW, WIDTH / 2, box_y + 120) 

    def draw_inventory(self):
        inv_height = 50
        inv_rect = pygame.Rect(0, HEIGHT - inv_height, WIDTH, inv_height)
        pygame.draw.rect(self.screen, DARK_GREY, inv_rect)
        self.draw_text("Inventory:", 20, WHITE, 70, HEIGHT - inv_height / 2 - 10)
        
        current_inventory_list = self.room_inventories[self.current_room]
        
        for i, item_name in enumerate(current_inventory_list):
            item_text = f"[{item_name}]"
            
            x_position = 160 + i * 200
           
            self.draw_text(item_text, 18, YELLOW, x_position + 100, HEIGHT - inv_height / 2 - 9)


    def draw_text(self, text, size, color, x, y):
        
        try:
            font = pygame.font.Font(self.font_name, size)
        except FileNotFoundError:
            font = pygame.font.Font(None, size) 
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Click to Start", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    waiting = False


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    if g.running:
        g.setup_room(1)
    pygame.quit()
    sys.exit()