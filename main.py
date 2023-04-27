from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox

import socket
import os

root = Tk()
root.title("A-Share")
root.geometry("450x660+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False,False)

def Send():
    window = Toplevel(window)
    window.title("Send")
    window.geometry('450x660+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def select_file():
        global filename
        filename= filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Select Image File',
                                            filetype=(('file_type','*.txt'),('all files','*.*')))
    
    def sender():
        s= socket.socket()
        host=socket.gethostname()
        port=8080
        s.bind((host,port))
        s.listen(1)
        print(host)
        print('writing for any incoming connectons.....')
        conn, addr=s.accept()
        file=open(filename,'rb')
        file_data= file.read(1024)
        conn.send(file_data)
        print("Data has been transmitted successfully..")



def Receive():
    main = Toplevel(root)
    host=socket.gethostname()
    main.title(host)
    main.geometry('450x660+500+200')
    main.configure(bg="#f4fdfe")
    main.resizable(False, False)

    def receiver():
        ID= SenderID.get()
        filename1=incoming_file.get()

        s=socket.socket()
        port=8080
        s.connect((ID,port))
        file=open(filename1,'wb')
        file_data= s.recv(1024)
        file.write(file_data)
        file.close()
        print("File has been received successfully")
    
    def select_file():
        global filename
        filename= filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Select Image File',
                                            filetype=(('file_type','*.txt'),('all files','*.*')))


    #icon
    image_icon1=PhotoImage(file="images/recieve.png")
    main.iconphoto(False, image_icon1)

    Hbackground = PhotoImage(file="images/sss.png")
    Label(main,image=Hbackground).place(x=-2,y=0)

    logo=PhotoImage(file='images/pro.png')
    Label(main,image=logo,bg="#f4fdfe").place(x=80,y=270)

    host=socket.gethostname()
    Label(main,text=f'ID: {host}',font='arial 14',bg='white',fg='black').place(x=170,y=300)

    Label(main,text="Write a message:",font=('arial',10,'bold'),bg="#f4fdfe").place(x=20,y=390)
    incoming_file = Entry(main,width=25,fg="black",border=2,bg='white',font=('arial',15))
    incoming_file.place(x=20,y=420)


    Button(main,text="+ file",width=8,height=1,font='arial 14 bold',bg="#fff",fg="#581845",command=select_file).place(x=310,y=420)
    Button(main,text="SEND",width=8,height=1,font='arial 14 bold',bg="#581845",fg="#fff",command=receiver).place(x=150,y=480)
    

    main.mainloop() 

#icon
image_icon= PhotoImage(file="images/icon.png")
root.iconphoto(False,image_icon)

Label(root, text="Share Your Heart", font=('Acumin Variable Concept',20,'bold'),bg="#f4fdfe").place(x=20,y=30)

Frame(root, width=30, height=2, bg="#f3f5f6").place(x=25,y=80)

receive_image = PhotoImage(file="images/recieve.png")
receive = Button(root, image=receive_image, bg="#f4fdfe",bd=0,command=Receive)
receive.place(x=250, y=100)

#label
Label(root,text="Receive", font=('Acumin Variable Concept',16,'bold'),bg="#f4fdfe").place(x=250,y=170)

background=PhotoImage(file="images/background.png")
Label(root, image=background).place(x=-2, y=300)

root.mainloop()
