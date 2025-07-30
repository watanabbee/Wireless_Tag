import pymongo
import locale
import tkinter as tk
from tkinter import ttk

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

client = pymongo.MongoClient('localhost', 27017)
data_base = client['my_database_v0']
collection = data_base['my_collection_v0']

def adicionar_produto():
    nome_produto = entry_nome.get()
    preco_produto = float(entry_preco.get())
    preco_produto = locale.currency(preco_produto)
    quantidade_produto = int(entry_quantidade.get())
    
    collection.insert_one({'nome': nome_produto, 'preço': preco_produto, 'quantidade': quantidade_produto })
    
    update_list()

def update_list():

    tree.delete(*tree.get_children())

    for doc in collection.find():
        nome_produto = doc.get('nome', 'N/A')
        preco_produto = doc.get('preço', 'N/A')
        quantidade_produto = doc.get('quantidade', 'N/A')

        tree.insert("", "end", values=(nome_produto, preco_produto, quantidade_produto))

root = tk.Tk()
root.title("Gerenciamento de Preços")

label_nome = ttk.Label(root, text="Nome do Produto:")
label_preco = ttk.Label(root, text="Preço do Produto:")
label_quantidade = ttk.Label(root, text="Quantidade do Produto:")

entry_nome = ttk.Entry(root)
entry_preco = ttk.Entry(root)
entry_quantidade = ttk.Entry(root)

button_adicionar = ttk.Button(root, text="Adicionar Produto", command=adicionar_produto)

tree = ttk.Treeview(root, columns=("Nome", "Preço", "Quantidade"), show="headings")

tree.heading("Nome", text="Nome")
tree.heading("Preço", text="Preço")
tree.heading("Quantidade", text="Quantidade")

tree.column("Nome", width=150, anchor=tk.CENTER)
tree.column("Preço", width=80, anchor=tk.CENTER)
tree.column("Quantidade", width=80, anchor=tk.CENTER)

label_nome.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
label_preco.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
label_quantidade.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

entry_nome.grid(row=0, column=1, padx=10, pady=5)
entry_preco.grid(row=1, column=1, padx=10, pady=5)
entry_quantidade.grid(row=2, column=1, padx=10, pady=5)

button_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

tree.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

update_list()

root.mainloop()
