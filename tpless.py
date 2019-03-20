from termpixels.app import App
from termpixels.screen import Color
import sys

class EditorApp(App):
    def __init__(self):
        super().__init__()
        if len(sys.argv) > 1:
            self.lines = open(sys.argv[1]).readlines()
        else:
            self.lines = sys.stdin.readlines()
        self.scroll_x = 0
        self.scroll_y = 0
        self._dirty = True
    
    def process_line(self, line):
        return line.replace("\t", " " * 4)
    
    def update(self):
        self.screen.clear()
        v_range = (self.scroll_y, self.scroll_y + self.screen.h)
        line_numbers_w = max(len(str(i)) for i in v_range)
        h_range = (self.scroll_x, self.scroll_x + self.screen.w - line_numbers_w)

        visible_lines = self.lines[v_range[0]:v_range[1]]
        for i, line in enumerate(visible_lines):
            line_num = " {} │".format(str(1 + i + v_range[0]).zfill(line_numbers_w))
            line_text = self.process_line(line)[h_range[0]:h_range[1]]
            self.screen.print(line_num, 0, i, fg=Color.rgb(0.7,0.7,0.7), bg=Color.rgb(0.2,0.2,0.2))
            self.screen.print(line_text, len(line_num), i)
        self.screen.update()
    
    def scroll(self, x, y):
        if x != 0 or y != 0:
            self._dirty = True
        self.scroll_x = max(0, self.scroll_x + x)
        self.scroll_y = max(0, self.scroll_y + y)

    def on_resize(self):
        self._dirty = True

    def on_frame(self):
        if self._dirty:
            self.update()
            self._dirty = False
    
    def on_key(self, key):
        if key == "down":
            self.scroll(0, 1)
        elif key == "up":
            self.scroll(0, -1)
        elif key == "left":
            self.scroll(-1, 0)
        elif key == "right":
            self.scroll(1, 0)

if __name__ == "__main__":
    EditorApp().start()