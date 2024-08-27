import time
from tkinter import filedialog
import customtkinter
from PIL import Image
import os

# Open the binary content file once and use it throughout
writelog = open("binarycontent.txt", "w")

# Conversion flag
convertedlen = False

def rgb_to_binary(r, g, b):
    # Scale each RGB value from range 0-255 to range 0-7
    r_scaled = r * 7 // 255
    g_scaled = g * 7 // 255
    b_scaled = b * 7 // 255
    
    # Convert each scaled value to a 3-bit binary string
    r_bin = f'{r_scaled:03b}'
    g_bin = f'{g_scaled:03b}'
    b_bin = f'{b_scaled:03b}'
    
    # Combine into a 9-bit binary string
    binary_content = r_bin + g_bin + b_bin
    
    return binary_content

def convert():
    try:
        with open("Rgbfile.txt", "r") as readnewfile:
            for line in readnewfile:
                rgb_value = line.strip().split()
                r, g, b = map(int, rgb_value)
                binary_content = rgb_to_binary(r, g, b)
                writelog.write(binary_content + "\n")
    except Exception as e:
        errorlbl.configure(text=f"Error during conversion: {e}")
        print(f"Exception occurred in convert: {e}")

def correct_image_orientation(img):
    try:
        exif = img._getexif()
        orientation_tag = 274  # Tag for orientation

        if exif is not None and orientation_tag in exif:
            orientation = exif[orientation_tag]

            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    
    except Exception as e:
        print(f"Error correcting image orientation: {e}")

    return img

def conversion():
    global convertedlen
    bitnum = bitsslider.get()

    if not photopath:
        errorlbl.configure(text="No image selected.")
        return

    try:
        print(f"Opening image at {photopath}")
        img = Image.open(photopath)
        img = correct_image_orientation(img)  # Correct image orientation
        imgwidth, imgheight = img.size
        print(f"Image size: {imgwidth}x{imgheight}")

        if imgwidth > 128 or imgheight > 128:
            errorlbl.configure(text="Image too big, must be 128x128 or smaller")
            return
        
        convertedlen = True
        errorlbl.configure(text="Converting to binary...", text_color="green")
        rgbimg = img.convert("RGB")

        with open("Rgbfile.txt", "w") as newfile:
            for x in range(imgwidth):
                for y in range(imgheight):
                    r, g, b = rgbimg.getpixel((x, y))
                    newfile.write(f"{r} {g} {b}\n")
        
        correctlbl.configure(text="Converted to RGB. Click 'Convert' again.")
        convert()
    
    except Exception as e:
        errorlbl.configure(text=f"Error: {e}")
        print(f"Exception occurred in conversion: {e}")

def openfile():
    global photopath
    photopath = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if photopath:
        if photopath.endswith(".png"):
            os.startfile(photopath)
        else:
            errorlbl.configure(text="Please choose a .png file")

mainwindow = customtkinter.CTk()
mainwindow.title("Junz Color RGB")
mainwindow.geometry("500x500")

header = customtkinter.CTkLabel(mainwindow, text="Junz Color RGB", font=("Arial", 20))
header.place(relx=0.5, rely=0.2, anchor="center")

photobtn = customtkinter.CTkButton(mainwindow, text="Choose Photo", command=openfile)
photobtn.place(relx=0.5, rely=0.5, anchor="center")

convertbtn = customtkinter.CTkButton(mainwindow, text="Convert", command=conversion)
convertbtn.place(relx=0.5, rely=0.7, anchor="center")

bitsslider = customtkinter.CTkSlider(mainwindow, from_=0, to=9, number_of_steps=9)
bitsslider.place(relx=0.5, rely=0.4, anchor="center")

errorlbl = customtkinter.CTkLabel(mainwindow, text=" ", text_color="red")
errorlbl.place(relx=0.5, rely=0.6, anchor="center")

correctlbl = customtkinter.CTkLabel(mainwindow, text=" ", text_color="green")
correctlbl.place(relx=0.5, rely=0.8, anchor="center")

mainwindow.mainloop()
