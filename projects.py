import sqlite3
from tkinter import *
from tkinter import messagebox

# ---------- DATABASE ----------
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    disease TEXT,
    contact TEXT
)
""")
conn.commit()

# ---------- FUNCTIONS ----------

def add_patient():
    name = name_var.get()
    age = age_var.get()
    gender = gender_var.get()
    disease = disease_var.get()
    contact = contact_var.get()

    if name == "" or age == "" or contact == "":
        messagebox.showerror("Error", "Please fill required fields")
        return

    cursor.execute("INSERT INTO patients(name, age, gender, disease, contact) VALUES (?, ?, ?, ?, ?)",
                   (name, age, gender, disease, contact))
    conn.commit()

    messagebox.showinfo("Success", "Patient Added Successfully")
    clear_fields()

def view_patients():
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM patients")
    for row in cursor.fetchall():
        listbox.insert(END, row)

def search_patient():
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + name_var.get() + '%',))
    for row in cursor.fetchall():
        listbox.insert(END, row)

def delete_patient():
    selected = listbox.get(ACTIVE)
    if selected:
        cursor.execute("DELETE FROM patients WHERE id=?", (selected[0],))
        conn.commit()
        view_patients()

def clear_fields():
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    disease_var.set("")
    contact_var.set()

# ---------- GUI ----------

root = Tk()
root.title("Patient Record Management System")
root.geometry("750x520")

Label(root, text="Hospital Patient Record System",
      font=("Arial", 18, "bold")).pack(pady=10)

frame = Frame(root)
frame.pack()

name_var = StringVar()
age_var = StringVar()
gender_var = StringVar()
disease_var = StringVar()
contact_var = StringVar()

Label(frame, text="Name").grid(row=0, column=0)
Entry(frame, textvariable=name_var).grid(row=0, column=1)

Label(frame, text="Age").grid(row=1, column=0)
Entry(frame, textvariable=age_var).grid(row=1, column=1)

Label(frame, text="Gender").grid(row=2, column=0)
Entry(frame, textvariable=gender_var).grid(row=2, column=1)

Label(frame, text="Disease").grid(row=3, column=0)
Entry(frame, textvariable=disease_var).grid(row=3, column=1)

Label(frame, text="Contact").grid(row=4, column=0)
Entry(frame, textvariable=contact_var).grid(row=4, column=1)

Button(frame, text="Add Patient", command=add_patient,
       bg="green", fg="white").grid(row=5, column=0, pady=10)

Button(frame, text="View All", command=view_patients)\
    .grid(row=5, column=1)

Button(frame, text="Search", command=search_patient)\
    .grid(row=6, column=0)

Button(frame, text="Delete Selected", command=delete_patient,
       bg="red", fg="white").grid(row=6, column=1)

Button(frame, text="Clear", command=clear_fields)\
    .grid(row=7, column=0, columnspan=2, pady=5)

listbox = Listbox(root, width=90)
listbox.pack(pady=20)

root.mainloop()
