import pyautogui
import platform
import ctypes

class MouseController:
    def __init__(self):
        # Optimize PyAutoGUI for real-time tracking speed
        pyautogui.PAUSE = 0

        # WINDOWS optimization: Fix cursor scaling issues
        if platform.system() == "Windows":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

        self.screen_w, self.screen_h = pyautogui.size()
        self.ploc_x, self.ploc_y = 0, 0

        # Emergency Break: Slam mouse to top-left corner (0,0) to abort script execution
        pyautogui.FAILSAFE = True

    def move_cursor(self, raw_x, raw_y):
        # raw_x/raw_y expected to be normalized floats (0..1)
        try:
            screen_x = int(raw_x * self.screen_w)
            screen_y = int(raw_y * self.screen_h)
        except Exception:
            # If values are pixel coords, fallback
            screen_x = int(raw_x)
            screen_y = int(raw_y)

        # Smooth out pixel micro-jitters using LERP
        cloc_x = self.ploc_x + (screen_x - self.ploc_x) / 4
        cloc_y = self.ploc_y + (screen_y - self.ploc_y) / 4

        # Safely execute standard coordinate translations across desktop platforms
        pyautogui.moveTo(int(cloc_x), int(cloc_y))
        self.ploc_x, self.ploc_y = cloc_x, cloc_y

    def left_click_down(self):
        pyautogui.mouseDown()

    def left_click_up(self):
        pyautogui.mouseUp()

    def scroll_action(self, direction):
        if direction == "up":
            pyautogui.scroll(3)
        elif direction == "down":
            pyautogui.scroll(-3)
