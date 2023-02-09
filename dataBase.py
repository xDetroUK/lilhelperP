

try:
    import PIL, sqlite3, webbrowser, easyocr, requests, folium, pyautogui, pyttsx3, os, speech_recognition
    from io import BytesIO
    from PIL import Image
    from pytube import YouTube
    from screen_recorder_sdk import screen_recorder
    import tkinter as tk
    from tkinter import ttk,filedialog
    from PIL import ImageTk, ImageGrab
    from cryptography.fernet import Fernet

except ImportError:

    import pip

    pip.main(['install', '--user', 'Pillow', 'webbrowser', 'easyocr', 'requests', 'folium', 'pyautogui', 'pytube',
              "SpeechRecognition"
              'screen_recorder_sdk', 'pyttsx3',"cryptography"])
    import PIL, sqlite3, webbrowser, easyocr, requests, folium, pyautogui, pyttsx3, os
    from io import BytesIO
    from PIL import Image
    from pytube import YouTube
    from screen_recorder_sdk import screen_recorder
    from cryptography.fernet import Fernet
    import tkinter as tk
    from tkinter import ttk,filedialog
    from PIL import ImageTk, ImageGrab

if not os.path.exists(r"Functions/"):
    os.makedirs(r"Functions/")

if not os.path.exists(r"Screenshots/"):
    os.makedirs(r"Screenshots/")

if not os.path.exists(r"Screenrecordings/"):
    os.makedirs(r"Screenrecordings/")

if not os.path.exists(r"imgtotext/"):
    os.makedirs(r"imgtotext/")

if not os.path.exists(r"maps/"):
    os.makedirs(r"maps/")

if not os.path.exists(r"keys/"):
    os.makedirs(r"keys/")

if not os.path.exists(r"YT/"):
    os.makedirs(r"YT/")

if not os.path.exists(r"Chess/"):
    os.makedirs(r"Chess/")

if not os.path.exists(r"txttospeech/"):
    os.makedirs(r"txttospeech/")

con = sqlite3.connect("HelperDatabase.db")
cur = con.cursor()
con.execute(
    'CREATE TABLE IF NOT EXISTS functionINFpython (id INTEGER PRIMARY KEY,functionUse TEXT,FunctionDescription TEXT, '
    'FunctionExample TEXT, FunctionImg TEXT )')
con.commit()


def addFunctionInf(FunctionUse, FunctionDescription, FunctionExample, FunctionPhoto):
    cur.execute("INSERT INTO functionINFpython VALUES (NULL,?,?,?,?,?)",
                (FunctionUse, FunctionDescription, FunctionExample, FunctionPhoto, ''))
    con.commit()


def showData():
    cur.execute("SELECT * FROM functionINFpython")
    rows = cur.fetchall()
    return rows


def deleteRec(idd):
    cur.execute("DELETE FROM functionINFpython WHERE id=?", idd)
    con.commit()


def searchData(idd):
    cur.execute(
        "SELECT * FROM functionINFpython WHERE FunctionUse LIKE '%s'" % idd)
    rows = cur.fetchall()
    return rows


def dataUpdate(idd, functionUse="", FunctionDescription='', FunctionExample="", FunctionCode=''):
    cur.execute(
        "UPDATE functionINFpython SET functionUse=?,FunctionDescription=?,FunctionExample = ?,FunctionCode=? where id "
        "=? ",
        (functionUse, FunctionDescription, FunctionExample, FunctionCode, idd))
    con.commit()


def returnCode(idd):
    # cur.execute("ALTER TABLE functionINFpython ADD FunctionCode TEXT")
    cur.execute("SELECT FunctionCode FROM functionINFpython WHERE id='%s'" % idd)
    row = cur.fetchall()
    return row


def return_image(idd):
    cur.execute("SELECT FunctionImg FROM functionINFpython WHERE id='%s'" % idd)
    img = cur.fetchone()
    row = BytesIO(img[0])
    return row.read()


def cropScreenshot(mode=''):
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
        fUse = tk.Entry(popup)
        fDes = tk.Entry(popup)
        fExm = tk.Entry(popup)
        fUse.grid(row=0, column=1)
        fDes.grid(row=1, column=1)
        fExm.grid(row=2, column=1)
        tk.Label(popup, text="Name").grid(row=0, column=0)
        tk.Label(popup, text="Function Description").grid(row=1, column=0)
        tk.Label(popup, text="We'll find out").grid(row=2, column=0)
        tk.Button(popup, width=10, text='Add', command=lambda: finaloutput()).grid(row=3)
        popup.grid()

        def finaloutput():

            if mode == 'Database':
                imggg = scrShot.crop(
                    canvas.coords([rect_id]))  # canvas.cords returns the coordinates of the selected area
                # inside the crop function
                imggg.save("Functions/" + fUse.get() + ".png", "PNG")

                with open("Functions/" + fUse.get() + ".png", "rb") as ff:
                    bytimg = ff.read()

                addFunctionInf(fUse.get(), fDes.get(), fExm.get(), bytimg)
                popup.destroy()
                window.destroy()
                canvas.destroy()

            if mode == 'ScrShot':
                imggg = scrShot.crop(
                    canvas.coords([rect_id]))  # canvas.cords returns the coordinates of the selected area
                # inside the crop function
                imggg.save("Screenshots/" + fUse.get() + ".png", "PNG")
                window.destroy()
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

        canvas.bind('<Button-1>', get_mouse_posn)  # blind to mouse left click
        canvas.bind('<B1-Motion>', update_sel_rect)  # detects the motion of the mouse
        canvas.bind("<ButtonRelease-1>", finalImage)  # if left button is released
        window.grid()

    except:
        pass

