from tkinter import *

root = Tk()
root.title("A-Share")
root.geometry("450x660+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False,False)
#icon
image_icon= PhotoImage(file="images/icon.png")
root.iconphoto(False,image_icon)

Label(root, text="Share Your Heart", font=('Acumin Variable Concept',20,'bold'),bg="#f4fdfe").place(x=20,y=30)

Frame(root, width=30, height=2, bg="#f3f5f6").place(x=25,y=80)

receive_image = PhotoImage(file="images/recieve.png")
receive = Button(root, image=receive_image, bg="#f4fdfe",bd=0)
# receive.place(x=250, y=100)

#label
Label(root,text="Receive", font=('Acumin Variable Concept',16,'bold'),bg="#f4fdfe").place(x=250,y=170)

background=PhotoImage(file="images/background.png")
Label(root, image=background).place(x=-2, y=300)

root.mainloop()
