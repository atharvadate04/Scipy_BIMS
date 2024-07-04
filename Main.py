from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk 
import tkinter as tk
from tkinter.messagebox import askyesno 
import sqlite3 as sql
from tkinter import messagebox


class IMS:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.geometry("1380x700+0+0")
        self.main_window.title("Scipy Bills and Inventory Management")
        self.main_window.iconbitmap("Dmart .ico")
        self.main_window.configure(bg="#BEE9E8")
        self.titleIcon = PhotoImage(file="SciPy.png")

        self.logged_in = False  # Track if user is logged in

#=========================================================Login window function============================================================#

        def show_login_window():
            login_window = Toplevel(self.main_window)
            login_window.title("Login")
            login_window.geometry("300x250+500+200")
            login_window.resizable(False, False)

            # window styling
            login_window.configure(bg="#CAE9FF")
            Label(login_window, text="Please Login to Access Admin Panel", font=("Arial", 12, "bold"), bg="#CAE9FF").pack(pady=10)

            #Username ntry
            username_label = Label(login_window, text="Username", bg="#CAE9FF", font=("Arial", 12))
            username_label.pack()
            username_entry = Entry(login_window, font=("Arial", 12), width=20, bd=1)
            username_entry.pack(pady=5)
            username_entry.focus()

            #Passwordentry
            password_label = Label(login_window, text="Password", bg="#CAE9FF", font=("Arial", 12))
            password_label.pack()
            password_entry = Entry(login_window, font=("Arial", 12), width=20, bd=1, show='*')
            password_entry.pack(pady=5)

            # Login button function
            def login(event=NONE):
                valid_username = "admin"
                valid_password = "12345"

                username = username_entry.get()
                password = password_entry.get()

                if username == valid_username and password == valid_password:
                    self.logged_in = True
                    login_window.destroy()
                    show_frame1()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
                    username_entry.delete(0, END)
                    password_entry.delete(0, END)

            login_window.bind('<Return>', login)

            # Login button
            login_btn = Button(login_window, text="Login", font=("Arial", 12, "bold"), bg="#1B4965", fg="white", relief=RAISED, command=login)
            login_btn.pack(pady=10)
            #Restrict background main windows activity
            login_window.transient(self.main_window)
            login_window.grab_set()
            self.main_window.wait_window(login_window)

#=================================Update function==================================#

        def show_frame1():
            if self.logged_in:
                adminFrame.tkraise()
            else:
                show_login_window() 

        def clear_field(field):
            field.config(state="normal") 
            field.delete(0, tk.END)

#=================================ADD function==================================#

        def addProduct(event=None):
            if (nameBox.get() and idBox.get() and priceBox.get() and quantityBox1.get()):
                conn = sql.connect("ProductList.db")
                cursor = conn.cursor()

                cursor.execute("CREATE TABLE IF NOT EXISTS productlist (pro_name TEXT, id INTEGER PRIMARY KEY, price REAL, quantity INTEGER)")

                # Check if the product ID already exists
                cursor.execute("SELECT * FROM productlist WHERE id = ?", (idBox.get(),))
                existing_product = cursor.fetchone()

                if existing_product:
                    messagebox.showinfo("Update Required", "Product ID already exists. Please update the product instead of adding a new one.")
                else:
                    cursor.execute("INSERT INTO productlist (pro_name, id, price, quantity) VALUES (?, ?, ?, ?)",
                                (nameBox.get(), idBox.get(), priceBox.get(), quantityBox1.get()))
                    conn.commit()
                    messagebox.showinfo("Success", "Product added successfully.")
                    print("Product added:", nameBox.get(), idBox.get(), priceBox.get(), quantityBox1.get())

                    populateListBox(productList)    
                    clear_field(nameBox)
                    clear_field(idBox)
                    clear_field(priceBox)
                    clear_field(quantityBox1)
            else:
                messagebox.showinfo("Warning", "All Fields are Necessary")
            
            conn.close()
            nameBox.focus()
            loadProducts()

