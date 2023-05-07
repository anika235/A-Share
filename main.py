from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import threading
import time
import socket
import os
import ipaddress
import struct
from tkinter import ttk

class ListFrame(ttk.Frame):
	def __init__(self, parent, text_data, item_height):
		super().__init__(master = parent)
		self.pack(expand = True, fill = 'both')

		# widget data
		self.text_data = text_data
		self.item_number = len(text_data)
		self.list_height = self.item_number * item_height

		# canvas 
		self.canvas = tk.Canvas(self, background = 'red', scrollregion = (0,0,self.winfo_width(),self.list_height))
		self.canvas.pack(expand = True, fill = 'both')

		# display frame
		self.frame = ttk.Frame(self)
		
		for index, item in enumerate(self.text_data):
			self.create_item(index, item).pack(expand = True, fill = 'both', pady =  4, padx = 10)

		# scrollbar 
		self.scrollbar = ttk.Scrollbar(self, orient = 'vertical', command = self.canvas.yview)
		self.canvas.configure(yscrollcommand = self.scrollbar.set)
		self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')

		# events
		self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
		self.bind('<Configure>', self.update_size)

	def update_size(self, event):
		if self.list_height >= self.winfo_height():
			height = self.list_height
			self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
			self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')
		else:
			height = self.winfo_height()
			self.canvas.unbind_all('<MouseWheel>')
			self.scrollbar.place_forget()
		
		self.canvas.create_window(
			(0,0), 
			window = self.frame, 
			anchor = 'nw', 
			width = self.winfo_width(), 
			height = height)

	def create_item(self, index, item):
		frame = ttk.Frame(self.frame)

		# grid layout
		frame.rowconfigure(0, weight = 1)
		frame.columnconfigure((0,1,2,3,4), weight = 1, uniform = 'a')

		# widgets 
		ttk.Label(frame, text = f'#{index}').grid(row = 0, column = 0)
		ttk.Label(frame, text = f'{item[0]}').grid(row = 0, column = 1)
		ttk.Button(frame, text = f'{item[1]}').grid(row = 0, column = 2, columnspan = 3, sticky = 'nsew')

		return frame


window_list = {}
online_friends = {} #online_friends[name]  = (IP , PORT)
PORT = 8080
HOST_NAME = socket.gethostname()
IP = socket.gethostbyname(HOST_NAME)
BROADCAST_ADDR = str(ipaddress.ip_network(IP + "/24", strict=False).broadcast_address)
print(BROADCAST_ADDR)
ADDR = (IP, PORT)
WINDOW_SIZE = "450x660+500+200"
SIZE = 1024
FORMAT = "utf-8"
is_first_page_on = True

root = Tk()


def make_file_name(file_name):
    
    name , extension = file_name.split(".")
    
    while os.path.exists(name):
        name = f'{name}_{num}'
        num += 1
    return name + "." + extension

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    data = conn.recv(SIZE).decode(FORMAT)
    file_name , file_size = data.split(" ")
    file_size = int(file_size)
    file_name = make_file_name(file_name)
    
    with open(file_name, "w") as f:
        while True:
            data = conn.recv(SIZE).decode(FORMAT)
            if not data:
                break
            f.write(data)
            conn.send("Data received.".encode(FORMAT))
    
    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()
    
def handle_recv():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

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



def Call_Second_Page(name):
    is_first_page_on = False
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry(WINDOW_SIZE)

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    global listbox
    listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    host=socket.gethostname()
    root.title(host)
    root.geometry(WINDOW_SIZE)
    root.configure(bg="#f4fdfe")
    root.resizable(False, False)

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
    root.iconphoto(False, image_icon1)

    Hbackground = PhotoImage(file="images/sss.png")
    Label(root,image=Hbackground).place(x=-2,y=0)

    logo=PhotoImage(file='images/pro.png')
    Label(root,image=logo,bg="#f4fdfe").place(x=80,y=270)

    host=socket.gethostname()
    Label(root,text=f'ID: {host}',font='arial 14',bg='white',fg='black').place(x=170,y=300)

    Label(root,text="Write a message:",font=('arial',10,'bold'),bg="#f4fdfe").place(x=20,y=390)
    incoming_file = Entry(root,width=25,fg="black",border=2,bg='white',font=('arial',15))
    incoming_file.place(x=20,y=420)


    Button(root,text="+ file",width=8,height=1,font='arial 14 bold',bg="#fff",fg="#581845",command=select_file).place(x=310,y=420)
    Button(root,text="SEND",width=8,height=1,font='arial 14 bold',bg="#581845",fg="#fff",command=receiver).place(x=150,y=480)
    Button(root,text="Back",width=8,height=1,font='arial 14 bold',bg="#fff",fg="#581845",command=call_first_page).place(x=310,y=520)

    root.mainloop() 

