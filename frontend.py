from tkinter import *
import login
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import os.path
import customtkinter as tk
import backend

tk.set_appearance_mode("dark")
tk.set_default_color_theme("green")

root = tk.CTk()
root.geometry("1024x600")
root.minsize(1024,600)
LARGE_FONT= ("Verdana", 28)
BUTTON_FONT=("Verdana", 20)

user=""
logged = False
username="kartik"
password=""

class FrontEnd(tk.CTk):

    def __init__(self, *args, **kwargs):
        
        tk.CTk.__init__(self, *args, **kwargs)
        container = tk.CTkFrame(self)
       
        container.pack(pady = 0, padx = 0, fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, LoginPage, SignUp, Menu, Preparation):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.CTkFrame):

    def __init__(self, parent, controller):
        tk.CTkFrame.__init__(self,parent,width=1024,height=600)
        label = tk.CTkLabel(self, text = "Welcome", font = LARGE_FONT)
        label.place(x =  470, y = 200 , in_ = self)

        button1 = tk.CTkButton(self, text="Login",  
            command=lambda: controller.show_frame(LoginPage),font = BUTTON_FONT)
        button1.place(x =  470, y = 250 , in_ = self)

        button2 = tk.CTkButton(self, text="Enter as guest", 
            command=lambda: controller.show_frame(Menu),font = BUTTON_FONT)
        
        button3 = tk.CTkButton(self, text="Sign Up", 
            command=lambda: controller.show_frame(SignUp),font = BUTTON_FONT)

        button2.place(x =  460, y = 300 , in_ = self)
        button3.place(x =  470, y = 350 , in_ = self)
        

class LoginPage(tk.CTkFrame):
   
    def __init__(self, parent, controller):
        tk.CTkFrame.__init__(self, parent,width=1024,height=600)
        label1 = tk.CTkLabel(self, text="Login", font = LARGE_FONT)
        label1.place(x =  470, y = 100 , in_ = self)

        label2 = tk.CTkLabel(self,text="", font = LARGE_FONT)
        label2.place(x =  470, y = 150 , in_ = self)
        
        entry1 = tk.CTkEntry(self, placeholder_text = "Username",font = BUTTON_FONT)
        entry1.place(x =  470, y = 200 , in_ = self)

        entry2 = tk.CTkEntry(self, placeholder_text = "Password",show = "*",font = BUTTON_FONT)
        entry2.place(x =  470, y = 250 , in_ = self)

        button2 = tk.CTkButton(self, text="Enter as guest", command=lambda: controller.show_frame(StartPage),font = BUTTON_FONT)
        button3 = tk.CTkButton(self, text="Sign Up", command=lambda: controller.show_frame(SignUp),font = BUTTON_FONT)
        
        button2.place(x =  460, y = 300 , in_ = self)
        button3.place(x =  470, y = 350 , in_ = self)
        button1 = tk.CTkButton(self, text="Login", command=lambda: self.get_response(entry1.get(), entry2.get(), label2, controller, entry1, entry2),font = BUTTON_FONT)
        button1.place(x =  470, y = 400 , in_ = self)
    
    def get_response(self,usr:str,passw:str,lbl,controller,entry1, entry2):
        global username
        global logged
        self.usr=usr
        self.passw=passw
        self.lbl=lbl
        self.entry1 = entry1
        self.entry2 = entry2
        status = login.login(self.usr,self.passw)
        if(status==0):
            self.lbl.configure(text="Required: Username or Password")
            self.lbl.configure(text_color="Red")
        elif(status==1):
            self.lbl.configure(text="Username or Password is Wrong")
            self.lbl.configure(text_color="Red")
            self.entry2.delete(0, END)
        else:
            self.lbl.configure(text="Login successful")
            self.lbl.configure(text_color="Green")
            self.entry2.delete(0, END)
            self.entry1.delete(0, END)
            logged = True
            username = self.usr
            controller.after(3000, controller.show_frame, Menu)

