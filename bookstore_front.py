from tkinter import *
from tkinter import messagebox
from bookstore_back import Database

database = Database("books.db")

class Window(object):
    def __init__(self, window):
        self.window = window
        self.window.wm_title("BookStore")

        l1 = Label(window, text="Title")
        l1.grid(row=0, column=1, sticky=E) # sticky aligns widget in compass direction
        l2 = Label(window, text="Author")
        l2.grid(row=1, column=1, sticky=E)
        l3 = Label(window, text="Year")
        l3.grid(row=0, column=3, sticky=E)
        l4 = Label(window, text="ISBN")
        l4.grid(row=1, column=3, sticky=E)

        self.titleEntry = StringVar()
        self.e1 = Entry(window, textvariable=self.titleEntry, width=28)
        self.e1.grid(row=0, column=2, sticky=E, pady = 10)

        self.authorEntry = StringVar()
        self.e2 = Entry(window, textvariable=self.authorEntry, width=28)
        self.e2.grid(row=1, column=2, sticky=E)

        self.yearEntry = StringVar()
        self.e3 = Entry(window, textvariable=self.yearEntry, width=28)
        self.e3.grid(row=0, column=4, columnspan = 2, sticky=E, padx=5)

        self.isbnEntry = StringVar()
        self.e4 = Entry(window, textvariable=self.isbnEntry, width=28)
        self.e4.grid(row=1, column=4, columnspan = 2, sticky=E, padx=5)

        self.listBox1 = Listbox(window, height=10, width=45)
        self.listBox1.grid(row=3, column=1, rowspan=6, columnspan=3, sticky=E)

        sb1 = Scrollbar(window)
        sb1.grid(row=3, column=4, rowspan=6)

        self.listBox1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.listBox1.yview)
        self.listBox1.bind('<<ListboxSelect>>', self.get_selected_row)

        b1 = Button(window, text="View all", width=18, command=self.view_command)
        b1.grid(row=3, column=5)
        b2 = Button(window, text="Search Entry", width=18, command=self.search_command)
        b2.grid(row=4, column=5)
        b3 = Button(window, text="Add Entry", width=18, command=self.add_command)
        b3.grid(row=5, column=5)
        b4 = Button(window, text="Update Selected", width=18, command=self.update_command)
        b4.grid(row=6, column=5)
        b5 = Button(window, text="Delete Selected", width=18, command=self.delete_command)
        b5.grid(row=7, column=5)
        b6 = Button(window, text="Close", width=18, command=window.destroy)
        b6.grid(row=8, column=5)

        pad1 = Label(window)
        pad1.grid(row=2)
        pad2 = Label(window)
        pad2.grid(row=9)
        pad3 = Label(window, width=1)
        pad3.grid(row=0, column=0)
        pad3 = Label(window, width=1)
        pad3.grid(row=0, column=6)

    def get_selected_row(self, event):
        if self.listBox1.curselection():
            index = self.listBox1.curselection()[0]
            self.selected_tuple = self.listBox1.get(index)
            self.e1.delete(0, END)
            self.e1.insert(END, self.selected_tuple[1])
            self.e2.delete(0, END)
            self.e2.insert(END, self.selected_tuple[2])
            self.e3.delete(0, END)
            self.e3.insert(END, self.selected_tuple[3])
            self.e4.delete(0, END)
            self.e4.insert(END, self.selected_tuple[4])

    def view_command(self):
        self.listBox1.delete(0, END)
        for row in database.view():
            self.listBox1.insert(END, row)

    def search_command(self):
        self.listBox1.delete(0, END)
        for row in database.search(self.titleEntry.get().strip(), self.authorEntry.get().strip(), self.yearEntry.get().strip(), self.isbnEntry.get().strip()):
            self.listBox1.insert(END, row)

    def add_command(self):
        if len(self.titleEntry.get()) != 0 and len(self.authorEntry.get()) != 0 and len(self.yearEntry.get()) != 0 and len(self.isbnEntry.get()) != 0:
            self.listBox1.delete(0, END)
            database.insert(self.titleEntry.get().strip(), self.authorEntry.get().strip(), self.yearEntry.get().strip(), self.isbnEntry.get().strip())
            self.listBox1.insert(END, (self.titleEntry.get().strip(), self.authorEntry.get().strip(), self.yearEntry.get().strip(), self.isbnEntry.get().strip()))
        else:
            messagebox.showinfo("Add Entry", "Please fill out all fields.")

    def update_command(self):
        if self.selected_tuple:
            database.update(self.selected_tuple[0], self.titleEntry.get().strip(), self.authorEntry.get().strip(), self.yearEntry.get().strip(), self.isbnEntry.get().strip())
            self.view_command()

    def delete_command(self):
        if self.listBox1.curselection():
            msg = messagebox.askquestion("Delete Entry", "Are you sure that you want to delete the entry?")
            if msg == "yes":
                database.delete(self.selected_tuple[0])
                self.view_command()


window = Tk()
Window(window)
window.mainloop()
