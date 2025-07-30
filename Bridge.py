import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymongo
import requests

def enviar_dados_para_esp(nome, preco):
    try:
        url = "http://192.168.0.18/receber_dados" 
        data = {"nome_produto": nome, "preco_produto": preco}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Dados enviados com sucesso para o ESP8266.")
        else:
            messagebox.showerror("Erro", "Erro ao enviar dados para o ESP8266.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def update_list():

    tree.delete(*tree.get_children())
    
    for doc in collection.find():

        nome_produto = doc.get('nome', 'N/A')
        preco_produto = doc.get('preço', 'N/A')
        tree.insert("", "end", values=(nome_produto, preco_produto))

def enviar_dados_selecionados():
    try:

        selecionado = tree.selection()
        if selecionado:

            values = tree.item(selecionado, 'values')
            
            if values:
                produto_nome = values[0]
                produto_preco = values[1]

                enviar_dados_para_esp(produto_nome, produto_preco)

                messagebox.showinfo("Sucesso", f"Dados do produto '{produto_nome}' enviados para o ESP com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum produto selecionado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

root = tk.Tk()
root.title("Aplicação Bridge")

client = pymongo.MongoClient('localhost', 27017)
data_base = client['my_database_v0']
collection = data_base['my_collection_v0']

tree = ttk.Treeview(root, columns=("Nome", "Preço", ), show="headings")

tree.heading("Nome", text="Nome")
tree.heading("Preço", text="Preço")

tree.column("Nome", width=150, anchor=tk.CENTER)
tree.column("Preço", width=80, anchor=tk.CENTER)

tree.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

botao_enviar_selecionado = tk.Button(root, text="Enviar Produto Selecionado", command=enviar_dados_selecionados)
botao_enviar_selecionado.grid(row=1, column=0, columnspan=2, pady=10)

botao_atualizar_lista = tk.Button(root, text="Atualizar Lista de Produtos", command=update_list)
botao_atualizar_lista.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
