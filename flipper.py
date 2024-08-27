from PIL import Image
from customtkinter import filedialog
import customtkinter



mainwindow = customtkinter.CTk()
mainwindow.geometry("300x200")


def readjust():
    img = Image.open(filepath)
    imgflip = img.rotate(90, expand=True)
    imgflip.save("test.png")
    convertedlbl.configure(text="converted")

def openfile():
    global filepath
    filepath = filedialog.askopenfilename()
    print(filepath)
    correctlbl.configure(text=filepath)


button = customtkinter.CTkButton(mainwindow, text="openfile", command=openfile)
button.place(relx=0.5, rely=0.5, anchor="center")

correctlbl = customtkinter.CTkLabel(mainwindow, text=" ")
correctlbl.place(relx=0.5, rely=0.6, anchor="center")

readjustbutton = customtkinter.CTkButton(mainwindow, text="readjust", command=readjust)
readjustbutton.place(relx=0.5, rely=0.7, anchor="center")

convertedlbl = customtkinter.CTkLabel(mainwindow, text=" ")
convertedlbl.place(relx=0.5, rely=0.8, anchor="center")
mainwindow.mainloop()
