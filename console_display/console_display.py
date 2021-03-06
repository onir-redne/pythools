# -*- coding: utf-8 -*-
import curses
import curses.panel
import signal
import time


class ConsoleTools(object):
    COLORS = {'CP_WHITE_BLACK': (0, curses.COLOR_WHITE, curses.COLOR_BLACK),
              'CP_WHITE_BLUE': (1, curses.COLOR_WHITE, curses.COLOR_BLUE),
              'CP_WHITE_CYAN': (2, curses.COLOR_WHITE, curses.COLOR_CYAN),
              'CP_WHITE_GREEN': (3, curses.COLOR_WHITE, curses.COLOR_GREEN),
              'CP_WHITE_MAGENTA': (4, curses.COLOR_WHITE, curses.COLOR_MAGENTA),
              'CP_WHITE_RED': (5, curses.COLOR_WHITE, curses.COLOR_RED),
              'CP_WHITE_YELLOW': (6, curses.COLOR_WHITE, curses.COLOR_YELLOW),
              'CP_BLACK_WHITE': (8, curses.COLOR_BLACK, curses.COLOR_WHITE),
              'CP_BLACK_BLUE': (9, curses.COLOR_BLACK, curses.COLOR_BLUE),
              'CP_BLACK_CYAN': (10, curses.COLOR_BLACK, curses.COLOR_CYAN),
              'CP_BLACK_GREEN': (11, curses.COLOR_BLACK, curses.COLOR_GREEN),
              'CP_BLACK_MAGENTA': (12, curses.COLOR_BLACK, curses.COLOR_MAGENTA),
              'CP_BLACK_RED': (13, curses.COLOR_BLACK, curses.COLOR_RED),
              'CP_BLACK_YELLOW': (14, curses.COLOR_BLACK, curses.COLOR_YELLOW),
              'CP_WHITE_BLACK': (15, curses.COLOR_WHITE, curses.COLOR_BLACK),
              'CP_BLUE_BLACK': (16, curses.COLOR_BLUE, curses.COLOR_BLACK),
              'CP_CYAN_BLACK': (17, curses.COLOR_CYAN, curses.COLOR_BLACK),
              'CP_GREEN_BLACK': (18, curses.COLOR_GREEN, curses.COLOR_BLACK),
              'CP_MAGENTA_BLACK': (19, curses.COLOR_MAGENTA, curses.COLOR_BLACK),
              'CP_RED_BLACK': (20, curses.COLOR_RED, curses.COLOR_BLACK),
              'CP_YELLOW_BLACK': (21, curses.COLOR_YELLOW, curses.COLOR_BLACK),
              'CP_BLACK_WHITE': (22, curses.COLOR_BLACK, curses.COLOR_WHITE),
              'CP_BLUE_WHITE': (23, curses.COLOR_BLUE, curses.COLOR_WHITE),
              'CP_CYAN_WHITE': (24, curses.COLOR_CYAN, curses.COLOR_WHITE),
              'CP_GREEN_WHITE': (25, curses.COLOR_GREEN, curses.COLOR_WHITE),
              'CP_MAGENTA_WHITE': (26, curses.COLOR_MAGENTA, curses.COLOR_WHITE),
              'CP_RED_WHITE': (27, curses.COLOR_RED, curses.COLOR_WHITE),
              'CP_YELLOW_WHITE': (28, curses.COLOR_YELLOW, curses.COLOR_WHITE)}

    @classmethod
    def color(cls, name, bold=False, blink=False, reverse=False):
        p = curses.color_pair(cls.COLORS[name][0])
        if bold:
            p |= curses.A_BOLD

        if blink:
            p |= curses.A_BLINK

        if reverse:
            p |= curses.A_REVERSE

        return p

    @classmethod
    def size(cls, win, h, w, y, x):
        maxy, maxx = win.getmaxyx()
        #offscr = False
        if isinstance(y, float):  # treat as percentage of total dimension
                cy = int(maxy * abs(y))
                if y < 0.0:
                    cy = maxy - cy
        elif isinstance(y, int):
            if abs(y) < maxy:
                cy = y
                if y < 0:
                    cy = maxy + y
            else:
                if y < 0:
                    cy = 0
                else:
                    cy = maxy - 1
        else:
            raise 'invalid y dimension format'

        if isinstance(x, float):  # treat as percentage of total dimension
            cx = int(maxx * abs(x))
            if x < 0.0:
                cx = maxx - cx
        elif isinstance(x, int):
            if abs(x) < maxx:
                cx = x
                if x < 0:
                    cx = maxx + x
            else:
                if x < 0:
                    cx = 0
                else:
                    cx = maxx - 1
        else:
            raise 'invalid x dimension format'

        maxh = maxy - cy
        maxw = maxx - cx

        if isinstance(h, float):  # treat as percentage of total dimension
            ch = int(maxh * h)
        elif isinstance(h, int):
            if h < maxh:
                ch = h
            else:
                ch = maxh - 1
        else:
            raise 'invalid w dimension format'

        if isinstance(w, float):  # treat as percentage of total dimension
            cw = int(maxw * w)
        elif isinstance(w, int):
            if w < maxw:
                cw = w
            else:
                cw = maxw - 1
        else:
            raise 'invalid h dimension format'

        return ch, cw, cy, cx


