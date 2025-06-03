import curses
import requests
import sys
from totem.ascii import AsciiArtLoader
from totem.config import API_URL
artManager = AsciiArtLoader()

def draw_bg(stdscr):
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    msg = "Pressione 'esc' para sair"
    y = height -3
    x = max((width - len(msg)) // 2, 1)
    if (width > len(msg)): stdscr.addstr(y,x,msg)
    stdscr.border()
    stdscr.refresh()


def user_verify(studentId):
    try:
        users = requests.get(API_URL+'usuario/').json()
    except:
        return None
    for user in users:
        if user.get("studentId", "") == studentId:
            return user
        return None
    
def too_small(stdscr):
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()
    try:
        stdscr.erase()
        msg = "Janela muito pequena!"
        x = (width - len(msg)) // 2
        y = max((height - 1) // 2,1)
        try:
            stdscr.addstr(y,x,msg)
        except curses.error:
            pass
        stdscr.refresh()
    except curses.error:
        pass

def login(stdscr):
    tooSmall = False
    buffer = ""
    cursor_x = 1
    while True:
        curses.curs_set(1)
        height, width = stdscr.getmaxyx()
        if not tooSmall: draw_bg(stdscr)

        logo = artManager.load_art('main_logo.txt')
        logoWidth = len(max(logo))
        logoHeight = len(logo)
        if (width >= logoWidth + 16 and height >= logoHeight + 4):
            logoY = 5
            logoX = (width - logoWidth) // 2
            for line in logo:
                stdscr.addstr(logoY, logoX, line)
                logoY += 1
            stdscr.border()
            if not tooSmall: stdscr.refresh()
        else:
            tooSmall = True
            too_small(stdscr)
            continue
            

        winWidth = int(width*0.5)
        winHeight = 3
        winX = (width - winWidth) // 2
        area = height - logoY  
        winY = logoY - 2 + int((area - winHeight)*0.35 )
        win = curses.newwin(winHeight, winWidth, winY, winX)
        
        msg = "Digite sua matrícula ou passe o cartão para entrar:"
        x = winX + 1
        y = winY - 1

        if (winWidth < len(msg)):
            x = (width - len(msg)) // 2
        if (y > logoY):
            tooSmall = False
            stdscr.addstr(y,x,msg, curses.A_BOLD)
            stdscr.refresh()
            win.border()
            winTxtY = winY+1
            winTxtX = winX+1
            if winWidth <= len(buffer):
                try:
                    win.addstr(1, 1, buffer[:-(len(buffer) - winWidth) -2])
                except curses.error:
                    pass
            else:
                try:
                    win.addstr(1, 1, buffer)
                except curses.error:
                    pass
            try:
                win.move(1,cursor_x)
            except:
                curses.curs_set(0)
            if not tooSmall: win.refresh()
        else:
            tooSmall = True
            too_small(stdscr)
            continue


    
        key = win.getch()
        
        if key == curses.KEY_RESIZE:
            continue

        elif key == curses.KEY_UP:
            continue
        elif key == curses.KEY_DOWN:
            continue
        elif key == curses.KEY_RIGHT:
            continue
        elif key == curses.KEY_LEFT:
            continue

        # Enter
        elif key in [10, 13]:
            if user_verify(buffer) is None:
                user_not_found(stdscr)
        
        # Backspace
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if len(buffer) > 0:
                buffer = buffer[:-1]
                cursor_x = max(cursor_x - 1, 1)

        # ESC
        elif key == 27:
            stdscr.nodelay(True)
            sequence = []
            while True:
                next_key = stdscr.getch()
                if next_key == -1:
                    break
                sequence.append(next_key)
            stdscr.nodelay(False)
            
            if not sequence:
                sys.exit()
            else:
                continue
        
        # Caracteres imprimíveis
        elif 32 <= key <= 126:
            if len(buffer) < (winWidth - 2):
                buffer += chr(key)
                cursor_x += 1

        

        curses.napms(50)

def user_not_found(stdscr):
    tooSmall = False
    while True:
        curses.curs_set(0)
        height, width = stdscr.getmaxyx()
        if not tooSmall: draw_bg(stdscr)
        winHeight = int(height * 0.3)
        winWidth = int(width * 0.3)
        winY = (height - winHeight) // 2
        winX = (width - winWidth) // 2
        win = curses.newwin(winHeight, winWidth, winY, winX)
        win.border()
        

        txt = "Usuário não encontrado!"
        txtWidth = len(txt)
        txtY = int(winHeight * 0.4)
        txtX = (winWidth - txtWidth) // 2
        if not tooSmall: 
            win.addstr(txtY, txtX, txt, curses.A_BOLD)
            win.refresh()
        if winWidth <= txtWidth + 6:
            tooSmall = True
            too_small(stdscr)
            continue
        else:
            tooSmall = False

        buttonTxt = "Retornar"
        buttonHeight = 3
        buttonWidth = len(buttonTxt) + 10   
        buttonY = txtY + 1 + int((winHeight - (txtY)) * 0.4)
        buttonX = (winWidth - buttonWidth) // 2
        try:
            btn = win.derwin(buttonHeight, buttonWidth, buttonY, buttonX)
            btn.addstr(1, (buttonWidth - len(buttonTxt)) //2 , buttonTxt)
            btn.border()
            btn.refresh()
        except:
            pass


        key = win.getch()
        
        if key == curses.KEY_RESIZE:
            continue

        elif key == curses.KEY_UP:
            continue
        elif key == curses.KEY_DOWN:
            continue
        elif key == curses.KEY_RIGHT:
            continue
        elif key == curses.KEY_LEFT:
            continue

        # Enter
        elif key in [10, 13]:
            btn.bkgd(' ', curses.color_pair(1) | curses.A_REVERSE)
            btn.addstr(1, (buttonWidth - len(buttonTxt)) //2 , buttonTxt, curses.A_BOLD)
            btn.border()
            btn.refresh()
            curses.napms(50)
            return

        # ESC
        elif key == 27:
            stdscr.nodelay(True)
            sequence = []
            while True:
                next_key = stdscr.getch()
                if next_key == -1:
                    break
                sequence.append(next_key)
            stdscr.nodelay(False)
            
            if not sequence:
                sys.exit()
            else:
                continue


        
        curses.napms(100)
        
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    while True:
        login(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)