class Menu(tk.CTkFrame):

    drink_name=["Lychee", "Soda", "Pepsi", "Pomegranate"]
    
    drink_number=1
    
    order=0

    def previous(prev_drinks):
        
        prev_drink = []
        for drink in prev_drinks[0]:
            prev_drink.append(drink)
        return prev_drink
    
    

    def __init__(self, parent, controller):
        # previous_drinks = Menu.previous(login.prev_drink(username)) 
        # print(previous_drinks)
        tk.CTkFrame.__init__(self,parent,width=1024,height=600)
        tabview = tk.CTkTabview(self,width=1024,height=600) #,state = "disabled")
        tabview.place(x =  0, y = 0 , in_ = self)
        #pack(pady=10,padx=10)

        #################################  TAB---1  ################################

        tab_1 = tabview.add("Menu")
        tab_2 = tabview.add("Prev")
        if(logged == True):
            print(login.prev_drink(username))
            tab_2.pack_forget()
        tabview.set("Menu")

        drink_name = tk.CTkLabel(self, text = str(Menu.drink_name[0]), font=LARGE_FONT)
        drink_name.place(x =  460, y = 100 ,in_= tab_1)
        
        back_button = tk.CTkButton(self, text = "<", font = BUTTON_FONT, state = "disabled", command=lambda: self.previous_drink(drink_name, back_button, forward_button), width=40, height=20)
        exit_button = tk.CTkButton(self, text = "Exit",font = BUTTON_FONT, width=100, height=30, command=lambda: self.exit(controller))

        var = IntVar()
        R1 = tk.CTkRadioButton(self, text="Soda", variable=var, value=2,font = BUTTON_FONT)
        R1.place(x =  460, y = 150 , in_=tab_1)

        R2 = tk.CTkRadioButton(self, text="Pepsi", variable=var, value=3,  font = BUTTON_FONT)
        R2.place(x =  460, y = 200 , in_=tab_1)

        R3 = tk.CTkRadioButton(self, text="Soda+Pepsi", variable=var, value=0,font = BUTTON_FONT)
        R3.place(x =  460, y = 250 , in_=tab_1)

        forward_button = tk.CTkButton(self, text = ">",font = BUTTON_FONT, command=lambda: self.next_drink(forward_button, back_button, drink_name),width=40,height=20)
        button7 = tk.CTkButton(self, text = "Order",command=lambda: self.Order(controller, var.get(), labl) ,font = BUTTON_FONT, width=100, height=30)
        button7.place(x =  460, y = 350 , in_ = tab_1)
        
        # button positioning
        back_button.place(x =  400, y = 350 , in_ = tab_1)
        exit_button.place(x =  460, y = 400 , in_ = tab_1)
        forward_button.place(x = 580 , y = 350 , in_ = tab_1) 

        labl = tk.CTkLabel(self, font = LARGE_FONT, text = "")
        labl.place(x =  320, y = 300 ,in_ = tab_1)


    def Order(self , controller, var, lbl):
        self.controller = controller
        self.lbl = lbl

        print(var)
        order = [0,0]
        order[0] = Menu.drink_number
        if(order[0] == 3):
            order[0] = 4
        elif(order[0] == 4):
            order[0]=5

        if(var == 0 ):
            self.lbl.configure(text="Select a mixer for you drink")
            self.lbl.configure(text_color="Red")
        else:

            if(var == 2):
                order[1] = 2
            elif(var == 3):
                order[1] = 3
            elif(var == 0):
                order[1] = 0
            
            print(order)
            backend.order(order)
            time.sleep(2)

            self.controller.show_frame(Preparation)

            self.controller.after(5000, self.controller.show_frame, StartPage)
    
    def exit(self,controller):
        self.controller = controller
        self.controller.show_frame(StartPage)

    def next_drink(self, button,button1,lbl1):
        self.button1 = button1
        self.button = button
        self.button1.configure(state="enabled")
        Menu.drink_number=Menu.drink_number+1
        self.lbl1 = lbl1
        self.lbl1.configure(text=Menu.drink_name[Menu.drink_number])
        
        if(Menu.drink_number==Menu.drink_name.__len__()-1):
            self.button.configure(state="disabled")
        
    
    def previous_drink(self,lbl1,button, button1):
        self.button1 = button1
        self.button1.configure(state="enabled")
        Menu.drink_number=Menu.drink_number-1
        self.lbl1 = lbl1
        self.lbl1.configure(text=str(Menu.drink_name[Menu.drink_number]))
        self.button = button
        
        if(Menu.drink_number==0):
            self.button.configure(state="disabled")
       



   

