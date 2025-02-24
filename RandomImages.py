from tkinter.filedialog import askdirectory
from os import walk
import tkinter as tk
from PIL import Image, ImageTk
from random import choice
import subprocess


class App:
    path = ""
    images = []
    dislayedImages = []
    buttons = []
    content_view = None

    imageWidth = 250
    imageHeight = 0

    amountToDisplay = 3
    def getPath(self):
        global path
        path = r'{}'.format(askdirectory(title="Choose directory", mustexist=True))
        DirLable.set(path)
        b2.config(state="normal")
        self.printPaths()
        
    def printPaths(self):
        self.images=[]
        self.displayedImages = []

        #clear buttons to add new ones
        for button in self.buttons:
            button.grid_remove()

        #walk to get all images
        for (dirpath, dirnames, filenames) in walk(path):
            self.images.extend(filenames)
            
            break

        tmpList = []
        for file in self.images:
            for ext in supported_extensions:
                if ext in file:
                    tmpList.append(file)

        self.images = tmpList
        
        if(len(self.images) > 0):
            rowVal = 3
            colVal = 1
            chosen = []
            amount = int(sp.get())

            #check to prevent out of bounds error
            if amount > len(self.images):
                amount = len(self.images)


            for x in range(amount):
                val = choice([i for i in range(0,len(self.images)) if i not in chosen])
               
                chosen.append(val)
                path_to_image = path+"/"+self.images[val]
                
                #get the current image sizes reduced
                tmpImg = Image.open(path_to_image)

                wpercent = (self.imageWidth/float(tmpImg.size[0]))
                hsize = int((float(tmpImg.size[1])*float(wpercent)))

                self.imageHeight = hsize

                image = ImageTk.PhotoImage(tmpImg.resize((self.imageWidth,self.imageHeight),Image.LANCZOS))
                self.displayedImages.append(image)
                l = tk.Button(master=self.content_view,image=self.displayedImages[x],text="", command=lambda x = path_to_image: self.showImage(x), background="#26242f")
                l.grid(row=rowVal,column=colVal,padx=5, pady=5)

                self.buttons.append(l)
                colVal+=1
                
                if(colVal >= 6):
                    colVal = 1
                    rowVal+=1

    def showImage(self,imPath):
        print(imPath)
        cleanPath = imPath.replace('/','\\')
        subprocess.Popen(f'explorer /select, "{cleanPath}"')

    

def _on_mousewheel(event):
    
    if(canvas.yview() != (0.0,1.0)):
        canvas.yview_scroll( int(-1 * (event.delta/120)), "units")
    

exts = Image.registered_extensions()
supported_extensions = {ex for ex, f in exts.items() if f in Image.OPEN}

# tkinter stuff
top = tk.Tk()
frame = tk.Frame(top)
frame.grid(row=1,column=1,sticky="nsew")
frame.config(bg="#26242f")
canvas = tk.Canvas()
scrollbar = tk.Scrollbar(top,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.config(bg="#26242f")

content = tk.Frame(canvas)
content.config(bg="#26242f")
content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


top.config(bg="#26242f")
app = App()
app.content_view = content
top.geometry("1350x980")
top.title("Random Image Chooser")

b = tk.Button(content,text="Choose directory", command=app.getPath,width=25)
b.grid(row=1,column=1, padx=5, pady=5)


DirLable = tk.StringVar()
selectedDirLable = tk.Label(content,textvariable=DirLable,bg="gray")
selectedDirLable.grid(row=1,column=2, padx=5, pady=5)

spLVariable = tk.StringVar(content,"Number of images to show")
spLable = tk.Label(content,textvariable=spLVariable)
spLable.grid(row=1,column=3, padx=5, pady=5)
sp = tk.Spinbox(content, from_=3, to=18)
sp.grid(row=1,column=4, padx=5, pady=5)

b2 = tk.Button(content,text="Get more images", command=app.printPaths,width=25)
b2.grid(row=1,column=5, padx=5, pady=5)
b2.config(state="disabled")

top.columnconfigure(0,weight=1)
top.rowconfigure(0,weight=1)
frame.columnconfigure(0,weight=1)
frame.rowconfigure(0,weight=1)

canvas.create_window((0,0), window=content, anchor="nw")
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0,column=6,sticky="ns")
canvas.bind_all("<MouseWheel>", _on_mousewheel)

top.mainloop()




