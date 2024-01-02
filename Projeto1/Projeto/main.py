import tkinter as tk
from tkinter import ttk
import utils as ut
from classes import ConsoleWidget, RegistradoresWidget, BlocoTraducao, MemoriaWidget

root = ut.criar_janela_principal()
menu = tk.Menu(root)

# Criar um Frame para a barra de ferramentas
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
toolbar_frame.config(bg="#1e1e1e", width=10)

# Campo dos registradores
registradores_widget = RegistradoresWidget(root)
registradores_widget.pack(side=tk.LEFT, fill=tk.Y, expand=False)

# Cria o console
console_widget = ConsoleWidget(master=root)
console_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)
console_widget.text_widget.config(height=15)
root.config(menu=menu)

#Bloco de Memoria de dados
memoria_widget = MemoriaWidget(root)
memoria_widget.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
memoria_widget.text_area.config(width=35)

# Bloco de tradução
traducao_widget = BlocoTraducao(root)
traducao_widget.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
traducao_widget.traducao_texto.config(width=36)

# Bloco de texto
texto = ut.criar_area_de_codigo(root)
texto.pack(side=tk.LEFT, fill=tk.Y, expand=False)

ut.novo_arquivo()

# Adiciona botões à barra de ferramentas
novo_button = tk.Button(toolbar_frame, text="New", command=ut.novo_arquivo, bg="#1e1e1e", fg="#27AE60")
novo_button.pack(side=tk.LEFT)

abrir_button = tk. Button(toolbar_frame, text="Open", command=ut.abrir_arquivo, bg="#1e1e1e", fg="#27AE60")
abrir_button.pack(side=tk.LEFT)

salvar_button = tk.Button(toolbar_frame, text="Save", command=ut.salvar_arquivo, bg="#1e1e1e", fg="#27AE60")
salvar_button.pack(side=tk.LEFT)

run_button = tk.Button(toolbar_frame, text="Run", command=lambda: ut.run_codigo(texto, console_widget, registradores_widget, traducao_widget, memoria_widget), bg="#1e1e1e", fg="#27AE60")
run_button.pack(side=tk.LEFT)

clear_button = tk.Button(toolbar_frame, text="Clear", command=lambda: ut.limpa_console(console_widget, registradores_widget, traducao_widget, memoria_widget), bg="#1e1e1e", fg="#27AE60")
clear_button.pack(side=tk.LEFT)

root.mainloop()
