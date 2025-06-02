import curses
import curses.textpad
import requests
from catraca.config import API_URL, BASE_DIR
import sys
import os
import json

class Option():
    def __init__(self, func, name, active = False):
        self.function = func
        self.name = name
        self.active = active

def enter_unkown(stdscr,restaurant):
    requests.post(API_URL+f'restaurante/{restaurant["id"]}/entrar')
    restaurant = requests.get(API_URL+f'restaurante/{restaurant["id"]}').json()
    return restaurant
def leave(stdscr,restaurant):
    requests.post(API_URL+f'restaurante/{restaurant["id"]}/sair')
    restaurant = requests.get(API_URL+f'restaurante/{restaurant["id"]}').json()
    return restaurant

def payment(user_id):
    try:
        response = requests.post(API_URL+f'usuario/{user_id}/passar')
        response.raise_for_status()  
        user = response.json()    
        return user
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            erro = response.json()
            if 'detail' in erro and erro['detail'] == 'Dinheiro insuficiente':
                return None
            
    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição: {err}")

def validate_student(studentId):
    students = requests.get(API_URL+f'usuario/').json()
    for student in students:
        if student["studentId"] == studentId:
            return student["id"]
    return None

def enter_student(stdscr, restaurant):
        buffer = ""
        cursor_x = 1
        while True:
            stdscr.erase()
            stdscr.border()
            stdscr.refresh()
            height, width = stdscr.getmaxyx()
            
            win_w = int(0.4*width)
            win_h = int (0.3*height)
            win_x = (width - win_w) // 2 
            win_y = (height - win_h) // 2
            win = curses.newwin(win_h, win_w, win_y, win_x)
            msg = "Digite sua matrícula:"
            try:
                win.addstr(3, 3, msg, curses.A_BOLD)
            except curses.error:
                pass
            win.border()
            win.refresh()
            
            subWinWidth = win_w - 6
            subWinHeight = 1
            subWinY = 6
            subWinX = 3
            #subWin = win.derwin(subWinHeight, subWinWidth, subWinY, subWinX)
            try:
                subWin2 = win.derwin(3, subWinWidth + 2, subWinY - 1, subWinX-1)
                subWin2.addstr(1,1,buffer)
                subWin2.move(1, cursor_x)
                subWin2.border()
                subWin2.refresh()
            except:
                pass
                       
            txt = "Pressione 'enter' para confirmar"
            buttonHeight = 3
            buttonWidth = (len(txt) + 8)
            buttonX = (win_w -buttonWidth) // 2
            buttonY = subWinY + 3
            if (win_w <= buttonWidth):
                txt = "Confirmar"
                buttonWidth = (len(txt) + 2)
                buttonX = (win_w -buttonWidth) // 2

            try:
                buttonWin = win.derwin(buttonHeight, buttonWidth, buttonY, buttonX)
                buttonWin.bkgd(' ', curses.color_pair(1) | curses.A_REVERSE)
                buttonWin.addstr(1, (buttonWidth-len(txt))//2, txt)
                buttonWin.border()
                buttonWin.refresh()
            except curses.error:
                pass
            



            key = win.getch()

            if key == curses.KEY_RESIZE:
                continue
            elif key in [10, 13]:  # Enter
                break
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if len(buffer) > 0:
                    buffer = buffer[:-1]
                    cursor_x = max(cursor_x - 1, 1)
            elif 32 <= key <= 126:  # Caracteres imprimíveis
                if len(buffer) < (subWinWidth - 2):
                    buffer += chr(key)
                    cursor_x += 1
            curses.napms(100)
        
        if validate_student(buffer) is None:
            txt = "Estudante não encontrado!"
            student = None
        else:
            student = payment(validate_student(buffer))
            if student is None:
                txt ="Dinheiro insuficiente!"
            else:
                txt = "Debitado com sucesso!"
        while True:
            stdscr.erase()
            stdscr.border()
            stdscr.refresh()
            height, width = stdscr.getmaxyx()
            
            win_w = int(0.4*width)
            win_h = int (0.3*height)
            win_x = (width - win_w) // 2 
            win_y = (height - win_h) // 2
            win = curses.newwin(win_h, win_w, win_y, win_x)
            try:
                win.addstr(3, 3, txt, curses.A_BOLD)
            except curses.error:
                pass
            win.border()
            win.refresh()
            msg = "Pressione 'enter' para retornar"
            buttonHeight = 3
            buttonWidth = (len(msg) + 8)
            buttonX = (win_w -buttonWidth) // 2
            buttonY = subWinY + 3
            if (win_w <= buttonWidth):
                msg = "Retornar"
                buttonWidth = (len(msg) + 2)
                buttonX = (win_w -buttonWidth) // 2

            try:
                buttonWin = win.derwin(buttonHeight, buttonWidth, buttonY, buttonX)
                buttonWin.bkgd(' ', curses.color_pair(1) | curses.A_REVERSE)
                buttonWin.addstr(1, (buttonWidth-len(msg))//2, msg)
                buttonWin.border()
                buttonWin.refresh()
            except curses.error:
                pass
            



            key = win.getch()

            if key == curses.KEY_RESIZE:
                continue
            elif key in [10, 13]:
                if student is not None:
                    enter_unkown(stdscr,restaurant)
                break
            curses.napms(100)


        


def restaurant_selection(stdscr):
    activeOption = 0
    selectedRestaurant = {}
    try:
        restaurants = requests.get(API_URL+"restaurante/").json()
    except requests.ConnectionError as error:
        restaurants = []
    while True:
        height, width = stdscr.getmaxyx()
        msg = "Pressione 'q' para sair"
        y = height -3
        x = max((width - len(msg)) // 2, 1)
        stdscr.erase()
        stdscr.addstr(y,x,msg)
        stdscr.border()
        stdscr.refresh()
        msg = "Selecione o restaurante da catraca:"
        borderY = int(0.3*height)
        borderX = int(0.2*width)
        winSizeY = height -(2*borderY)
        winSizeX = width - (2*borderX)

        msg = "ESCOLHA O RESTAURANTE DA CATRACA"
        try:
            win = curses.newwin(winSizeY, winSizeX, borderY , borderX)
            win.erase()
            #win.border()
            if (len(msg) > winSizeX):
                raise curses.error
            y = 0
            x = max((winSizeX - len(msg)) // 2, 1)
            win.addstr(y, x, msg, curses.A_BOLD)
            win.refresh()
            optionSizeY = 5
            optionSizeX = winSizeX
            spacing = int(winSizeY*0.15)
            ##currentPosY = borderY + (winSizeY // 2) - (optionSizeY * len(restaurants)) - (spacing * (len(restaurants) -1))
            currentPosY = borderY + ((winSizeY - (optionSizeY * len(restaurants) +  (spacing * (len(restaurants) -1)))) // 2)
            currentOptionX = borderX
            if (winSizeY < 2+ (optionSizeY * len(restaurants) +  (spacing * (len(restaurants) -1)))):
                raise curses.error
            for restaurant in restaurants:
                optionWin = curses.newwin(optionSizeY, optionSizeX, currentPosY, currentOptionX)
                if restaurant["id"] == activeOption:
                    optionWin.bkgd(' ', curses.color_pair(1) | curses.A_REVERSE)
                optionWin.erase()
                optionWin.border()
                restaurantText = restaurant["name"]
                textX = optionSizeX //2 - (len(restaurantText) // 2)
                textY = optionSizeY // 2
                optionWin.addstr(textY, textX, restaurantText)
                optionWin.refresh()
                currentPosY+=(spacing+optionSizeY)
            
        
        except curses.error:
            stdscr.erase()
            msg = "Janela muito pequena!"
            y = height // 2
            x = max((width - len(msg)) // 2, 1)
            stdscr.addstr(y,x,msg)
            stdscr.refresh()


        try:
            key = stdscr.getch()
            if key == ord('q'):
                sys.exit()
            elif key == curses.KEY_UP:
                if (activeOption == 0):
                    activeOption = len(restaurants) - 1
                else:
                    activeOption -= 1
            elif  key == curses.KEY_DOWN:
                if (activeOption == len(restaurants) - 1):
                    activeOption =  0
                else:
                    activeOption += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                selectedRestaurant = restaurants[activeOption]
                break

        except curses.error:
            pass
        curses.napms(100)
    restaurant_turnstile_dashboard(stdscr, selectedRestaurant)

def restaurant_turnstile_dashboard(stdscr, restaurant):
    activeOption = 0
    count = 0
    while True:
        count += 1
        if (count == 5):
            count = 0
            restaurant = requests.get(API_URL+f'restaurante/{restaurant["id"]}').json()
        height, width = stdscr.getmaxyx()
        msg = "Pressione 'q' para sair, 'esc' para retornar à seleção de restaurante"
        y = height -3
        x = max((width - len(msg)) // 2, 1)
        stdscr.erase()
        if (width > len(msg)): stdscr.addstr(y,x,msg)
        try:
            y, lineSize, logoNumOfLines= draw_logo(stdscr, height, width)
            if logoNumOfLines == 0: continue
        except curses.error:
            pass
        lineSize = (lineSize-len(f'{restaurant["name"]} | UFMG')) //2
        line = ""
        for l in range(lineSize):
            line+="─"
        msg = f'{line} {restaurant["name"]} | UFMG {line}'
        x = max((width - len(msg)) // 2, 1)
        stdscr.addstr(y,x, msg)
        stdscr.border()
        stdscr.refresh()
        logoNumOfLines +=3
        lines = int(height-logoNumOfLines-5)
        cols = width - 6
        y = (height - logoNumOfLines - lines) // 2 + logoNumOfLines
        x = (width - cols) // 2
        try:
            win = stdscr.subwin(lines,cols,y,x)
        except curses.error:
            continue
        win.border()
        try:
            win.addstr(1,2,f'Lotação Atual: {restaurant["occupancy"]} pessoas', curses.A_BOLD)
        except curses.error:
            pass
        option1 = Option(enter_student, "Entrar no restaurante com cartão")
        option2 = Option(enter_unkown, "Entrar no restaurante com funcionário abrindo")
        option3 = Option(leave, "Sair do restaurante")
        options = [option1, option2, option3]
        options[activeOption].active = True
        if lines >= 20:
            size = 5
        else:
            size = 3
        
        if lines <= 12:
            stdscr.erase()
            stdscr.addstr(1, 1, "Janela muito pequena!")
            stdscr.refresh()
            continue
        spacing = int((lines-(size*3)-2)*0.3)
        currentY = (lines - ((size*3)+(spacing*2)))//2
        width = int(0.9*cols)
        x = (cols - width) //2
        for option in options:
            try:
                optionWin = win.derwin(size,width,currentY,x)
                if (option.active):
                    optionWin.bkgd(' ', curses.color_pair(1) | curses.A_REVERSE)

                optionWin.border()
                textX = (width - len(option.name)) //2
                if size == 5:
                    textY = 2
                else:
                    textY = 1
                optionWin.addstr(textY,textX,option.name, curses.A_BOLD)
                optionWin.refresh()
                currentY+=size+spacing
            except curses.error:
                pass
        win.refresh()

        try:
            key = stdscr.getch()
            if key == ord('q'):
                sys.exit()
            elif key == 27:
                restaurant_selection(stdscr)
            elif key == curses.KEY_UP:
                if (activeOption == 0):
                    activeOption = len(options) - 1
                else:
                    activeOption -= 1
            elif  key == curses.KEY_DOWN:
                if (activeOption == len(options) - 1):
                    activeOption =  0
                else:
                    activeOption += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                    option = options[activeOption].function(stdscr, restaurant)

        except curses.error:
            pass
        curses.napms(100)      

def draw_logo(window, height, width):
    ascii_art = []
    file_path = os.path.join(BASE_DIR, 'ascii.txt')
    with open(file_path, 'r') as f:
        ascii_art = f.readlines()
    f.close()
    art_height = len(ascii_art)
    art_width = max(len(line) for line in ascii_art)

    if height < art_height + 2 or width < art_width + 2:
        try:
            window.erase()
            window.addstr(1, 1, "Janela muito pequena!")
            window.refresh()
        except curses.error:
            pass
        return 0,0,0


    start_y = 3
    start_x = (width - art_width) // 2

    for idx, line in enumerate(ascii_art):
        try:
            window.addstr(start_y + idx, start_x, line)
        except curses.error:
            pass  
    return (start_y + len(ascii_art)), art_width, len(ascii_art)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    restaurant_selection(stdscr)

    

if __name__ == '__main__':
    curses.wrapper(main)