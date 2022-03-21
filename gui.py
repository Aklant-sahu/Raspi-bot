#Creating GUI with tkinter
import tkinter
from tkinter import *
from bot import chatbot_response,displaycsv,room_func
from PIL import ImageTk, Image
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pyttsx3
lemmatizer = WordNetLemmatizer()
engine = pyttsx3.init()  
voices = engine. getProperty('voices')
engine.setProperty("rate", 140)
engine.setProperty('voice', voices[1].id)  

################################ 


def get_div(msg_lst,msg):
    for i in msg_lst:
        if i[0]== 'd':            
            return i.upper()
    else:
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        print('Please also provide division')
        ChatLog.insert(END, "Bot: " + 'Div Not found' + '\n\n')

def timetable(div):
    div = div.upper()
    win = tkinter.Toplevel()
    win.geometry("400x400")
    p1 = PhotoImage(file = 'veslogo.png')
    win.iconphoto(False, p1)
    win.title(f"TimeTable of DIV {div}")
    img = ImageTk.PhotoImage(Image.open(f'Timetable/{div}.jpg'))
    Label(win,image = img).pack()
    print("TimeTable")
    win.mainloop()

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    msg_lst = word_tokenize(msg)
    msg_lst = [i.lower() for i in msg_lst]
    # msg_lst = [lemmatizer.lemmatize(word.lower()) for word in msg_lst]
    print(msg_lst)
    EntryBox.delete("0.0",END)
    df = displaycsv()
    res = chatbot_response(msg)
    engine.say(res)   
    engine.runAndWait()
    ChatLog.config(state=NORMAL)
    

    if "Timetable".lower() in msg_lst:

        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        # ChatLog.insert(END, "You: " + msg + '\n\n')
        # ChatLog.insert(END, "You: " + msg + '\n\n')
        timetable(get_div(msg_lst,msg))
    
    if res == "Room_func":
        room,flag = room_func(msg,df)
        print(room,flag)
        # ChatLog.config(state=NORMAL)
        if flag == True:
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.insert(END, "Bot: " + room + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        elif flag == False:
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.insert(END, "Bot: " +"Oops !!This professor name is not present in this department\nBelow is the list of Professors:"+ '\n\n')
            ChatLog.insert(END,df["Professors"])
            ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        
    elif msg != " ":
        # ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        # print("LALALALALALALALAaaaaaa")
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        # res = chatbot_response(msg)
        print(res)
        if res == "PROF_CSV":
                ChatLog.insert(END,df)
        else:
            ChatLog.insert(END, "Bot: " + res + '\n\n')
            # print("ABRACADABRA")


        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


root = Tk()
root.title("Enquiry-Bot")
root.geometry("600x500")
root.resizable(False, False)
p1 = PhotoImage(file = 'static/timetable/veslogo.png')
# p2 = ImageTk.PhotoImage(Image.open('Timetable/D16B.jpg'))
# label = Label(root,image = p2)
root.iconphoto(False, p1)
root.resizable(width=True, height=FALSE)

#Create Chat window
ChatLog = Text(root, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(root, command=ChatLog.yview, cursor="heart")
# scrollbar = Scrollbar(root, command=p2.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
# p2['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(root, font=("Verdana",12,'bold'), text="Send", width="12", height=2,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(root, bd=0, bg="white",width="29", height="2", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
# label.place(x=600,y=6,height=570)
# scrollbar.place(x=1252,y=6, height=570)
scrollbar.place(x=576,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=570)
EntryBox.place(x=128, y=401, height=90, width=465)
SendButton.place(x=6, y=401, height=90)

root.mainloop()