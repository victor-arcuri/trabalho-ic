import curses
import requests
from config import API_URL

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
                break
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
    return selectedRestaurant

def draw_logo(window, height, width):
    ascii_art = [
        " _____       _                       ",
        "/  __ \     | |                      ",
        "| /  \/ __ _| |_ _ __ __ _  ___ __ _ ",
        "| |    / _` | __| '__/ _` |/ __/ _` |",
        "| \__/\ (_| | |_| | | (_| | (_| (_| |",
        " \____/\__,_|\__|_|  \__,_|\___\__,_|"
    ]

    art_height = len(ascii_art)
    art_width = max(len(line) for line in ascii_art)

    if height < art_height + 2 or width < art_width + 2:
        try:
            window.addstr(1, 1, "Janela muito pequena para o ASCII!")
        except curses.error:
            pass
        return


    start_y = (height - art_height) // 2
    start_x = (width - art_width) // 2

    for idx, line in enumerate(ascii_art):
        try:
            window.addstr(start_y + idx, start_x, line)
        except curses.error:
            pass  

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    restaurant = restaurant_selection(stdscr)

    

if __name__ == '__main__':
    curses.wrapper(main)