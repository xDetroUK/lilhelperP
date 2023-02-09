
from io import BytesIO

try:
    import PIL,os,io,sqlite3
except ImportError:
    import pip

    pip.main(['install', '--user', 'PIL','os','io','sqlite3'])
    import PIL,os,io,sqlite3

import tkinter as tk
from PIL import ImageTk, ImageGrab
con = sqlite3.connect("HelperDatabase.db")
cur = con.cursor()
con.execute('CREATE TABLE IF NOT EXISTS functionINFpython (id INTEGER PRIMARY KEY,functionUse TEXT,FunctionDescription TEXT, FunctionExample TEXT, FunctionImg TEXT )')
con.commit()



def addFunctionInf(FunctionUse,FunctionDescription,FunctionExample,FunctionPhoto):
        cur.execute("INSERT INTO functionINFpython VALUES (NULL,?,?,?,?)",(FunctionUse,FunctionDescription,FunctionExample,FunctionPhoto))
        con.commit()

def showData():
        cur.execute("SELECT * FROM functionINFpython")
        rows=cur.fetchall()
        return rows


def deleteRec(id):
    cur.execute("DELETE FROM functionINFpython WHERE id=?",(id))
    con.commit()

def searchData(id):
    cur.execute("SELECT * FROM functionINFpython WHERE FunctionDescription LIKE '%s'"%id) ##################### '' LIKE '%s%'"% THE % solves value error
    rows=cur.fetchall()
    return rows

def update_image(id,photo):
    with open(photo,'rb') as f:
        data = f.read()
        cur.execute("UPDATE functionINF SET photo=(?) WHERE id=?",(data,id))
        con.commit()

def dataUpdate(id,functionUse="",FunctionDescription='',FunctionExample="",FunctionImg=""):
    cur.execute("UPDATE functionINF SET functionUse=?,cFunctionDescription=?,FunctionExample = ?,FunctionnImg=? where "
                "id =? ",(functionUse,FunctionDescription,FunctionExample,FunctionImg,id))
    con.commit()


def return_image(id):
    cur.execute("SELECT FunctionImg FROM functionINFpython WHERE id='%s'"%id)
    img = cur.fetchone()
    row = BytesIO(img[0])
    return row.read()

def cropScreenshot():



    scrShot = ImageGrab.grab()

    topx, topy, botx, boty = 0, 0, 0, 0

    def get_mouse_posn(event):
        global topy, topx
        topx, topy = event.x, event.y

    def update_sel_rect(event):
        global topy, topx, botx, boty
        botx, boty = event.x, event.y
        canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.

    def finalImage(event):

        popup = tk.Toplevel()
        popup.geometry('200x200')
        fUse = tk.Entry(popup)
        fDes = tk.Entry(popup)
        fExm = tk.Entry(popup)
        fUse.grid(row=0,column=1)
        fDes.grid(row=1,column=1)
        fExm.grid(row=2,column=1)
        tk.Label(popup,text="Function Use").grid(row=0,column=0)
        tk.Label(popup,text="Function Description").grid(row=1,column=0)
        tk.Label(popup,text="We'll find out").grid(row=2,column=0)
        tk.Button(popup, width=10, text='Add',
                   command=lambda: finaloutput()).grid(row=3)
        popup.grid()

        def finaloutput():
            if not os.path.exists(r"Functions/"):
                os.makedirs(r"Functions/")
            try:
                imggg = scrShot.crop(canvas.coords(rect_id))  # canvas.cords returns the coordinates of the selected area
                # inside the crop function
                imggg.save("Functions/" + fUse.get() + ".png", "PNG")
            finally:
                with open("Functions/"+fUse.get()+".png","rb") as ff:
                    bytimg = ff.read()

                addFunctionInf(fUse.get(),fDes.get(),fExm.get(),bytimg)
                popup.destroy()
                window.destroy()
                canvas.destroy()



    try:
        window = tk.Toplevel()
        img = ImageTk.PhotoImage(scrShot)
        canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                           borderwidth=0, highlightthickness=0)
        canvas.pack(expand=True)
        canvas.img = img  # Keep reference in case this code is put into a function.
        canvas.create_image(0, 0, image=img, anchor=tk.NW)
        # Create selection rectangle (invisible since corner points are equal).
        rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2, 2), fill='', outline='white')

        canvas.bind('<Button-1>', get_mouse_posn) # blind to mouse left click
        canvas.bind('<B1-Motion>', update_sel_rect) # detects the motion of the mouse
        canvas.bind("<ButtonRelease-1>", finalImage) # if left button is released
        window.grid()

    except:
        pass