class ConsoleControl(object):
    """
    base class for any control
    """
    def __init__(self, parent_win, y, x, name, value, color):
        self._parent_win = parent_win
        self._y = y
        self._x = x
        self._name = name
        self._value = value
        self._visible = True
        self._color = color
        self._w = 0
        self._h = 0
        self._offscreen = False

        self._cb_invalidate_handler = None  # invalidate function forces redraw

    def get_name(self):
        return self._name

    def get_pos(self):
        return self._y, self._x

    def set_pos(self, y, x):
        self._y = y
        self._x = x

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_size(self):
        return self._h, self._w

    def set_size(self, h, w):
        self._h = h
        self._w = w

    def set_h(self, h):
        self._h = h
        if self._h == 0:
            self._h = 1

    def set_w(self, w):
        self._w = w
        if self._w == 0:
            self._w = 1

    def get_h(self,):
        return self._h

    def get_w(self):
        return self._w

    def set_hwyx(self, h, w, y, x):
        self._h = h
        self._w = w
        self._y = y
        self._x = x

    def get_hwyx(self):
        return self._h, self._w, self._y, self._x

    def hide(self):
        self._visible = False

    def show(self):
        self._visible = True

    def get_parent_win(self):
        return self._parent_win

    def update(self):
        pass

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def is_visible(self):
        return self._visible

    def process_input(self):
        pass

    def is_offscreen(self):
        return self._offscreen

    def set_offsecreen(self, offscreen):
        self._offscreen = offscreen



class ConsoleWindow(ConsoleControl):
    """
    Simple windows - can hold controls, automatically scales and allows resize accordingly to Display layout
    """
    def __init__(self, parent_win, h, w, y, x, name, title, color):

        super(ConsoleWindow, self).__init__(parent_win, y, x, name, title, color)
        self._controls = {}
        self.set_h(h)
        self.set_w(w)
        #super(ConsoleWindow, self)._h = h  # control specific
        #super(ConsoleWindow, self)._w = w

        self._last_h, self._last_w, self._last_y, self._last_x = ConsoleTools.size(self.get_parent_win(), self.get_h(),
                                                                                   self.get_w(), self.get_y(),
                                                                                   self.get_x())
        # self._win = self.get_parent_win().subpad(self._last_h, self._last_w, self._last_y, self._last_x)
        self._win = curses.newwin(self._last_h, self._last_w, self._last_y, self._last_x)
        self._win.bkgd(' ', self._color)
        self._panel = curses.panel.new_panel(self._win)
        self._panel.set_userptr(self.get_name())

    def add(self, control):
        self._controls[control.get_name()] = control

    def remove(self, name):
        self._controls.pop(name)

    def update(self):
        h, w, y, x = ConsoleTools.size(self.get_parent_win(), self.get_h(), self.get_w(), self.get_y(), self.get_x())
        if self._last_y != y or self._last_x != x or self._last_h != h or self._last_w != w:
            self._last_h = h
            self._last_w = w
            self._last_y = y
            self._last_x = x
            self._win.resize(self._last_h, self._last_w)
            self._win.mvwin(self._last_y, self._last_x)
            #self._win = curses.newwin(self._last_h, self._last_w, self._last_y, self._last_x)
            #self._win.bkgd(' ', self._color)
            #self._panel = curses.panel.new_panel(self._win)
            # self._win = self.get_parent_win().subpad(h, w, y, x)
            # self._win.bkgd(ord(' '), self.get_color())
            # self._win.mvderwin(y, x)

        if self.get_value():
            window_title_str = self.get_value() + ' (' + self.get_name() + ')'
            self._win.addstr(0, 1, window_title_str[:w - 2], self.get_color() | curses.A_REVERSE)

        for name, control in self._controls.iteritems():
            if control.is_visible():
                control.update()