#=================================Update function==================================

        def updateProduct(event=None):
            conn = sql.connect("ProductList.db")
            cursor = conn.cursor()
            
            product_id = idBox.get()
            if not product_id:
                messagebox.showinfo("Error", "Product ID is required.")
                conn.close()
                return
            
            try:
                product_id = int(product_id)
            except ValueError:
                messagebox.showinfo("Error", "Invalid Product ID.")
                conn.close()
                return
            
            cursor.execute("SELECT * FROM productlist WHERE id=?", (product_id,))
            existing_product = cursor.fetchone()
            
            if existing_product:
                pro_name = existing_product[0]
                pro_price = existing_product[1]
                current_quantity = existing_product[2]
                
                new_name = nameBox.get().strip()
                new_price = priceBox.get().strip()
                new_quantity = quantityBox1.get().strip()
                
                # Only update the fields that are provided by the user
                updates = []
                values = []
                
                if new_name:
                    updates.append("pro_name=?")
                    values.append(new_name)
                if new_price:
                    updates.append("price=?")
                    values.append(float(new_price))
                if new_quantity:
                    try:
                        new_quantity = int(new_quantity)
                        updates.append("quantity=?")
                        values.append(new_quantity)
                    except ValueError:
                        messagebox.showinfo("Error", "Invalid quantity value.")
                        conn.close()
                        return
                
                if updates:
                    # Append the product_id to the values list
                    values.append(product_id)
                    update_query = f"UPDATE productlist SET {', '.join(updates)} WHERE id=?"
                    cursor.execute(update_query, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Product updated successfully.")
                    print(f"Updated product {product_id}: {new_name if new_name else pro_name}, {new_price if new_price else pro_price}, {new_quantity if new_quantity else current_quantity}")  # Debug statement
                    
                    clear_field(nameBox)
                    clear_field(priceBox)
                    clear_field(quantityBox1)
                else:
                    messagebox.showinfo("Warning", "No fields to update.")
            else:
                messagebox.showinfo("Error", f"Product with ID {product_id} not found.")
            
            conn.close()
            loadProducts()
            nameBox.focus()




#=================================Delete function==================================

        def deleteproduct(event=None):
            productid = idBox.get()
            if not productid:
                messagebox.showinfo("Error", "Product ID is required.")
                return
            
            conn = sql.connect("ProductList.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productlist WHERE id = ?", (productid,))
            existing_product = cursor.fetchone()
            if existing_product:
                pro_name = existing_product[0]
                confirm = messagebox.askyesno("Warning", f"Are you sure you want to delete {pro_name} with Product ID {productid}?")
                if confirm:
                    cursor.execute("DELETE FROM productlist WHERE id = ?", (productid,))
                    conn.commit()
                    messagebox.showinfo("Success", "Product deleted successfully.")
                    print(f"Deleted product {productid}: {pro_name}")  # Debug statement
                    
                    clear_field(idBox)
                    loadProducts()
            else:
                messagebox.showinfo("Error", f"Product with ID {productid} not found.")
            
            conn.close()
            idBox.focus()


#=================================Showframe Function===============================

        def show_frame2():
            dashBoardFrame.tkraise()     

#================================= Load products Function===============================
        def loadProducts():
            print("Loading products into the Treeview...")  # Debug statement
            # Clear existing rows in the Treeview
            for item in tree.get_children():
                tree.delete(item)
            
            # Fetching data from SQLite database
            conn = sql.connect("ProductList.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productlist")
            rows = cursor.fetchall()
            
            # Insert fetched data into the Treeview
            for row in rows:
                tree.insert('', tk.END, values=row)
            
            print(f"Loaded {len(rows)} products.")  # Debug statement
            conn.close()


        #********************************CALCULATOR FUNCTION*************************
        def change(event=None):  # Added default event parameter
                a = int(totalCost1.get())
                b = int(cashBox.get())  # Get value from totalCost Entry widget
                c = b-a
                changeText.config(state="normal") 
                changeText.delete(0, tk.END)
                changeText.insert(0, str(c))
                changeText.config(state="disabled")

        def populateListBox(productList):
            for item in productList.get_children():
                productList.delete(item)
            conn = sql.connect('ProductList.db')
            cursor = conn.cursor()
            cursor.execute("SELECT pro_name, price FROM productlist")
            rows = cursor.fetchall()
            
            for data in rows:
                productList.insert('', tk.END, values=data)
            loadProducts()
            conn.close()

        def displayBill():
            textArea.config(state="normal")   
            textArea.delete(1.0,END)
            # textArea.insert(END,'\n**************************************************') 
            textArea.insert(END,'------------------TAX INVOICE--------------\n\n')
            textArea.insert(END,'CUSTOMER DETAILS\n')
            # textArea
            textArea.insert(END,'-------------------------------------------------') 
            textArea.insert(END,'NAME : Atharva Ravi Date\n')
            textArea.insert(END,'PHONE NO. : 7276250789\n')
            textArea.insert(END,'-------------------------------------------------') 
            textArea.insert(END,'Particulars                \t Qty   \t  Rate \t   Amount\n')
            textArea.insert(END,'-------------------------------------------------') 

        def addItem():
            selected_items = productList.selection()
            if not selected_items:
                messagebox.showwarning("Warning", "Please select a product to add.")
                return

            try:
                quantity = int(quantityBox.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity.")
                return
    
            # Enable textArea to insert text
            textArea.config(state="normal")

            cumulative_total = 0

            for item in selected_items:
                item_data = productList.item(item, 'values')
                product_name, product_price = item_data[0], float(item_data[1])
                total_price = product_price * quantity

                textArea.insert(tk.END, f"{product_name}\t                  {quantity:.1f}\t      {product_price:.1f}\t      {total_price:.1f}\n")
                
                cumulative_total += total_price

            # Clear the quantity box for new input
            quantityBox.delete(0, tk.END)

            # Update the totalCostBox with the new cumulative total
            current_total = totalCostBox.get()
            if current_total:
                cumulative_total += float(current_total)
            
            totalCostBox.delete(0, tk.END)
            totalCostBox.insert(0, str(cumulative_total))

    # Remove selection after adding to the textArea
            for item in selected_items:
                productList.selection_remove(item)

            # Disable textArea to prevent user editing
            LoadProducts()
            textArea.config(state="disabled") 

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

        #prdTitle = PRODUCT PANEL Title
        prdTitle = Label(productPanel, text="-------- Product Panel --------", font=("Arial", 15, "bold"), pady=7).pack()

        prdName = Label(productPanel, text="Name :", font=("Arial", 11, "bold"))
        prdName.place(x=20, y=80)
        nameBox = tk.Entry(productPanel, width=25, bd=1, validate=None, relief=SOLID, font=("Arial", 12)) 
        nameBox.place(x=120, y=80, height=25) 
        nameBox.focus()

        prdId = Label(productPanel, text="ID :", font=("Arial", 11, "bold"))
        prdId.place(x=20, y=140)
        idBox = tk.Entry(productPanel, width=25, bd=1, validate=None, relief=SOLID, font=("Arial", 12))
        idBox.place(x=120, y=140, height=25)

        prdPrice = Label(productPanel, text="Price :", font=("Arial", 11, "bold"))
        prdPrice.place(x=20, y=200)
        priceBox = tk.Entry(productPanel, width=25, bd=1, validate=None, relief=SOLID, font=("Arial", 12))
        priceBox.place(x=120, y=200, height=25)

        prdQuantity = Label(productPanel, text="Quantity :", font=("Arial", 11, "bold"))
        prdQuantity.place(x=20, y=260)
        quantityBox1 = tk.Entry(productPanel, width=25, bd=1, validate=None, relief=SOLID, font=("Arial", 12))
        quantityBox1.place(x=120, y=260, height=25)

        addBtn = Button(productPanel, text="ADD", width=8, height=2, relief=RAISED, bg="#1B4965", fg="white", font=("Arial", 11, "bold"), command=addProduct)
        addBtn.place(x=30, y=420)
        updateBtn = Button(productPanel, text="UPDATE", width=8, height=2, relief=RAISED, bg="#1B4965", fg="white", font=("Arial", 11, "bold"), command=updateProduct)
        updateBtn.place(x=150, y=420)
        deleteBtn = Button(productPanel, text="DELETE", width=8, height=2, relief=RAISED, bg="#1B4965", fg="white", font=("Arial", 11, "bold"), command=deleteproduct)
        deleteBtn.place(x=270, y=420)

        productTable = Frame(adminFrame, bd=3, relief=RIDGE)
        productTable.place(x=409, y=5, width=737, height=607)

    #=================================Admin panel display=============================

        prdTableTitle = Label(productTable, text="-------- Products Table --------", font=("Arial", 15, "bold"), pady=7).pack()

        columns = ('id', 'pro_name', 'price', 'quantity')
        tree = ttk.Treeview(productTable, columns=columns, show='headings')
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 12)) 
        tree.heading('id', text='ID', anchor=tk.W)
        tree.heading('pro_name', text='Name', anchor=tk.W)
        tree.heading('price', text='Price',anchor=tk.W)
        tree.heading('quantity', text='Quantity',anchor=tk.W)

        tree.pack(fill=tk.BOTH, expand=True)

        loadProducts()

        #==================DASH BOARD PANEL ===========================================
        #==========product================
        pSelectFrame = tk.Frame(dashBoardFrame, bd=3, relief=tk.RIDGE, bg="white")
        pSelectFrame.place(x=5, y=5, width=430, height=350)

        l1 = tk.Label(pSelectFrame, text="PRODUCT LIST", bg="#5FA8D3", fg="#CAE9FF", font=("Arial", 16, "bold"), height=2, relief=tk.RAISED)
        l1.pack(side=tk.TOP, fill=tk.X)

        dedicateFrame = tk.Frame(pSelectFrame, width=380, height=500)
        dedicateFrame.place(x=25, y=100)

        # Create a Treeview widget
        columns = ('product', 'price')
        productList = ttk.Treeview(dedicateFrame, columns=columns, show='headings', selectmode='extended')

        # Define headings
        productList.heading('product', text='Product')
        productList.heading('price', text='Price')

        # Define column widths
        productList.column('product', width=200, anchor=tk.CENTER)
        productList.column('price', width=100, anchor=tk.CENTER)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(dedicateFrame, orient="vertical", command=productList.yview)
        productList.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        productList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        populateListBox(productList)
        productList.pack(side=RIGHT,fill=BOTH,padx=1)
        scrollbar.config( command = productList.yview )

        def LoadProducts():
            for item in productList.get_children():
                productList.delete(item)
            
            conn = sql.connect('ProductList.db')
            cursor = conn.cursor()
            cursor.execute("SELECT pro_name, price FROM productlist")
            rows = cursor.fetchall()
            
            for data in rows:
                productList.insert('', tk.END, values=data)

            conn.close()
        #=============calculator==========

        calciFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE,bg="white")
        calciFrame.place(x=440,y=5,width=290,height=290)

        l1 = Label(calciFrame,text="CALCULATOR",bg="#5FA8D3",fg="#CAE9FF",font=("Arial",16,"bold"),height=2,relief=RAISED).pack(side=TOP,fill=X)

        cashRecieved = Label(calciFrame,text="Money Received",font=("Arial",10,"bold"),bg="white").place(x=5,y=65)
        rupees = Label(calciFrame,text="₹",font=("Arial",15,"bold"),bg="white").place(x=15,y=92)
        cashBox = tk.Entry(calciFrame,width=17,bd=1,validate=None,justify="center",relief=SOLID,font=("Arial",12),bg="white")
        cashBox.place(x=46,y=95,height=30)

        totalCost = Label(calciFrame,text="Total Cost",font=("Arial",10,"bold"),bg="white").place(x=5,y=141)
        rupeesTotal = Label(calciFrame,text="₹",font=("Arial",15,"bold"),bg="white").place(x=15,y=169)
        totalCost1 = tk.Entry(calciFrame,width=17,bd=1,relief=SOLID,justify="center",font=("Arial",12),bg="white")
        totalCost1.place(x=46,y=171,height=30)


        rupeesChange = Label(calciFrame,text="₹",font=("Arial",15,"bold"),bg="white").place(x=15,y=235)
        changeText = tk.Entry(calciFrame,width=17,bd=1,relief=SOLID,state="disabled",justify="center",font=("Arial",12),bg="white")
        changeText.place(x=46,y=235,height=30)
        changeBtn = Button(calciFrame,text="CHANGE",relief=RAISED,bg="#1B4965",fg="white",font=("Arial",10,"bold"),command=change).place(x=210,y=237)


        #=================================Options============================================
        moneyFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE,bg="white")
        moneyFrame.place(x=440,y=300,width=290,height=310)
        l1 = Label(moneyFrame,text="OPTIONS",bg="#5FA8D3",fg="#CAE9FF",font=("Arial",16,"bold"),height=2,relief=RAISED).pack(side=TOP,fill=X)

        adD = Button(moneyFrame,text="Add",font=("Arial",11,"bold"),width=9,height=2,command=addItem,relief=RAISED).place(x=30,y=75)

        biLLBtn = Button(moneyFrame,text="Bill",font=("Arial",11,"bold"),width=9,height=2,relief=RAISED,command=displayBill).place(x=150,y=75)

        totalLabel = Label(moneyFrame,text="TotalCost : ",font=("Calibri",12,"bold"),bg="white")
        totalLabel.place(x=30,y=150)

        totalCostBox = tk.Entry(moneyFrame,width=13,bd=1,relief=SOLID,justify="center",font=("Arial",12),bg="white")
        totalCostBox.place(x=120,y=150,height=32)

        quantityLabel = Label(moneyFrame,text="Quantity : ",font=("Calibri",12,"bold"),bg="white")
        quantityLabel.place(x=30,y=200)

        quantityBox = tk.Entry(moneyFrame,width=7,bd=1,relief=SOLID,justify="center",font=("Arial",12),bg="white")
        quantityBox.place(x=120,y=200,height=35)


        TotalBtn = Button(moneyFrame,text="Total",font=("Arial",11,"bold"),width=9,height=2,relief=RAISED).place(x=30,y=250)

        printBtn = Button(moneyFrame,text="Print",font=("Arial",11,"bold"),width=9,height=2,relief=RAISED).place(x=150,y=250)


        #==================================Bill============================================
        billFrame = Frame(dashBoardFrame,bd=3,relief=RIDGE)
        billFrame.place(x=735,y=5,width=415,height=563)

        innerBillFrame = Frame(billFrame,bd=3,relief=RIDGE)
        innerBillFrame.place(x=3,y=2,width=404,height=553)

        billHead = Label(innerBillFrame,text="BILL",bd=3,relief=RAISED,height=3,font=("Arial",15,"bold"),bg="#5FA8D3",fg="#CAE9FF").pack(side=TOP,fill=X)

        billBoardArea = Frame(innerBillFrame,bd=2,relief=GROOVE,width=400,height=545)
        billBoardArea.pack()

        billtitle = Label(billBoardArea,text="Receipt",font=("Arial",15,"bold"),bd=7,relief=GROOVE).pack(fill=X)

        scrol = Scrollbar(billBoardArea,orient=VERTICAL)
        scrol.pack(side=RIGHT,fill=Y)
        textArea = Text(billBoardArea,font=("Times New Roman",12),yscrollcommand=scrol.set,state="disabled",padx=40)
        textArea.pack(fill=BOTH)
        scrol.config(command=textArea.yview)

        




main_window = Tk()
mainObj=IMS(main_window)


main_window.mainloop()