def ImageTotext():
    scrShot = ImageGrab.grab()
    topx, topy, botx, boty = 0, 0, 0, 0

    def get_mouse_posn(event):
        global topy, topx
        topx, topy = event.x, event.y

    def update_sel_rect(event):
        global topy, topx, botx, boty
        botx, boty = event.x, event.y
        canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.

    def imgtospeech(txt):

        engine = pyttsx3.init()
        engine.say(txt)
        engine.runAndWait()


    def ExtractText(event):

        imggg = scrShot.crop(canvas.coords([rect_id]))
        imggg.save("imgtotext/testbrat.png")
        window.destroy()
        canvas.destroy()
        finalResult = tk.Toplevel()

        reader = easyocr.Reader(['en'])
        results = reader.readtext("imgtotext/testbrat.png", paragraph=False)
        text = ''
        for result in results:
            text += result[1] + ''

        SelText = tk.Text(finalResult, height=20, width=100)
        tk.Button(finalResult, command=lambda: imgtospeech(text), text='Text to speech').grid()
        SelText.insert(tk.END, text)
        SelText.grid()
        print(text)

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
        canvas.bind('<Button-1>', get_mouse_posn)  # blind to mouse left click
        canvas.bind('<B1-Motion>', update_sel_rect)  # detects the motion of the mouse
        canvas.bind("<ButtonRelease-1>", ExtractText)  # if left button is released
        window.grid()
    except:
        pass


def downWebmPortable():
    d = tk.Toplevel()
    d.grid()
    x = tk.Entry(d)
    x.grid()
    current_var = tk.StringVar()
    combobox = ttk.Combobox(d, textvariable=current_var)
    combobox["values"] = ('Video', 'Audio')
    combobox.grid()

    def downSong():
        yt = YouTube(x.get())
        if combobox.get() == 'Audio':
            stream = yt.streams.get_by_itag(251)
            stream.download('YT/')

        elif combobox.get() == 'Video':
            vstream = yt.streams.get_highest_resolution()
            vstream.download('YT/')

    tk.Button(d, text='Submit', command=downSong).grid()


def targetLongLat(curIP=''):
    try:

        response = requests.post("http://ip-api.com/batch", json=[
            {"query": curIP}]).json()

        lon = response[0]['lon']
        lat = response[0]['lat']

        m = folium.Map(location=[lat, lon])

        xd = tk.Toplevel()
        TreeVwTwo = ttk.Treeview(xd, columns=('Info', 'Data'), show='headings', height=5)

        for g in response:
            for f in g.items():
                TreeVwTwo.insert(parent='', index='end', text='Parent Shit', values=f)

        folium.Marker([lat, lon],
                      popup='<strong>Location One</strong>').add_to(m)

        m.save('maps/map.html')
        webbrowser.open('maps/map.html')
        TreeVwTwo.grid()
        TreeVwTwo.heading('1', text='Data')
        TreeVwTwo.heading('2', text='Information')


    except:
        pass


def scrnRecorder():
    try:
        mwin = tk.Toplevel()
        # screen_recorder.get_screenshot(15).save('test_before.png')
        oky = "30", "60", "120"
        cb1 = ttk.Combobox(mwin, values=oky, width=7)
        filname = tk.Entry(mwin, width=20)

        def closFunc():
            screen_recorder.stop_video_recording()
            screen_recorder.free_resources()
            mwin.destroy()

        def recScrn(fps, name):
            screen_recorder.enable_dev_log()
            params = screen_recorder.RecorderParams()
            # params.pid = 0 # use it to set process Id to capture
            # params.desktop_num = 0 # use it to set desktop num, counting from 0
            screen_recorder.init_resources(params)
            xxx = int(fps)
            screen_recorder.start_video_recording("Screenrecordings/" + name + '.mp4', xxx, 8000000, True)

        filname.grid(row=0, column=1)
        cb1.grid(row=0, column=0)
        tk.Button(mwin, text='Start', command=lambda: recScrn(cb1.get(), filname.get())).grid(row=1, column=0)
        tk.Button(mwin, text='Stop', command=closFunc).grid(row=1, column=1)
        mwin.grid()
        mwin.mainloop()

    except:
        print("")


def chessHelper():
    chessWin = tk.Toplevel()
    chessImg = tk.Label(chessWin, image='')
    chessStyle = tk.Label(chessWin, text='hi')
    chessStyle.grid(row=0, column=0)
    chessImg.grid(row=1, column=0)
    ckd = True
    gambitImg = Image.open("Chess/Stafford.png")
    fim = ImageTk.PhotoImage(gambitImg)
    chessWin.grid()
    while ckd:
        chessboard = pyautogui.locateOnScreen("Chess/Stafford.png")

        if chessboard:
            chessImg.configure(image=fim)
            print('Hi')
        else:
            print('pass')


def filencrypter(file,mode=''):
    key = Fernet.generate_key()
    filepath = os.path.abspath(file.name)
    filname = os.path.basename(filepath)

    print(key, '\n', file, '\n', filepath,'\n')

    if file and mode == 'Encrypt':
        try:
            with open("keys/"+filname+".key", "wb") as deckey:
                deckey.write(key)
            with open(filepath ,'rb') as thefile:
                contents = thefile.read()
            enccontent = Fernet(key).encrypt(contents)

            with open(filepath,"wb") as thefile:
                thefile.write(enccontent)
        except:
            pass

    elif mode =="Decrypt":

        try:
            with open("keys/"+filname+".key", "rb") as bs:
                x = bs.read()
            with open(filepath,'rb')as thefile:
                contentss = thefile.read()
            contdec = Fernet(x).decrypt(contentss)
            with open(filepath,'wb') as thefile:
                thefile.write(contdec)
        except:
            pass
    else:
        print("Shit")

