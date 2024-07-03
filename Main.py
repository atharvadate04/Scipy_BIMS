from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk 
import tkinter as tk
from tkinter.messagebox import askyesno 
class IMS:
    def __init__(self,main_window):
        self.main_window = main_window
        self.main_window.geometry("1380x700+0+0")
        self.main_window.title("Scipy Bills and Inventory Management")
        self.main_window.iconbitmap("Dmart .ico")
        self.main_window.configure(bg="#BEE9E8")
        self.titleIcon = PhotoImage(file="SciPy.png")



        def show_frame1():
            adminFrame.tkraise() 

        def show_frame2():
            dashBoardFrame.tkraise()     

        #=====================================TITILE==================================

        self.mainTitle = Label(self.main_window,text="SciPy Bills and Inventory Management",font=("times new roman",40,"bold"),bg="#1B4965",fg="#CAE9FF",image=self.titleIcon,compound=LEFT,padx=30).place(x=0,y=0,relwidth=1,height=70)
        
        #====================================Left-Menu================================


        mainLeftMenuO = Frame(self.main_window,bd=2,relief=RIDGE,bg="#5FA8D3")
        mainLeftMenuO.place(x=5,y=75,width=200,height=620)

        mainLeftMenuI = Frame(self.main_window,bd=1,relief=RIDGE,bg="#CAE9FF")
        mainLeftMenuI.place(x=7,y=77,width=199,height=619)
        
        #===================================MENU BUTTONS==============================

        menuList = Label(mainLeftMenuI,text="MENU",font=("Arial",20,"bold"),bg="#1B4965",fg="#CAE9FF",relief=RAISED,pady=12).pack(side=TOP,fill=X)

        spacer = Frame(mainLeftMenuI, height=16, bg="#CAE9FF")
        spacer.pack(side=TOP,fill=X)

        adminBtn = Button(mainLeftMenuI,text="Admin Panel",font=("Monospace",15,"bold"),bg="#5FA8D3",fg="#1B4965",cursor="hand2",bd=3,relief=RAISED,command=show_frame1).pack(side=TOP,fill=X)


        #==========================creation of Admin Frame =============================

        adminFrame = Frame(main_window,bd=2,relief=RIDGE)
        adminFrame.place(x=210,y=75,width=1165,height=620)

        spacer = Frame(mainLeftMenuI, height=10, bg="#CAE9FF")
        spacer.pack(side=TOP,fill=X)

        dashBoardBtn = Button(mainLeftMenuI,text="DashBoard",font=("Monospace",15,"bold"),bg="#5FA8D3",fg="#1B4965",cursor="hand2",bd=3,relief=RAISED,command=show_frame2).pack(side=TOP,fill=X)


        #=====================creation of DashBoard Frame ================================

        dashBoardFrame = Frame(main_window,bd=2,relief=RIDGE)
        dashBoardFrame.place(x=210,y=75,width=1165,height=620)

        #===================================ADMIN PANEL WORK ============================

        productPanel = Frame(adminFrame,bd=3,relief=RIDGE)
        productPanel.place(x=5,y=5,width=390,height=607)

        #prdTitle = Product panel Title
        prdTitle = Label(productPanel,text="-------- Product Panel --------",font=("Arial",15,"bold"),pady=7).pack()

        prdName = Label(productPanel,text="Name :",font=("Arial",11,"bold")).place(x=20,y=80)
        nameBox = tk.Entry(productPanel,width=25,bd=1,validate=None,relief=SOLID,font=("Arial",12)).place(x=120,y=80,height=25)

        prdId = Label(productPanel,text="ID :",font=("Arial",11,"bold")).place(x=20,y=140)
        idBox = tk.Entry(productPanel,width=25,bd=1,relief=SOLID,font=("Arial",12)).place(x=120,y=140,height=25)


        prdPrice = Label(productPanel,text="Price :",font=("Arial",11,"bold")).place(x=20,y=200)
        priceBox = tk.Entry(productPanel,width=25,bd=1,validate=None,relief=SOLID,font=("Arial",12)).place(x=120,y=200,height=25)


        prdQuantity = Label(productPanel,text="Quantity :",font=("Arial",11,"bold")).place(x=20,y=260)
        quantityBox = tk.Entry(productPanel,width=25,bd=1,validate=None,relief=SOLID,font=("Arial",12)).place(x=120,y=260,height=25)

        addBtn = Button(productPanel,text="ADD",width=8,height=2,relief=RAISED,bg="#1B4965",fg="white",font=("Arial",11,"bold")).place(x=30,y=420)
        updateBtn = Button(productPanel,text="UPDATE",width=8,height=2,relief=RAISED,bg="#1B4965",fg="white",font=("Arial",11,"bold")).place(x=150,y=420)
        deleteBtn = Button(productPanel,text="DELETE",width=8,height=2,relief=RAISED,bg="#1B4965",fg="white",font=("Arial",11,"bold")).place(x=270,y=420)



        productTable = Frame(adminFrame,bd=3,relief=RIDGE)
        productTable.place(x=409,y=5,width=737,height=607)



        prdTableTitle = Label(productTable,text="-------- Products Table --------",font=("Arial",15,"bold"),pady=7).pack()
        












        #==================DASH BOARD PANEL ===========================================

        #==========product================
        pSelectFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE)
        pSelectFrame.place(x=5,y=5,width=430,height=607)
        l1 = Label(pSelectFrame,text="PRODUCT LIST",bg="#5FA8D3",fg="#CAE9FF",font=("Arial",16,"bold"),height=2,relief=RAISED).pack(side=TOP,fill=X)


        #=============calculator==========
        calciFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE)
        calciFrame.place(x=440,y=5,width=290,height=290)

        l1 = Label(calciFrame,text="CALCULATOR",bg="#5FA8D3",fg="#CAE9FF",font=("Arial",16,"bold"),height=2,relief=RAISED).pack(side=TOP,fill=X)




        #===========money==================
        moneyFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE)
        moneyFrame.place(x=440,y=300,width=290,height=310)
        l1 = Label(moneyFrame,text="OPTIONS",bg="#5FA8D3",fg="#CAE9FF",font=("Arial",16,"bold"),height=2,relief=RAISED).pack(side=TOP,fill=X)

        #============bill==============
        billFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE)
        billFrame.place(x=735,y=5,width=420,height=570)









    
main_window = Tk()
mainObj=IMS(main_window)


main_window.mainloop()
