import curses
import requests
import sys
from totem.ascii import AsciiArtLoader
from totem.config import API_URL
artManager = AsciiArtLoader()

class Button:
    def __init__(self, text, function=None):
        self.text = text
        self.function = function
    
    def execute(self, **kwargs):
        if self.function != None:
            return self.function(**kwargs)

def invalid_recharge(stdscr):
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
        

        txt = "Valor inválido!"
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

def draw_bg(stdscr):
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    msg = "Pressione 'esc' para sair"
    y = height -3
    x = max((width - len(msg)) // 2, 1)
    if (width > len(msg)): stdscr.addstr(y,x,msg)
    stdscr.border()
    stdscr.refresh()

def validate_recharge(buffer):
    try:
        return float(buffer.replace(",","."))
    except: 
        return None

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

        logo = artManager.load_art('main_logo_2.txt')
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
            user = user_verify(buffer) 
            if user is None:
                user_not_found(stdscr)
                continue
            user_dashboard(stdscr, user)
            buffer = ""
            cursor_x = 1
        
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

def user_recharge(stdscr, user):
    tooSmall = False
    buffer = ""
    cursor_x = 1
    while True:
        curses.curs_set(1)
        height, width = stdscr.getmaxyx()
        if not tooSmall: draw_bg(stdscr)

        logo = artManager.load_art('main_logo_2.txt')
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
        
        msg = "Digite a quantia que deseja recarregar (R$):"
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
            amount = validate_recharge(buffer)
            if amount == None:
                invalid_recharge(stdscr)
                return None
            else:
                return requests.post(API_URL+f'usuario/{user["id"]}/recarregar', json={"amount":int(amount)*100}).json()
                break




        
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
                break
            else:
                continue
        
        # caracteres numéricos
        elif 48 <= key <= 57 or key == 44:
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

def user_dashboard(stdscr, user):
    tooSmall = False
    fump = None
    restaurants = None
    count = 0
    buttonIndex = 0
    while True:
        if (count == 0):
            fump = requests.get(API_URL+f'usuario/{user["id"]}/fump').json()
            restaurants = requests.get(API_URL+f'restaurante/').json()
            user = requests.get(API_URL+f'usuario/{user["id"]}').json()
            count = 10
        else:
            count -= 1
        stdscr.erase()
        stdscr.border()
        stdscr.refresh()
        curses.curs_set(0)
        height, width = stdscr.getmaxyx()
        logo = artManager.load_art('main_logo_2.txt')
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
        
        infoWinHeight = int(0.3*height)
        infoWinWidth = width - 2;
        infoWinY = height - infoWinHeight - 1
        infoWinX = 1
        infoWin = curses.newwin(infoWinHeight, infoWinWidth, infoWinY, infoWinX)
        if not tooSmall: infoWin.refresh()
        
        infoWinUserWidth = infoWinWidth//2 - 1
        infoWinUserHeight = infoWinHeight
        infoWinUserY = 0
        infoWinUserX = 0
        try:
            infoWinUser = infoWin.derwin(infoWinUserHeight, infoWinUserWidth, infoWinUserY, infoWinUserX)
            tooSmall = False
            infoWinUser.border()
        except curses.error:
            pass
        
        userWinLabel = "Informações de Usuário"
        userWinLabelY = 2
        userWinLabelX = (infoWinUserWidth - len(userWinLabel))// 2


        if (infoWinUserWidth > len(userWinLabel)):
            try:
                infoWinUser.addstr(userWinLabelY, userWinLabelX, userWinLabel, curses.A_BOLD)
            except curses.error:
                pass
        

                
        userWinUsernameLabel = "Usuário:"
        userWinUsernameContent = user["name"] + ' ' + user["surname"]
        userWinUsernameText = userWinUsernameLabel + " " + userWinUsernameContent

        userWinStudentIdLabel = "Matrícula:"
        userWinStudentIdContent = user["studentId"]
        userWinStudentIdText = userWinStudentIdLabel + " " + userWinStudentIdContent
        
        userWinFumpLabel = "FUMP:"
        userWinFumpLevel = 'Nível ' if user["fump"] > 0  else ''
        userWinFumpContent = f'{userWinFumpLevel}{fump["level"]} (almoço R${float(fump["price"])/100:.2f})'
        userWinFumpText = userWinFumpLabel + " " + userWinFumpContent

        userWinBalanceLabel = "Saldo:"
        userWinBalanceContent = f'R${float(user["balance"])/100:.2f}'
        userWinBalanceText = userWinBalanceLabel + " " + userWinBalanceContent

        labels = [userWinUsernameLabel, userWinStudentIdLabel, userWinFumpLabel,userWinBalanceLabel]
        contents = [userWinUsernameContent, userWinStudentIdContent,userWinFumpContent,userWinBalanceContent]
        texts = [userWinUsernameText, userWinStudentIdText,userWinFumpText,userWinBalanceText]
        textX = (infoWinUserWidth - len(max(texts, key=len))) // 2
        textY =  int((infoWinUserHeight - 3)*0.3) + 3
        starterTextY = textY
        
        if (infoWinUserWidth > len(max(texts,key=len))):
            for i,text in enumerate(texts):
                try:
                    tooSmall = False
                    infoWinUser.addstr(textY, textX, labels[i], curses.A_BOLD)
                    infoWinUser.addstr(textY, textX+len(labels[i])+1, contents[i])
                    textY+=1
                except curses.error:
                    tooSmall = True
                    too_small(stdscr)
                    continue
        
        if not tooSmall: infoWinUser.refresh()

        
        infoWinRestaurantWidth = infoWinWidth//2 - 1
        infoWinRestaurantHeight = infoWinHeight
        infoWinRestaurantY = 0
        infoWinRestaurantX = infoWinUserWidth + 1
        try:
            infoWinRestaurant = infoWin.derwin(infoWinRestaurantHeight, infoWinRestaurantWidth, infoWinRestaurantY, infoWinRestaurantX)
            tooSmall = False
            infoWinRestaurant.border()
        except:
            tooSmall = True
            pass
        if not tooSmall: infoWinRestaurant.refresh()
        
        restaurantWinLabel = "Lotação dos Restaurantes"
        restaurantWinLabelY = 2
        restaurantWinLabelX = (infoWinRestaurantWidth - len(restaurantWinLabel))// 2

        if (infoWinRestaurantWidth > len(restaurantWinLabel)):
            try:
                infoWinRestaurant.addstr(restaurantWinLabelY, restaurantWinLabelX, restaurantWinLabel, curses.A_BOLD)
            except curses.error:
                pass



        restaurantTexts = []
        for restaurant in restaurants:
            restaurantTexts.append(f'{restaurant["name"]}: {restaurant["occupancy"]}/{restaurant["capacity"]}')

        restaurantTextX = (infoWinRestaurantWidth - len(max(restaurantTexts, key=len))) // 2
        restaurantTextY = starterTextY

        if (infoWinRestaurantWidth > len(max(restaurantTexts,key=len))):
            for restaurant in restaurants:
                try:
                    tooSmall = False
                    infoWinRestaurant.addstr(restaurantTextY, restaurantTextX, restaurant["name"]+':', curses.A_BOLD)
                    if restaurant["occupancy"] >= 1 *  restaurant["capacity"]:
                        color = curses.color_pair(2)
                    elif restaurant["occupancy"] >= 0.8 * restaurant["capacity"]:
                        color = curses.color_pair(3)
                    else:
                        color = curses.color_pair(4)
                    infoWinRestaurant.addstr(restaurantTextY, restaurantTextX+len(restaurant["name"]+':')+2, f'{restaurant["occupancy"]}/{restaurant["capacity"]}', color)
                    restaurantTextY+=1

                except curses.error:
                    tooSmall = True
                    too_small(stdscr)
                    continue
        if not tooSmall: infoWinRestaurant.refresh()

        rechargeButtonText = "Recarregar cartão"
        exitButtonText = "Sair"

        buttonSize = 5
        buttonsArea = height - infoWinHeight - logoHeight
        spacing = int(0.1 * buttonsArea)
        buttonsTotalHeight = spacing + (buttonSize*2)
        buttonY = logoHeight + 1 + ((buttonsArea - buttonsTotalHeight)//2)
        buttonWidth = int(width*0.5)
        buttonX = (width - buttonWidth) // 2
        buttons = [Button(rechargeButtonText, user_recharge), Button(exitButtonText)]
        if (buttonY > (logoHeight+4) and width > buttonWidth):
            for index,button in enumerate(buttons):
                buttonWin = curses.newwin(buttonSize, buttonWidth, buttonY, buttonX)
                if buttonIndex == index:
                    buttonWin.bkgd(' ', curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD)    
                try:
                    buttonWin.addstr(2, (buttonWidth - len(button.text))// 2,  button.text)
                except curses.error:
                    pass
                buttonWin.border()
                buttonWin.refresh()
                buttonY += buttonSize + spacing

        
        key = stdscr.getch()
        
        if key == curses.KEY_RESIZE:
            continue

        elif key == curses.KEY_UP:
            buttonIndex = 1 if buttonIndex == 0 else 0
            continue
        elif key == curses.KEY_DOWN:
            buttonIndex = 1 if buttonIndex == 0 else 0
            continue
        elif key == curses.KEY_RIGHT:
            continue
        elif key == curses.KEY_LEFT:
            continue

        # Enter
        elif key in [10, 13]:
            if (buttonIndex == 1):
                break
            else:
                updateUser = buttons[buttonIndex].execute(stdscr=stdscr, user=user)
                if updateUser is not None:
                    user = updateUser
            continue
    

        curses.napms(100)
        

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    while True:
        login(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)