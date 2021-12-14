import curses
import time
from curses import wrapper
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Typing speed test!\n")
    stdscr.addstr("Press any key to start!")
    stdscr.refresh()
    stdscr.getch()


def dis_text(stdscr,target,typed,wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")
    for i,char in enumerate(typed):
        correct_text=target[i]
        color=curses.color_pair(2)
        if char != correct_text:
            color=curses.color_pair(1)
            
        stdscr.addstr(0,i,char,color)

def get_text():
    with open("text.txt","r") as f:
        lines=f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):    
    target_text=get_text()
    type_text=[]
    wpm=0
    start_time=time.time()
    stdscr.nodelay(True)

    while True:
        time_elaspe=max(time.time()-start_time,1)
        wpm=round((len(type_text)/(time_elaspe/60)/5))

        stdscr.clear()
        dis_text(stdscr,target_text,type_text,wpm)
        stdscr.refresh()

        if "".join(type_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key=stdscr.getkey()
        except:
            continue

        if ord(key)==27:
            break
        if key in ("KEY_BACKSPACE",'\b',"\x7f"):
            if len(type_text)>0:
                type_text.pop()
        elif len(type_text)<len(target_text):
            type_text.append(key)
        


def main(stdscr):
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0,"Congratulations you have completed the text!")
        stdscr.addstr(3,0,"Press any key to continue...")
        stdscr.addstr(4,0,"Or press ESC to escape the test.")
        key=stdscr.getkey()
        if ord(key)==27:
            break



wrapper(main) 