from tkinter import *
from tkinter import ttk
import tkinter as tk
import io
from PIL import ImageTk, Image
import dataBase as dB

class mainScr(tk.Tk):
    def __init__(self):
        super().__init__()
        self.mainPage = Frame(self,bg='Ghost White')
        self.TreeVw = ttk.Treeview(self.mainPage, columns=(1, 2, 3 , 4), show='headings', height='5')
        self.mainPage.grid(row =1,column=0)
        self.TreeVw.bind('<<TreeviewSelect>>',self.imgManager)
        self.TreeVw.grid(row=1,column=0)

        self.photoLabel = Label(self.mainPage, image = '')
        self.photoLabel.grid()

        x = Label(self)
        x.grid(row=0)
        self.showData()
        self.srchData= Entry(x,width=20)
        self.srchData.grid(row=1,column=0)
        Button(x,text='add',command = dB.cropScreenshot).grid(row=1,column=1)
        Button(x,text='delete',command=self.delData).grid(row=1,column=2)
        Button(x,text='Search',command=self.searchData).grid(row=1,column=3)
        Button(x,text='f10',command= self.showData).grid(row=1,column=4)


    def returnValues(self):
            try:
                viewInfo = self.TreeVw.focus()
                toyinf = self.TreeVw.item(viewInfo)
                row = toyinf['values']
                return row[0]
            except:
                pass

    def imgManager(self,event):

        img = Image.open(io.BytesIO(dB.return_image(self.returnValues())))
        x = img.resize((950,500),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(x)

        self.photoLabel.configure(image=img)
        self.photoLabel.image=img


    def delData(self):
        dB.deleteRec([self.returnValues()])
        self.showData()


    def showData(self):
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