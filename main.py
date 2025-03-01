from PIL import Image, ImageTk, ImageOps, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog, messagebox, TclError
import os
from pathlib import Path

app_dir = os.path.dirname(os.path.abspath(__file__))
pictures_dir = f"{Path.home()}/Pictures"
os.chdir(app_dir)

class App():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Watermark')
        self.window.config(padx=5, pady=5, bg='white')
        self.blank = Image.open('blank.png')
        self.blank_tk = ImageTk.PhotoImage(self.blank)
        self.display = tk.Canvas(width=500, height=500)
        self.display_image = self.display.create_image(250, 250, image=self.blank_tk)
        self.is_watermarked = False
        self.upload_button = tk.Button(text='Upload File', command=self.stage_image)
        self.watermark_button = None
        self.download_button = None        
        self.display.grid(row=0,column=0, columnspan=3, pady=5)
        self.watermark = Image.open('watermark.png')
        if os.path.isdir(pictures_dir):
            self.default_directory = pictures_dir
        elif os.path.isdir(Path.home()):
            self.default_directory = Path.home()
        else:
            self.default_directory = app_dir
        self.load_buttons()      

    def stage_image(self):
        if self.is_watermarked:
            self.is_watermarked = False
        file = filedialog.askopenfilename(initialdir=self.default_directory)
        try:
            self.picture = Image.open(file)
        except AttributeError:
            return
        except UnidentifiedImageError:
            messagebox.showinfo(title='Not an image', message='Not a valid image file.')
            return
        self.watermark_button = tk.Button(text="Add Watermark", command=self.watermark_image)
        self.download_button = tk.Button(text="Save Image", command=self.download_image)
        self.load_buttons()
        self.display_picture()

    def watermark_image(self):
        if self.is_watermarked:
            messagebox.showinfo(title='Already watermarked', message='This image is already watermarked')
            return
        dimension = min(self.picture.width, self.picture.height)
        watermark_new_size: tuple[int, int] = (
            int(dimension*0.5),
            int(dimension*0.5)
            )
        resized_watermark = self.watermark.resize(watermark_new_size)
        self.picture.paste(
            resized_watermark, 
            (0,0),
            resized_watermark)
        self.is_watermarked = True
        self.load_buttons()
        self.display_picture()

    def download_image(self):
        if not self.is_watermarked:
            messagebox.showinfo(title='Not watermarked', message='This image has not been watermarked.')
            return
        image_title = os.path.basename(self.picture.filename)
        saveas_title = f'watermarked_{image_title}'
        watermarked_image = filedialog.asksaveasfilename(initialfile=saveas_title, initialdir=self.default_directory)
        try:
            self.picture.save(watermarked_image)
        except ValueError:
            return
        messagebox.showinfo(title='Picture saved', message='Picture has been saved.')
        self.reinit()

    def load_buttons(self):
        if self.watermark_button:
            self.watermark_button.grid(row=1, column=0)
        if self.upload_button:
            self.upload_button.grid(row=1,column=1)
        if self.download_button:
            self.download_button.grid(row=1, column=2)  


    def display_picture(self):
        size = (500,500)
        staged_image = ImageOps.pad(self.picture, size)
        self.picture_tk = ImageTk.PhotoImage(staged_image, (500,500))
        self.display.itemconfig(self.display_image, image=self.picture_tk)

    def reinit(self):
        self.picture = Image.open('blank.png')
        self.download_button.destroy()
        self.watermark_button.destroy()
        self.display_picture()

def main():
    app = App()
    app.window
    app.window.mainloop()

if __name__ == "__main__":
    main()