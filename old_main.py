import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
'''
# Step 1: Import image file with TK
 - Store as a variable?
 - Size limit?
 - with keyword
# Use PIL.ImageTk to display image in GUI
# Step 2: Modify image file
 - PIL to combine with watermark.png
# Step 3: Implement in tkinter

# Notes: 
Does tkinter have a 'native' function to upload files?
'''
new_tk = ''
picture_tk = None
def watermark_image(input) -> Image:
    img = Image.open(input)
    watermark = Image.open('watermark.png')
    watermark_new_size: tuple[int, int] = (int(img.width*0.5), int(img.width*0.5))
    resized_watermark = watermark.resize(watermark_new_size)
    img.paste(
        resized_watermark, 
        (0,0),
        resized_watermark)
    return img

def upload_file():
    global picture_tk
    size = (500,500)
    file = filedialog.askopenfilename()
    picture = watermark_image(file)
    picture = ImageOps.pad(picture, size)
    picture_tk = ImageTk.PhotoImage(picture)
    display.itemconfig(display_image, image=picture_tk)

def update_canvas():
    global new_tk
    new_image = Image.open('watermark.png')
    new_tk = ImageTk.PhotoImage(new_image, (500,500))
    display.itemconfig(display_image, image=new_tk)


    

if __name__ == "__main__":
    window= tk.Tk()
    button = tk.Button(text='Click me', command=upload_file)

    blank_image = Image.open('blank.png')
    blank_tk = ImageTk.PhotoImage(blank_image)
    display = tk.Canvas(width=500, height=500)
    display_image = display.create_image(250, 250, image=blank_tk)

    display.grid(row=0,column=0)
    button.grid(row=1,column=0)

    window.mainloop()
    