def broad_cast_your_presence():
    # Broadcast the IP address to all devices on the local network
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        msg = HOST_NAME + " " + IP + " " + str(PORT)
        s.sendto(msg.encode(), (BROADCAST_ADDR, port))
        print("Sent IP address:", msg)

def check_online():
    
    #check who is online
    start_timer = time.time() + 10
    while True:
        if time.time() - start_timer > 5:
            start_timer = time.time()
            broad_cast_your_presence_thread = threading.Thread(target=broad_cast_your_presence)
            broad_cast_your_presence_thread.start()
            #check online   
            
def check_if_any_friend_is_still_online():
    start_time = time.time()
    while True:
        if time.time()-start_time>5:
            start_time = time.time()
            tmp_problem = []
            for friend in online_friends: 
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(online_friends[friend])
                    s.close()
                except:
                    s.close()
                    tmp_problem.append(friend)
            for friend in tmp_problem:
                del online_friends[friend]
            print(online_friends)
            if not is_first_page_on:
                continue
            while listbox.size()>0:
                listbox.delete(0)
            for name in online_friends:
                button_name = name
                button = tk.Button(root, text=button_name, command=lambda name=button_name: Call_Second_Page(name))
                button.pack(padx=10, pady=5)
                listbox.insert(tk.END, button)
        
def check_broadcast_messages():
    
    while True:
        ip_address = "0.0.0.0"  # Listen on all available network interfaces
        port = 12345

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ip_address, port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            # Wait for a message and print it
            print("Waiting for message...")
            while True:
                data, addr = s.recvfrom(1024)
                message = data.decode()
                tmp_name , tmp_ip , tmp_port = message.split(" ")
                online_friends[tmp_name] = (tmp_ip , int(tmp_port))
                print("Received message from {}: {}".format(addr, message))
                

def call_first_page():
    
    is_first_page_on = True
    
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("A-Share")
    root.geometry(WINDOW_SIZE)
    root.configure(bg="#f4fdfe")
    root.resizable(False,False)
    #icon
    image_icon= PhotoImage(file="images/icon.png")
    root.iconphoto(False,image_icon)

    Label(root, text="Share Your Heart", font=('Acumin Variable Concept',20,'bold'),bg="#f4fdfe").place(x=20,y=400)

    Frame(root, width=30, height=2, bg="#f3f5f6").place(x=25,y=80)

    # receive_image = PhotoImage(file="images/recieve.png")
    # receive = Button(root, image=receive_image, bg="#f4fdfe",bd=0,command=Receive)
    # receive.place(x=250, y=100)

    #label
    # Label(root,text="Receive", font=('Acumin Variable Concept',16,'bold'),bg="#f4fdfe").place(x=250,y=170)

    background=PhotoImage(file="images/background.png")
    Label(root, image=background).place(x=-2, y=300)
    text_list = [('label', 'button'),('thing', 'click'),('third', 'something'),('label1', 'button'),('label2', 'button'),('label3', 'button'),('label4', 'button')]
    list_frame = ListFrame(root, text_list, 100)
    list_frame.pack(side='left', fill='x', expand=True , anchor='nw')
    root.mainloop()    

def main():
    
    check_online_thread = threading.Thread(target=check_online)
    check_online_thread.start()
    
    check_broadcast_messages_thread = threading.Thread(target=check_broadcast_messages)
    check_broadcast_messages_thread.start()
    
    check_if_any_friend_is_still_online_thread = threading.Thread(target=check_if_any_friend_is_still_online)
    check_if_any_friend_is_still_online_thread.start()
    
    call_first_page()
    

if __name__ == "__main__":
    main()