class ConsoleLabel(ConsoleControl):

    def __init__(self, parent_win, y, x, name, value, color):

        if not isinstance(basestring, value):
            raise 'invalid value type'

        super(ConsoleLabel, self).__init__(parent_win, y, x, name, value, color)
        self.set_w(len(value))
        self.set_h(1)

    def update(self):
        self.get.addstr(self.get_y(), self.get_x(), self.get_value(), self.get_color())


class ConsoleProgressBar(ConsoleControl):
    pass


class ConsoleMenuBar(ConsoleControl):
    pass


class ConsoleDialog(ConsoleControl):
    pass


class ConsoleDisplay(object):
    """
    present test results on text console with curses
    """

    def __init__(self, debug=False):
        self._debug = debug
        self._cscreen = None
        self._maxy = 0
        self._maxx = 0
        self._subwindows = {}
        self._internal_windows = {}
        self._stopping = False
        self._mouse_nfo = {'x' : 0, 'y': 0, 'btn': 'L'}

        try:
            self._cscreen = curses.initscr()
            curses.start_color()
            curses.noecho()
            curses.cbreak()
            curses.use_default_colors()
            # self._cscreen.nodelay(1)
            # signal.signal(signal.SIGWINCH, self._cb_resize)

            for cname, cdef in ConsoleTools.COLORS.iteritems():
               curses.init_pair(*cdef)

            self._maxy, self._maxx = self._cscreen.getmaxyx()
            if self._debug: # create internal debug windows... they can be managed in different manner than user windows
                self._internal_windows['mouse_debug'] = ConsoleWindow(self._cscreen, 1, 10, 0, -0.2,
                                                                      'mouse_debug', None,
                                                                      ConsoleTools.color('CP_WHITE_MAGENTA'))
                self._internal_windows['mouse_debug'].add(ConsoleLabel(self._internal_windows['mouse_debug'], 0, 0,
                                                                       'test', 'test',
                                                                       ConsoleTools.color('CP_BLUE_WHITE')))
        except:
            self._curses_clean()

    def _curses_clean(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _cb_resize(self, n, frame):
        self._maxy, self._maxx = self._cscreen.getmaxyx()
        self._cscreen.clear()
        curses.resizeterm(self._maxy, self._maxx)

    def add_window(self, h, w, y, x, name, title, color):
        self._subwindows[name] = ConsoleWindow(self._cscreen, h, w, y, x, name, title, color)

    def update(self):
        #if curses.is_term_resized(self._maxy, self._maxx):
        for wname, win in self._subwindows.iteritems():
            win.update()

        for wname, win in self._internal_windows.iteritems():
            win.update()

        curses.panel.update_panels()
        self._cscreen.refresh()

    def run(self):
        try:
            self._loop()
        finally:
            self._curses_clean()

    def _loop(self):
        self.update()
        #time.sleep(5.0)
        while not self._stopping:
            key = curses.panel.top_panel().window().getch()
            if key == curses.KEY_RESIZE:       # terminal resized
                self._maxy, self._maxx = self._cscreen.getmaxyx()
                #curses.resizeterm(self._maxy, self._maxx)
                self._cscreen.clear()
                self.update()
            elif key == curses.KEY_MOUSE:
                # mouse event, if clicked an active panel pass to its handler otherwise
                # if clicked on inactive window make it active in other case use main
                # handler
                id, x, y, z, bstate = self._cscreen.getmouse()
                active_y, active_x = curses.panel.top_panel().window().getbegyx()
                #if x >= active_x and
                #pass
            elif key == ord('q'):
                self._stopping = True
