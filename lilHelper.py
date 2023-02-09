import subprocess
from tkinter import *
from tkinter import ttk,filedialog
import tkinter as tk
import io
from PIL import ImageTk, Image
import dataBase as dB


class mainScr(tk.Tk):
    def __init__(self):
        super().__init__()

        self.aistart = True
        self.mainPage = Frame(self, bg='Ghost White')
        self.TreeVw = ttk.Treeview(self.mainPage, columns=str((1, 2, 3, 4)), show='headings', height=5)

        self.mainPage.grid(row=1, column=0)
        self.TreeVw.bind('<<TreeviewSelect>>', self.imgManager)

        self.photoLabel = Label(self.mainPage, image='')
        self.photoLabel.grid(row=2, column=0)

        x = Label(self)
        x.grid(row=0)
        self.srchData = Entry(x, width=20)
        self.srchData.grid(row=1, column=0)

        Button(x, text='add', command=self.hideWindow).grid(row=1, column=1)
        Button(x, text='edit', command=self.editCurfile).grid(row=1, column=2)
        Button(x, text='delete', command=self.delData).grid(row=1, column=3)
        Button(x, text='Search', command=self.searchData).grid(row=1, column=4)
        Button(x, text='IP info', command=lambda: dB.targetLongLat(self.srchData.get())).grid(row=1, column=8)
        Button(x, text='Encrypt file', command=self.encryptfile).grid(row=1, column=5)
        Button(x, text='YT downloader', command=dB.downWebmPortable).grid(row=1, column=6)
        Button(x, text='Screenrecorder', command=dB.scrnRecorder).grid(row=1, column=7)
        Button(x, text='Image to text', command=dB.ImageTotext).grid(row=1, column=9)
        Button(x, text='ScrShot', command=lambda: dB.cropScreenshot(mode='ScrShot')).grid(row=1, column=10)
        Button(x, text='Assistant', command= self.runaioffon).grid(row=1, column=12)
        Button(x, text='f10', command=self.showData).grid(row=1, column=11)

    def returnValues(self):
        try:
            viewInfo = self.TreeVw.focus()
            toyinf = self.TreeVw.item(viewInfo)
            row = toyinf['values']
            return row[0]
        except:
            pass


    def spchtxt(self):
        rt = Toplevel()
        showtxt = Text(rt,height=8)
        showtxt.grid()

    def editCurfile(self):

        def updateData():
            dB.dataUpdate(row[0], a.get(), v.get(), b.get(), SelText.get("1.0", 'end-1c'))
            editFrame.destroy()
            self.showData()

        cursel = self.TreeVw.focus()
        curselfocus = self.TreeVw.item(cursel)
        row = curselfocus['values']
        editFrame = Toplevel()
        a = Entry(editFrame, width=15)
        a.insert(END, row[1])

        v = Entry(editFrame, width=15)
        v.insert(END, row[2])

        b = Entry(editFrame, width=15)
        b.insert(END, row[3])

        a.grid(), v.grid(), b.grid()
        Button(editFrame, text="Submit", command=updateData, width=5).grid(row=1, column=1)
        SelText = Text(editFrame, height=20, width=100)
        SelText.insert(tk.END, dB.returnCode(row[0]))
        SelText.grid()

    def hideWindow(self):
        tk.Tk.withdraw(self)
        dB.cropScreenshot(mode='Database')
        tk.Tk.deiconify(self)

    def hideWindowForText(self):
        tk.Tk.withdraw(self)
        dB.ImageTotext()
        tk.Tk.deiconify(self)

    def imgManager(self, event):
        img = Image.open(io.BytesIO(dB.return_image(self.returnValues())))
        x = img.resize((1100, 650), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(x)
        self.photoLabel.configure(image=img)
        self.photoLabel.image = img

    def runaioffon(self):
        global subp

        if self.aistart == True:
            subp = subprocess.Popen(['python', 'offlinespch.py'])
            self.aistart = False

        elif self.aistart == False:
            subp.kill()
            self.aistart = True

    def delData(self):
        dB.deleteRec([self.returnValues()])
        self.showData()

    def encryptfile(self):
            x = Toplevel()
            current_var = tk.StringVar()
            combobox = ttk.Combobox(x, textvariable=current_var)
            combobox["values"] = ('Encrypt', 'Decrypt')
            combobox.grid()
            ttk.Button(x,text='continue',command=lambda: dB.filencrypter(file=filedialog.askopenfile(), mode=current_var.get())).grid()

    def showData(self):
        self.TreeVw.grid(row=1, column=0)
        self.TreeVw.delete(*self.TreeVw.get_children())
        b = dB.showData()
        for x in b:
            self.TreeVw.insert(parent='', index='end', text='Parent Shit', values=x)

    def searchData(self):
        self.TreeVw.delete(*self.TreeVw.get_children())
        b = dB.searchData(self.srchData.get())
        for x in b:
            self.TreeVw.insert(parent='', index='end', text='Parent Shit', values=x)


if __name__ == "__main__":
    app = mainScr()
    app.mainloop()
