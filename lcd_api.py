import time

class LCD:

    LCD_CLR =  0X01
    LCD_HOME = 0X02

    LCD_ENTRY_MODE =0X04
    LCD_INCREMENT =0X02
    LCD_SHIFT =0X01

    LCD_CONTROL = 0X08
    LCD_DISPLAY = 0X04
    LCD_CURSOR_ON = 0X02
    LCD_BLINK_CURSOR = 0X01

    LCD_MOVE = 0X10
    LCD_MOVE_DISP = 0X08
    LCD_MOVE_RIGHT = 0X04

    LCD_FUNCTION = 0X20
    LCD_FUNCTION_8BIT = 0X10
    LCD_FUNCTION_2LINES = 0X08
    LCD_FUNCTION_10DOTS = 0X04
    LCD_FUNCTION_RESET = 0X30
    

    LCD_CGRAM = 0X40
    LCD_DDRAM = 0X80
    
    LCD_RS_CM = 0
    LCD_RS_DATA = 1


    LCD_RW_CMD = 0
    LCD_RW_READ = 1

    def init(self, num_lines, num_columns):
        self.num_lines= num_lines
        if self.num_lines>4:
            self.num_lines= 4
        self.num_columns = num_columns
        if num_columns>40:
            self.num_columns= 40
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_line = False
        self.backlight = True
        self.display_off()
        self.backlight_on()
        self.clear()
        self.display_on()
        self.hide_cursor()
        self.write(self.LCD_ENTRY_MODE, self. LCD_INCREMENT)
    
    def show_cursor(self):
        self.write(self.LCD_CONTROL| self.LCD_DISPLAY | self.LCD_CURSOR_ON )

    def clear (self):
        self.write(self.LCD_CLR)
        self.write(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y=0
    
    def backlight_on(self):
        self.backlight = True
        self.writeon()

    def backlight_off(self):
        self.backlight = False
        self.writeoff()
    
    def blink_cursoron(self):
        self.write()
        self.write(self.LCD_CONTROL | self.LCD_DISPLAY |self.LCD_CURSOR_ON | self.LCD_BLINK_CURSOR)

    def blink_cursoroff(self):
        self.write(self.LCD_CONTROL | self.LCD_DISPLAY |self.LCD_CURSOR_ON | self.LCD_BLINK_CURSOR)

    def hide_cursor(self):
        self.write(self.LCD_CONTROL | self.LCD_DISPLAY)
    def show_cursor(self):
        self.write(self.LCD_CONTROL | self.LCD_DISPLAY | self.LCD_CURSOR_ON)
    def display_off(self):
        self.write(self.LCD_CONTROL)
    def display_on(self):
        self.write(self.LCD_CONTROL | self.LCD_DISPLAY)


    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3f
        if cursor_y & 1:
            addr += 0x40    # Lines 1 & 3 add 0x40
        if cursor_y & 2:    # Lines 2 & 3 add number of columns
            addr += self.num_columns
        self.write(self.LCD_DDRAM | addr)

    def putchar(self, char):
        if char == '\n':
            if self.implied_newline:
                self.implied_newline = False
            else:
                self.cursor_x = self.num_columns
        else:
            self.write_data(ord(char))
            self.cursor_x += 1
        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = (char != '\n')
        if self.cursor_y >= self.num_lines:
            self.cursor_y = 0
        self.move_to(self.cursor_x, self.cursor_y)

    def putstr(self, string):
        for char in string:
            self.putchar(char)

    def custom_char(self, location, charmap):
        location &= 0x7
        self.write_command(self.LCD_CGRAM | (location << 3))
        self.hal_sleep_us(40)
        for i in range(8):
            self.write_data(charmap[i])
            self.write_sleep_us(40)
        self.move_to(self.cursor_x, self.cursor_y)

    def write_backlight_on(self):
        pass

    def write_backlight_off(self):
        pass

    def write_write_command(self, cmd):
        raise NotImplementedError

    def write_write_data(self, data):
         raise NotImplementedError

    def write_sleep_us(self, usecs):
        time.sleep_us(usecs)
