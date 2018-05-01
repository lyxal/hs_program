class Screen:
    def __init__(self, p_name, p_window):
        """
        Takes: Self, the name of the screen

        Does: Initialises the screen class

        Returns: Nothing
        """
        self.widgets = list()
        self.name = p_name
        self.window = p_window
        self.hidden = True

    def add_item(self, p_widget, p_row, p_column):
        """
        Takes: Self, a tkinter widget, a row number and a column number

        Does: Adds the item to the list of widgets to show

        Returns: Nothing
        """
        self.widgets.append([p_widget, p_row, p_column])
        
    def show(self):
        for item in self.widgets:
            item[0].grid(row=item[1], column=item[2])
        self.window.title(self.name)
        self.hidden = False
            
    def hide(self):
        for item in self.widgets:
            item[0].grid_forget()
        self.hidden = True

    def __iter__(self):
        return iter(self.widgets)

    def update_widget(self, count, new_x):
        self.widgets[count][1] = new_x

class ScreenXY(Screen):
    def add_item(self, p_widget, p_x, p_y):
        '''
        Takes: Self, a tkinter widget, and the x/y co-ordinates

        Does: Adds the item to the list of widgets to show

        Returns: Nothing
        '''

        
        self.widgets.append([p_widget, p_x, p_y, p_x, p_y])

    def show(self):
        for item in self.widgets:
            item[0].place(x=item[1], y=item[2])

        self.window.title(self.name)
        self.hidden = False

    def hide(self):
        for item in self.widgets:
            item[0].place_forget()
        self.hidden = True

