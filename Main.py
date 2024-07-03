from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk 
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
        productPanel.place(x=5,y=5,width=450,height=607)

        #prdTitle = Product panel Title
        prdTitle = Label(productPanel,text="-------- Product Panel --------",font=("Arial",15,"bold"),pady=7).pack()

        prdName = Label(productPanel,text="Name :",font=("Arial",11,"bold")).place(x=20,y=80)
        nameBox = ttk.Entry(productPanel,width=50).place(x=90,y=80)

        prdId = Label(productPanel,text="ID :",font=("Arial",11,"bold")).place(x=20,y=140)
        prdPrice = Label(productPanel,text="Price :",font=("Arial",11,"bold")).place(x=20,y=200)
        prdQuantity = Label(productPanel,text="Quantity :",font=("Arial",11,"bold")).place(x=20,y=260)




        productTable = Frame(adminFrame,bd=3,relief=RIDGE)
        productTable.place(x=459,y=5,width=697,height=607)



        prdTableTitle = Label(productTable,text="-------- Products Table --------",font=("Arial",15,"bold"),pady=7).pack()













        #==================DASH BOARD PANEL ===========================================

        l1dash = Label(dashBoardFrame,text="DASHBOARD AREA",font=("Arial",40,"bold")).pack();








    
main_window = Tk()
mainObj=IMS(main_window)


main_window.mainloop()