import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Image Viewer and Converter')
        self.geometry('900x600')  # Increased width for toolbar

        # Main container frame
        container = ttk.Frame(self)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Image display area
        self.image_panel = tk.Canvas(container, bg='gray')  

        # Scrollbars for the canvas
        self.scroll_x = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.image_panel.xview)
        self.scroll_y = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.image_panel.yview)
        self.image_panel.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        # Pack scrollbars and canvas
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.image_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind arrow keys for navigation
        self.bind('<Left>', self.scroll_left)
        self.bind('<Right>', self.scroll_right)
        self.bind('<Up>', self.scroll_up)
        self.bind('<Down>', self.scroll_down)
        
        # Make sure the canvas is focusable
        self.image_panel.focus_set()

        # Toolbar
        self.toolbar = ttk.Frame(self, padding="5 5 5 5")
        self.toolbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Threshold value entry
        self.threshold_value = tk.IntVar(value=127)  # Default threshold value
        self.threshold_entry = ttk.Entry(self.toolbar, textvariable=self.threshold_value, width=5)
        

        # Decrement button
        self.dec_button = ttk.Button(self.toolbar, text='<', command=self.decrement_threshold)
        self.dec_button.pack(side=tk.LEFT)


        self.threshold_entry.pack(side=tk.LEFT)

        # Increment button
        self.inc_button = ttk.Button(self.toolbar, text='>', command=self.increment_threshold)
        self.inc_button.pack(side=tk.RIGHT)

        self.create_menu()

        self.original_image = None
        self.processed_image = None
        self.photo_image = None  # To keep a reference



    def scroll_left(self, event):
        self.image_panel.xview_scroll(-1, "units")  # Scroll left

    def scroll_right(self, event):
        self.image_panel.xview_scroll(1, "units")  # Scroll right

    def scroll_up(self, event):
        self.image_panel.yview_scroll(-1, "units")  # Scroll up

    def scroll_down(self, event):
        self.image_panel.yview_scroll(1, "units")  # Scroll down

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_image)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)

        menubar.add_cascade(label='File', menu=file_menu)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('PNG files', '*.png'), ('JPG files', '*.jpg'), ('All files', '*.*')])
        if not file_path:
            return

        self.original_image = cv2.imread(file_path)
        self.processed_image = self.original_image.copy()
        self.display_image(self.processed_image)

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        self.photo_image = ImageTk.PhotoImage(image=img_pil)
        self.image_panel.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
        self.image_panel.config(scrollregion=self.image_panel.bbox(tk.ALL))

    def convert_to_grayscale(self):
        if self.original_image is None:
            messagebox.showerror('Error', 'No image loaded.')
            return

        self.processed_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2BGR)
        self.display_image(self.processed_image)
       
    def update_threshold(self, value):
        # Modified to work with the IntVar of the entry
        self.threshold_value.set(int(value))
        self.apply_threshold()

    def apply_threshold(self):
        if self.original_image is None:
            return
        _, thresh_image = cv2.threshold(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY), self.threshold_value.get(), 255, cv2.THRESH_BINARY)
        self.processed_image = cv2.cvtColor(thresh_image, cv2.COLOR_GRAY2BGR)
        self.display_image(self.processed_image)

    def increment_threshold(self):
        self.threshold_value.set(self.threshold_value.get() + 5)
        self.apply_threshold()

    def decrement_threshold(self):
        self.threshold_value.set(max(0, self.threshold_value.get() - 5))  # Ensure threshold doesn't go below 0
        self.apply_threshold()

if __name__ == '__main__':
    app = ImageApp()
    app.mainloop()
