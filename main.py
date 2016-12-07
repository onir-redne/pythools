# -*- coding: utf-8 -*-
import console_display

def main():
    cd = console_display.ConsoleDisplay(True)
    cd.add_window(5, 31, 0.5, 0.5, 'win0', 'Windows 0', console_display.ConsoleTools.color('CP_WHITE_MAGENTA'))
    cd.add_window(0.5, 0.6, 2, 2, 'win1', 'Windows 1', console_display.ConsoleTools.color('CP_WHITE_BLUE'))
    cd.run()

if __name__ == '__main__':
    main()