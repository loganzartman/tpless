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
        self.input_buffer = []
        self.search_mode = False
        self._dirty = True
        self._stopping = False
    
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
        
        if self.search_mode:
            search_term = "".join(self.input_buffer)
            self.screen.fill(0, self.screen.h-1, self.screen.w, 1, char=" ", fg=Color.rgb(0,0,0), bg=Color.rgb(1,1,1))
            x, y = self.screen.print("/{}".format(search_term), 0, self.screen.h-1)
            self.screen.show_cursor = True
            self.screen.cursor_pos = (x, y)
        else:
            self.screen.show_cursor = False
        self.screen.update()
    
    def scroll(self, x, y):
        if x != 0 or y != 0:
            self._dirty = True
        self.scroll_x = max(0, self.scroll_x + x)
        self.scroll_y = max(0, self.scroll_y + y)
    
    def search(self, s):
        for i, line in enumerate(self.lines[self.scroll_y + 1:]):
            try:
                line.index(s)
                self.scroll_y += i + 1
                break
            except:
                pass
        self._dirty = True

    def on_resize(self):
        self._dirty = True

    def on_frame(self):
        if self._stopping:
            raise KeyboardInterrupt()
        if self._dirty:
            self.update()
            self._dirty = False
    
    def on_key(self, key):
        if not self.search_mode:
            if key == "down":
                self.scroll(0, 1)
            elif key == "up":
                self.scroll(0, -1)
            elif key == "left":
                self.scroll(-1, 0)
            elif key == "right":
                self.scroll(1, 0)
            elif key == "g":
                self.scroll_y = 0
                self._dirty = True
            elif key == "G":
                self.scroll_y = max(0, len(self.lines) - self.screen.h)
                self._dirty = True
            elif key == "q":
                self._stopping = True
            elif key.char == "/":
                self.search_mode = True
                self.input_buffer = []
                self._dirty = True
            elif key.char == "n" and len(self.input_buffer) > 0:
                self.search("".join(self.input_buffer))
        else:
            if key == "backspace":
                self.input_buffer = self.input_buffer[:-1]
                self._dirty = True
            elif key == "\n" or key == "\r":
                self.search("".join(self.input_buffer))
                self.search_mode = False
            elif key.char:
                self.input_buffer.append(key.char)
                self._dirty = True

if __name__ == "__main__":
    EditorApp().start()
