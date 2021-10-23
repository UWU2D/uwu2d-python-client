import pygame

from ..services.keystack import KeyStack
from .service import Service


class InputService(Service):

    KEY_BACKSPACE = pygame.K_BACKSPACE
    KEY_TAB = pygame.K_TAB
    KEY_CLEAR = pygame.K_CLEAR
    KEY_RETURN = pygame.K_RETURN
    KEY_PAUSE = pygame.K_PAUSE
    KEY_ESCAPE = pygame.K_ESCAPE
    KEY_SPACE = pygame.K_SPACE
    KEY_EXCLAIM = pygame.K_EXCLAIM
    KEY_QUOTEDBL = pygame.K_QUOTEDBL
    KEY_HASH = pygame.K_HASH
    KEY_DOLLAR = pygame.K_DOLLAR
    KEY_AMPERSAND = pygame.K_AMPERSAND
    KEY_QUOTE = pygame.K_QUOTE
    KEY_LEFTPAREN = pygame.K_LEFTPAREN
    KEY_RIGHTPAREN = pygame.K_RIGHTPAREN
    KEY_ASTERISK = pygame.K_ASTERISK
    KEY_PLUS = pygame.K_PLUS
    KEY_COMMA = pygame.K_COMMA
    KEY_MINUS = pygame.K_MINUS
    KEY_PERIOD = pygame.K_PERIOD
    KEY_SLASH = pygame.K_SLASH
    KEY_0 = pygame.K_0
    KEY_1 = pygame.K_1
    KEY_2 = pygame.K_2
    KEY_3 = pygame.K_3
    KEY_4 = pygame.K_4
    KEY_5 = pygame.K_5
    KEY_6 = pygame.K_6
    KEY_7 = pygame.K_7
    KEY_8 = pygame.K_8
    KEY_9 = pygame.K_9
    KEY_COLON = pygame.K_COLON
    KEY_SEMICOLON = pygame.K_SEMICOLON
    KEY_LESS = pygame.K_LESS
    KEY_EQUALS = pygame.K_EQUALS
    KEY_GREATER = pygame.K_GREATER
    KEY_QUESTION = pygame.K_QUESTION
    KEY_AT = pygame.K_AT
    KEY_LEFTBRACKET = pygame.K_LEFTBRACKET
    KEY_BACKSLASH = pygame.K_BACKSLASH
    KEY_RIGHTBRACKET = pygame.K_RIGHTBRACKET
    KEY_CARET = pygame.K_CARET
    KEY_UNDERSCORE = pygame.K_UNDERSCORE
    KEY_BACKQUOTE = pygame.K_BACKQUOTE
    KEY_a = pygame.K_a
    KEY_b = pygame.K_b
    KEY_c = pygame.K_c
    KEY_d = pygame.K_d
    KEY_e = pygame.K_e
    KEY_f = pygame.K_f
    KEY_g = pygame.K_g
    KEY_h = pygame.K_h
    KEY_i = pygame.K_i
    KEY_j = pygame.K_j
    KEY_k = pygame.K_k
    KEY_l = pygame.K_l
    KEY_m = pygame.K_m
    KEY_n = pygame.K_n
    KEY_o = pygame.K_o
    KEY_p = pygame.K_p
    KEY_q = pygame.K_q
    KEY_r = pygame.K_r
    KEY_s = pygame.K_s
    KEY_t = pygame.K_t
    KEY_u = pygame.K_u
    KEY_v = pygame.K_v
    KEY_w = pygame.K_w
    KEY_x = pygame.K_x
    KEY_y = pygame.K_y
    KEY_z = pygame.K_z
    KEY_DELETE = pygame.K_DELETE
    KEY_KP0 = pygame.K_KP0
    KEY_KP1 = pygame.K_KP1
    KEY_KP2 = pygame.K_KP2
    KEY_KP3 = pygame.K_KP3
    KEY_KP4 = pygame.K_KP4
    KEY_KP5 = pygame.K_KP5
    KEY_KP6 = pygame.K_KP6
    KEY_KP7 = pygame.K_KP7
    KEY_KP8 = pygame.K_KP8
    KEY_KP9 = pygame.K_KP9
    KEY_KP_PERIOD = pygame.K_KP_PERIOD
    KEY_KP_DIVIDE = pygame.K_KP_DIVIDE
    KEY_KP_MULTIPLY = pygame.K_KP_MULTIPLY
    KEY_KP_MINUS = pygame.K_KP_MINUS
    KEY_KP_PLUS = pygame.K_KP_PLUS
    KEY_KP_ENTER = pygame.K_KP_ENTER
    KEY_KP_EQUALS = pygame.K_KP_EQUALS
    KEY_UP = pygame.K_UP
    KEY_DOWN = pygame.K_DOWN
    KEY_RIGHT = pygame.K_RIGHT
    KEY_LEFT = pygame.K_LEFT
    KEY_INSERT = pygame.K_INSERT
    KEY_HOME = pygame.K_HOME
    KEY_END = pygame.K_END
    KEY_PAGEUP = pygame.K_PAGEUP
    KEY_PAGEDOWN = pygame.K_PAGEDOWN
    KEY_F1 = pygame.K_F1
    KEY_F2 = pygame.K_F2
    KEY_F3 = pygame.K_F3
    KEY_F4 = pygame.K_F4
    KEY_F5 = pygame.K_F5
    KEY_F6 = pygame.K_F6
    KEY_F7 = pygame.K_F7
    KEY_F8 = pygame.K_F8
    KEY_F9 = pygame.K_F9
    KEY_F10 = pygame.K_F10
    KEY_F11 = pygame.K_F11
    KEY_F12 = pygame.K_F12
    KEY_F13 = pygame.K_F13
    KEY_F14 = pygame.K_F14
    KEY_F15 = pygame.K_F15
    KEY_NUMLOCK = pygame.K_NUMLOCK
    KEY_CAPSLOCK = pygame.K_CAPSLOCK
    KEY_SCROLLOCK = pygame.K_SCROLLOCK
    KEY_RSHIFT = pygame.K_RSHIFT
    KEY_LSHIFT = pygame.K_LSHIFT
    KEY_RCTRL = pygame.K_RCTRL
    KEY_LCTRL = pygame.K_LCTRL
    KEY_RALT = pygame.K_RALT
    KEY_LALT = pygame.K_LALT
    KEY_RMETA = pygame.K_RMETA
    KEY_LMETA = pygame.K_LMETA
    KEY_LSUPER = pygame.K_LSUPER
    KEY_RSUPER = pygame.K_RSUPER
    KEY_MODE = pygame.K_MODE
    KEY_HELP = pygame.K_HELP
    KEY_PRINT = pygame.K_PRINT
    KEY_SYSREQ = pygame.K_SYSREQ
    KEY_BREAK = pygame.K_BREAK
    KEY_MENU = pygame.K_MENU
    KEY_POWER = pygame.K_POWER
    KEY_EURO = pygame.K_EURO

    def __init__(self):
        super().__init__()

        self.key_listeners = {}
        self.mouse_motion_listeners = []
        self.mouse_click_listeners = []

        self.key_stack: KeyStack = KeyStack()

    def on_event(self, event):
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key in self.key_listeners:
                for c in self.key_listeners[event.key]:
                    c(event.key, True if event.type == pygame.KEYDOWN else False)

            if event.type == pygame.KEYDOWN:
                self.key_stack.press(event.key)
            elif event.type == pygame.KEYUP and len(self.key_stack) > 0:
                self.key_stack.release(event.key)
                if self.key_stack.is_key_pressed():
                    key = self.key_stack.active()
                    if key in self.key_listeners:
                        for c in self.key_listeners[key]:
                            c(key, True)

        elif event.type == pygame.MOUSEMOTION:
            for c in self.mouse_motion_listeners:
                c(event.pos[0], event.pos[1])
        elif event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
            for c in self.mouse_click_listeners:
                c(
                    event.pos[0],
                    event.pos[1],
                    event.button,
                    event.type == pygame.MOUSEBUTTONDOWN,
                )

    def register_key_event(self, key_code, callback):
        if key_code not in self.key_listeners:
            self.key_listeners[key_code] = []

        self.key_listeners[key_code].append(callback)

    def register_mouse_motion(self, callback):
        self.mouse_motion_listeners.append(callback)

    def register_mouse_click(self, callback):
        self.mouse_click_listeners.append(callback)
