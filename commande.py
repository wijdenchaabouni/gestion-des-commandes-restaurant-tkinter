from subprocess import call 
from tkinter import ttk, Tk  
from tkinter import *  
from tkinter import messagebox 
import mysql.connector  


def get_connection():
   
    return mysql.connector.connect(host="localhost", user="root", password="", database="resto")


def update_treeview():
  
    for row in tablecommande.get_children():
        tablecommande.delete(row)

   
    maBase = get_connection()
    meConnect = maBase.cursor()
    meConnect.execute("SELECT * FROM commande")
  
    for row in meConnect:
        tablecommande.insert('', END, values=row) 

 
    maBase.close()


def update_libere_treeview():
    
    for row in tableliberee.get_children():
        tableliberee.delete(row)

    maBase = get_connection()
    meConnect = maBase.cursor()
    meConnect.execute("SELECT numero_table, id_commande FROM commande WHERE liberee = 1")

   
    for row in meConnect:
        tableliberee.insert('', END, values=row)


    maBase.close()


def ajouterCommande():
    
    code_aliment = txtaliment.get()
    quantite = txtquantite.get()
    numero_table = txttable.get()

   
    maBase = get_connection()
    meConnect = maBase.cursor()

    try:
     
        sql = "INSERT INTO commande (code_aliment, quantite, numero_table) VALUES (%s, %s, %s)"
        val = (code_aliment, quantite, numero_table)
        meConnect.execute(sql, val)
        maBase.commit()  

     
        messagebox.showinfo("Information", "Commande ajoutée avec succès")

       
        update_treeview()

       
        txtaliment.delete(0, END)
        txtquantite.delete(0, END)
        txttable.delete(0, END)

    except Exception as e:
        print(e) 
        maBase.rollback()  

    finally:
        maBase.close() 


def supprimerCommande():
    
    id_commande = txtannuler.get()

 
    maBase = get_connection()
    meConnect = maBase.cursor()

    try:
      
        sql = "DELETE FROM commande WHERE id_commande = %s"
        val = (id_commande,)
        meConnect.execute(sql, val)
        maBase.commit()  
      
        messagebox.showinfo("Information", "Commande supprimée avec succès")

      
        update_treeview()

      
        txtannuler.delete(0, END)

    except Exception as e:
        print(e) 
        maBase.rollback()  

    finally:
        maBase.close() 


def libererTable():
   
    numero_table = txttable.get()

    maBase = get_connection()
    meConnect = maBase.cursor()

    try:
      
        meConnect.execute("SELECT id_commande FROM commande WHERE numero_table = %s", (numero_table,))
        commandes_supprimees = meConnect.fetchall()

       
        sql = "DELETE FROM commande WHERE numero_table = %s"
        val = (numero_table,)
        meConnect.execute(sql, val)
        maBase.commit()  

        messagebox.showinfo("Information", "Table libérée et commandes supprimées")
 
        for commande in commandes_supprimees:
            tableliberee.insert('', END, values=(numero_table, commande[0]))

       
        txttable.delete(0, END)

    except Exception as e:
        print(e)  
        maBase.rollback()  

    finally:
        maBase.close()  

root = Tk()
root.title("RESTO")  
root.geometry("1350x700+2+20") 
root.resizable(False, False) 
root.configure(background="#164159")  


lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Formulaire d'enregistrement des commandes", font=("Sans Serif", 18), background="#164159", foreground="white")
lbltitre.place(x=-5, y=20, width=600)


lblaliment = Label(root, text="Code aliment", font=("Sans Serif", 14), background="#164159", foreground="white")
lblaliment.place(x=10, y=70, width=200)
txtaliment = Entry(root, bd=4, font=("Arial", 14))
txtaliment.place(x=230, y=70, width=150)


lblquantite = Label(root, text="Quantité", font=("Sans Serif", 14), background="#164159", foreground="white")
lblquantite.place(x=10, y=120, width=200)
txtquantite = Entry(root, bd=4, font=("Arial", 14))
txtquantite.place(x=230, y=120, width=150)

lbltable = Label(root, text="Numéro de la table", font=("Sans Serif", 14), background="#164159", foreground="white")
lbltable.place(x=10, y=170, width=200)
txttable = Entry(root, bd=4, font=("Arial", 14))
txttable.place(x=230, y=170, width=150)


btnenregistrerTable = Button(root, text="ENREGISTRER", font=("Arial", 18), bg="#180461", fg="white", command=ajouterCommande)
btnenregistrerTable.place(x=10, y=220, width=200)

btnannuler = Button(root, text="ANNULER", font=("Arial", 18), bg="#180461", fg="white", command=supprimerCommande)
btnannuler.place(x=10, y=300, width=200)


txtannuler = Entry(root, bd=4, font=("Arial", 14))
txtannuler.place(x=230, y=300, width=150, height=45)


btnliberer = Button(root, text="LIBERER UNE TABLE", font=("Arial", 18), bg="#180461", fg="white", command=libererTable)
btnliberer.place(x=60, y=380, width=400)


tablecommande = ttk.Treeview(root, columns=(1, 2, 3, 4), height=10, show="headings")
tablecommande.place(x=550, y=60, width=800, height=300)


tablecommande.heading(1, text="ID COMMANDE")
tablecommande.heading(2, text="NUMERO DE LA TABLE")
tablecommande.heading(3, text="COMMANDE")
tablecommande.heading(4, text="QUANTITÉ")

tablecommande.column(1, width=50)
tablecommande.column(2, width=20)
tablecommande.column(3, width=100)
tablecommande.column(4, width=100)


tableliberee = ttk.Treeview(root, columns=(1, 2), height=10, show="headings")
tableliberee.place(x=550, y=380, width=800, height=300)

tableliberee.heading(1, text="NUMERO DE LA TABLE")
tableliberee.heading(2, text="ID COMMANDE")

tableliberee.column(1, width=50)
tableliberee.column(2, width=50)

root.mainloop()