class Preparation(tk.CTkFrame):

    def __init__(self, parent, controller):
        tk.CTkFrame.__init__(self, parent,width=1024,height=600)    
        labl1 = tk.CTkLabel(self, text = "You order is being prepared", font=LARGE_FONT)
        labl1.place(x =  330, y = 270 ,in_ = self)
        #pack(pady=10, padx=10)

        labl1 = tk.CTkLabel(self, text="Order: " + str(Menu.drink_name[Menu.order]), font=LARGE_FONT)
        

class SignUp(tk.CTkFrame):

    def __init__(self, parent, controller):
        tk.CTkFrame.__init__(self, parent,width=1024,height=600)
        label1 = tk.CTkLabel(self, text="Sign Up", font = LARGE_FONT)
        label1.place(x =  460, y = 100 ,in_= self)
        #pack(pady=10,padx=10)

        label2 = tk.CTkLabel(self,text="", font = LARGE_FONT)
        label2.place(x =  460, y = 150 ,in_= self)

        entry1 = tk.CTkEntry(self, placeholder_text = "Username", font = BUTTON_FONT)
        entry1.place(x =  460, y = 200 ,in_= self)

        entry2 = tk.CTkEntry(self, placeholder_text = "Password",show = "*", font = BUTTON_FONT)
        entry2.place(x =  460, y = 250 ,in_= self)

        entry3 = tk.CTkEntry(self, placeholder_text = "Confirm Password",show = "*", font = BUTTON_FONT)
        entry3.place(x =  460, y = 300 ,in_= self)

        button1 = tk.CTkButton(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage), font = BUTTON_FONT)
        button1.place(x =  450, y = 350 ,in_= self)

        button2 = tk.CTkButton(self, text="Sign Up",
                            command=lambda: self.get_response(entry1.get(), entry2.get(), entry3.get(), label2,parent,controller, entry1, entry2, entry3), font = BUTTON_FONT)
        button2.place(x =  460, y = 400 ,in_= self)
    

    def get_response(self,usr:str,passw:str,conpas:str,lbl,parent,controller,entry1,entry2,entry3):
        self.usr=usr
        self.passw=passw
        self.lbl=lbl
        self.conpas=conpas
        self.entry1 = entry1
        self.entry2 = entry2
        self.entry3 = entry3
        status = login.signUp(self.usr,self.passw,self.conpas)
        if(status==0):
            self.lbl.configure(text="Required: All fields")
            self.lbl.configure(text_color="Red")
        elif(status==1):
            print(passw)
            print(conpas)
            self.lbl.configure(text="Confirm Password and Password: Fields must match")
            self.lbl.configure(text_color="Red")
            self.entry3.delete(0, END)
        elif(status==2):
            self.lbl.configure(text="User Already exists")
            self.lbl.configure(text_color="Black")
            self.entry3.delete(0, END)
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)

        else:
            self.lbl.configure(text="Signed Up successfully")
            self.lbl.configure(text_color="Green")
            
            controller.after(2000, controller.show_frame, Menu)
            
            
app = FrontEnd()
app.mainloop()
