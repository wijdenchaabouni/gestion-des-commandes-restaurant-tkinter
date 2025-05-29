
from tkinter import ttk, Tk  
from tkinter import *  
from tkinter import messagebox 
from subprocess import call  
import mysql.connector 



# === Fonction : Ajouter une Table ===
def ajouteTable():
    numero_table = txttable.get()   
    nombre_chaise = txtchaise.get() 
    etat = "libre" "

   
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
    meConnect = maBase.cursor()

    try:
       
        sql = "INSERT INTO tbl (numero_table, nombre_chaise, etat) VALUES (%s, %s, %s)"
        val = (numero_table, nombre_chaise, etat)
        meConnect.execute(sql, val)
        maBase.commit()  

       
        messagebox.showinfo("Information", "Table ajoutée avec succès")

      
        table.insert('', END, values=(numero_table, nombre_chaise, etat))

     
        txttable.delete(0, END)
        txtchaise.delete(0, END)

    except Exception as e:  
        print(e)  
        maBase.rollback() 

    finally:
        maBase.close()  
    maBase.close()  

# === Fonction : Supprimer une Table ===

def supprimerTable():
    numero_table = txttable.get()  

    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
    meConnect = maBase.cursor()  
    try:
      
        sql = "DELETE FROM tbl WHERE numero_table = %s"  
        val = (numero_table,)  
        meConnect.execute(sql, val)  
        maBase.commit()  

      
        messagebox.showinfo("Information", "Table supprimée avec succès")
        
       
        selected_item = table.selection()  
        if selected_item:
            table.delete(selected_item)  

        
        maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
        meConnect = maBase.cursor()  
        meConnect.execute("SELECT * FROM tbl")  
        for row in table.get_children():
            table.delete(row)  
        for row in meConnect:  
            table.insert('', END, values=row)  
        txttable.delete(0, END)

    except Exception as e:  
        print(e)  
        maBase.rollback() 
    finally:
        maBase.close()  

# === Fonction : Ajouter un Aliment ===
def ajouterAliments():
  
    code_aliment = txtcodealiment.get() 
    nom_aliment = txtnomaliment.get()  
    prix_aliment = txtprixaliment.get()

   
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
    meConnect = maBase.cursor()  
    try:
       
        sql = "INSERT INTO aliment (code_aliment, nom_aliment, prix_aliment) VALUES (%s, %s, %s)"
        val = (code_aliment, nom_aliment, prix_aliment)  
        meConnect.execute(sql, val)  
        maBase.commit() 

    
        messagebox.showinfo("Information", "Aliment ajouté avec succès")

       
        tablealiment.insert('', END, values=(code_aliment, nom_aliment, prix_aliment)) 
        txtcodealiment.delete(0, END)  
        txtnomaliment.delete(0, END)  
        txtprixaliment.delete(0, END)  

    except Exception as e:
      
        print(e)
        maBase.rollback()  

    finally:
        
        maBase.close()


# === Fonction : Supprimer un Aliment ===
def supprimerAliments():
  
    code_aliment = txtcodealiment.get()

   
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
    meConnect = maBase.cursor()  

    try:
       
        sql = "DELETE FROM aliment WHERE code_aliment = %s"
        val = (code_aliment,)  
        meConnect.execute(sql, val)  
        maBase.commit()  
        messagebox.showinfo("Information", "Aliment supprimé avec succès")

      
        selected_item = tablealiment.selection() 
        if selected_item:  
            tablealiment.delete(selected_item)  

        maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
        meConnect = maBase.cursor()  
        meConnect.execute("SELECT * FROM aliment") 
        for row in tablealiment.get_children():
            tablealiment.delete(row)  

        for row in meConnect: 
            tablealiment.insert('', END, values=row)  
        txtcodealiment.delete(0, END)

    except Exception as e:
      
        print(e) 
        maBase.rollback() 

    finally:
        maBase.close()  #
# === Interface graphique principale ===
root = Tk()
root.title("RESTO")
root.geometry("1350x700+2+20")
root.resizable(False, False)
root.configure(background="#164159")

lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Formulaire d'enregistrement des tables", font=("Sans Serif", 18), background="#164159", foreground="white")
lbltitre.place(x=-5, y=20, width=600)

lbltable = Label(root, text="Numéro table", font=("Sans Serif", 14), background="#164159", foreground="white")
lbltable.place(x=10, y=70, width=200)
txttable = Entry(root, bd=4, font=("Arial", 14))
txttable.place(x=200, y=70, width=150)

lblchaise = Label(root, text="Nombre de chaise", font=("Sans Serif", 14), background="#164159", foreground="white")
lblchaise.place(x=10, y=120, width=200)
txtchaise = Entry(root, bd=4, font=("Arial", 14))
txtchaise.place(x=200, y=120, width=150)

btnenregistrerTable = Button(root, text="ENREGISTRER", font=("Arial", 18), bg="#180461", fg="white", command=ajouteTable)
btnenregistrerTable.place(x=10, y=170, width=200)
btnsupprimerTable = Button(root, text="SUPPRIMER", font=("Arial", 18), bg="#180461", fg="white", command=supprimerTable)
btnsupprimerTable.place(x=230, y=170, width=200)

table = ttk.Treeview(root, columns=(1, 2, 3), height=10, show="headings")
table.place(x=550, y=60, width=800, height=200)

table.heading(1, text="NUMERO TABLE")
table.heading(2, text="NOMBRE DE CHAISES")
table.heading(3, text="ETAT")

table.column(1, width=50)
table.column(2, width=20)
table.column(3, width=100)

maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
meConnect = maBase.cursor()
meConnect.execute("SELECT * FROM tbl")
for row in meConnect:
    table.insert('', END, values=row)
maBase.close()

lbltitreAliment = Label(root, borderwidth=3, relief=SUNKEN, text="Formulaire d'enregistrement des aliments", font=("Sans Serif", 18), background="#164159", foreground="white")
lbltitreAliment.place(x=-5, y=300, width=600)

lblcodealiment = Label(root, text="Code aliment", font=("Sans Serif", 14), background="#164159", foreground="white")
lblcodealiment.place(x=10, y=350, width=200)
txtcodealiment = Entry(root, bd=4, font=("Arial", 14))
txtcodealiment.place(x=200, y=350, width=150)

lblnomaliment = Label(root, text="Nom aliment", font=("Sans Serif", 14), background="#164159", foreground="white")
lblnomaliment.place(x=10, y=400, width=200)
txtnomaliment = Entry(root, bd=4, font=("Arial", 14))
txtnomaliment.place(x=200, y=400, width=300)

lblprixaliment = Label(root, text="Prix aliment", font=("Sans Serif", 14), background="#164159", foreground="white")
lblprixaliment.place(x=10, y=450, width=200)
txtprixaliment = Entry(root, bd=4, font=("Arial", 14))
txtprixaliment.place(x=200, y=450, width=100)

btnenregistrerAliment = Button(root, text="ENREGISTRER", font=("Arial", 18), bg="#180461", fg="white", command=ajouterAliments)
btnenregistrerAliment.place(x=10, y=500, width=200)
btnsupprimerAliment = Button(root, text="SUPPRIMER", font=("Arial", 18), bg="#180461", fg="white", command=supprimerAliments)
btnsupprimerAliment.place(x=230, y=500, width=200)

tablealiment = ttk.Treeview(root, columns=(1, 2, 3), height=10, show="headings")
tablealiment.place(x=550, y=350, width=800, height=300)

tablealiment.heading(1, text="Code Aliment")
tablealiment.heading(2, text="Nom Aliment")
tablealiment.heading(3, text="Prix Aliment")

tablealiment.column(1, width=50)
tablealiment.column(2, width=20)
tablealiment.column(3, width=100)

maBase = mysql.connector.connect(host="localhost", user="root", password="", database="resto")
meConnect = maBase.cursor()
meConnect.execute("SELECT * FROM aliment")
for row in meConnect:
    tablealiment.insert('', END, values=row)
maBase.close()

root.mainloop()
