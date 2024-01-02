import tkinter as tk
from lexer import processar_codigo
from tkinter import filedialog

def run_codigo(texto, console_widget, registradores_widget, traducao_widget, memoria_widget,modo_debug):
    limpa_console(console_widget, registradores_widget, traducao_widget, memoria_widget)
    texto_inserido = texto.get("1.0", tk.END)
    processar_codigo(texto_inserido, registradores_widget, console_widget, traducao_widget, memoria_widget,modo_debug)

def limpa_console(console_widget, registradores_widget, traducao_widget, memoria_widget): 
    traducao_widget.limpar_traducao()
    console_widget.clear()
    registradores_widget.zerar_registradores()
    memoria_widget.zerar_memoria()
    registradores_widget.endereco_label.clear()
    
def criar_janela_principal():
    global root
    root = tk.Tk()
    root.title("PyMIPS")
    root.state('zoomed')
    return root

def criar_area_de_codigo(root):
    global texto
    texto = tk.Text(root)
    texto.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    texto.config(bg="#1e1e1e", fg="#ECF0F1", font=("monaco", 14))
    return texto

def novo_arquivo():
    texto.delete(1.0, tk.END)
    
def abrir_arquivo():
    arquivo = filedialog.askopenfile(defaultextension=".s", filetypes=[("Arquivos Assembly", "*.ass"),("Arquivos Assembly", "*.s"),("Arquivos Assembly", "*.a"), ("Todos os arquivos", "*.*")])
    if arquivo:
        texto.delete(1.0, tk.END)
        texto.insert(tk.END, arquivo.read())
        arquivo.close()

def salvar_arquivo():
    arquivo = filedialog.asksaveasfile(defaultextension =".ass", filetypes=[("Arquivos Assembly", "*.ass"),("Arquivos Assembly", "*.s"),("Arquivos Assembly", "*.a"), ("Todos os arquivos", "*.*")])
    if arquivo:
        arquivo.write(texto.get(1.0, tk.END))
        arquivo.close()