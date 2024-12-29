import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk, ImageWin, ImageDraw
import os
import sys
import win32print
import win32ui
import tempfile
from datetime import datetime
from ctypes import windll



# class QRCodeLabelPrinter:

#     global back
#     back = "#DCDCDC"
    
#     def __init__(self, root):
#         self.codigos_unicos = set()
#         self.contador_codigos = 0
#         self.root = root
#         self.root.title("Montador de Palete")

#         icon = ImageTk.PhotoImage(file='logo.png')
#         self.root.iconphoto(False, icon)

#         # Adicionando o título
#         self.title_label = tk.Label(self.root, text="Montagem de Palete",  font=("Roboto", 24, "bold"))
#         self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10, 20), sticky="n")
#         self.title_label.configure(bg=back)
        
#         # Configurar o layout da janela usando grid
#         self.root.geometry("800x400")
#         self.root.grid_columnconfigure(0, weight=1)
#         self.root.grid_columnconfigure(1, weight=1)
#         self.root.grid_columnconfigure(2, weight=1)

#         # Frame para a área de texto (à esquerda)
#         self.frame_text = tk.Frame(self.root)
#         self.frame_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#         self.frame_text.configure(bg=back)

#         # Label e área de texto
#         self.input_label = tk.Label(self.frame_text, text="Insira os códigos de barras:", font=("Roboto", 20, "bold"))
#         self.input_label.pack(pady=10)
#         self.input_label.configure(bg=back)

#         self.input_text = tk.Text(self.frame_text, height=20, width=50)
#         self.input_text.pack(pady=10)
#         self.input_text.configure(bg="#C0C0C0")

#         # Frame para o contador (à direita da área de texto)
#         self.frame_counter = tk.Frame(self.root)
#         self.frame_counter.grid(row=1, column=1, padx=10, pady=(150, 10), sticky="nsew")  # Agora na mesma linha, mas em uma coluna diferente
#         self.frame_counter.configure(bg=back)

#         # Label para o texto "Total de códigos lidos"
#         self.counter_label_text = tk.Label(self.frame_counter, text="Total de códigos lidos:", font=("Roboto", 14, "bold"))
#         self.counter_label_text.pack(pady=10)

#         # Label para o número total de códigos, com fonte maior
#         self.counter_label_number = tk.Label(self.frame_counter, text="0", font=("Roboto", 100, "bold"))
#         self.counter_label_number.pack()

#         self.counter_label_text.configure(bg=back)
#         self.counter_label_number.configure(bg=back)


#         # Vincular o evento de mudança de conteúdo no campo de texto
#         self.input_text.bind("<<Modified>>", self.update_counter)

#         # Frame para os botões (centro)
#         self.frame_buttons = tk.Frame(self.root)
#         self.frame_buttons.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
#         self.frame_buttons.configure(bg="#D3D3D3")
        
#         # Botão de gerar QR Code
#         self.generate_button = tk.Button(self.frame_buttons, text="Gerar QR Code", command=self.gerar_qr_code, width=30, height=10, font=("Roboto", 15, "bold"), bg="#006400", fg="#f0f0f0")
#         self.generate_button.pack(pady=(50, 20))

#         # Botão para limpar a tela
#         self.clear_button = tk.Button(self.frame_buttons, text="Limpar Tela", command=self.limpar_tela, width=30, font=("Roboto", 15, "bold"), bg="#006400", fg="#f0f0f0")
#         self.clear_button.pack(pady=20)

#         # Frame para a imagem (à direita)
#         self.frame_image = tk.Frame(self.root)
#         self.frame_image.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Ocupa as 3 colunas
#         self.frame_image.configure(bg=back)

#         # Adicionar a imagem estática
#         self.display_image()

#         self.contador_imagens = 1
#         self.qr_image_path = None

#         # Adicionar eventos de hover
#         self.add_hover_effect(self.generate_button)
#         self.add_hover_effect(self.clear_button)
class QRCodeLabelPrinter:
    def __init__(self, root):
        self.codigos_unicos = set()
        self.contador_codigos = 0
        self.root = root
        self.root.title("Montador de Palete")
        self.root.geometry("800x400")

        # Customizar o tema
        ctk.set_appearance_mode("dark")  # Tema escuro
        ctk.set_default_color_theme("green")  # Cor verde

        # Ícone do programa
        icon = ImageTk.PhotoImage(file='logo.png')
        self.root.iconphoto(False, icon)

        # Adicionar título
        self.title_label = ctk.CTkLabel(self.root, text="Montagem de Palete", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10, 20), sticky="n")

        # Configurar colunas para distribuir conteúdo
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Frame para a área de texto (à esquerda)
        self.frame_text = ctk.CTkFrame(self.root)
        self.frame_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Label e área de texto
        self.input_label = ctk.CTkLabel(self.frame_text, text="Insira os códigos de barras:", font=("Roboto", 20, "bold"))
        self.input_label.pack(pady=10)

        self.input_text = ctk.CTkTextbox(self.frame_text, height=20, width=50, bg_color="#333333", fg_color="#C0C0C0")
        self.input_text.pack(pady=10)
        
        # Frame para o contador (à direita da área de texto)
        self.frame_counter = ctk.CTkFrame(self.root)
        self.frame_counter.grid(row=1, column=1, padx=10, pady=(150, 10), sticky="nsew")

        self.counter_label_text = ctk.CTkLabel(self.frame_counter, text="Total de códigos lidos:", font=("Roboto", 14, "bold"))
        self.counter_label_text.pack(pady=10)

        self.counter_label_number = ctk.CTkLabel(self.frame_counter, text="0", font=("Roboto", 100, "bold"))
        self.counter_label_number.pack()

        self.input_text.bind("<<Modified>>", self.update_counter)

        # Frame para os botões (centro)
        self.frame_buttons = ctk.CTkFrame(self.root)
        self.frame_buttons.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # Botão de gerar QR Code
        self.generate_button = ctk.CTkButton(
            self.frame_buttons, text="Gerar QR Code", command=self.gerar_qr_code,
            corner_radius=8, hover_color="#004d00", fg_color="#006400", text_color="#f0f0f0",
            font=("Roboto", 15, "bold")
        )
        self.generate_button.pack(pady=(50, 20))

        # Botão para limpar a tela
        self.clear_button = ctk.CTkButton(
            self.frame_buttons, text="Limpar Tela", command=self.limpar_tela,
            corner_radius=8, hover_color="#004d00", fg_color="#006400", text_color="#f0f0f0",
            font=("Roboto", 15, "bold")
        )
        self.clear_button.pack(pady=20)

        # Frame para a imagem (abaixo)
        self.frame_image = ctk.CTkFrame(self.root)
        self.frame_image.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Adicionar a imagem estática
        self.display_image()

        self.contador_imagens = 1
        self.qr_image_path = None

    # Função para adicionar hover effect aos botões
    def add_hover_effect(self, button):
        button.bind("<Enter>", lambda e: button.config(bg="#008B8B", fg="#4F4F4F"))
        button.bind("<Leave>", lambda e: button.config(bg="#006400", fg="#f0f0f0"))

    def display_image(self):
        # Carregar a imagem do caminho especificado (use o caminho absoluto ou relativo correto)
        image_path = resource_path('img.png')  # Verifique se este caminho está correto!

        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Imagem não encontrada no caminho: {image_path}")

            img = Image.open(image_path)
            img = img.resize((400, 200), Image.Resampling.LANCZOS)
            # img_tk = ctk.CTkImage(img)
            img_tk = ImageTk.PhotoImage(img)

            self.image_label = ctk.CTkFrame(self.root)
            self.image_label = tk.Label(self.frame_image, image=img_tk)
            self.image_label.grid(column=2, columnspan=3, pady=10)
            self.image_label.image = img_tk
            # self.image_label.pack(pady=10)
        except FileNotFoundError as fnf_error:
            messagebox.showerror("Erro", str(fnf_error))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")
        #     # Verifique se o arquivo de imagem existe
        #     if not os.path.exists(image_path):
        #         raise FileNotFoundError(f"Imagem não encontrada no caminho: {image_path}")

        #     # Carregar e redimensionar a imagem
        #     img = Image.open(image_path)
        #     img = img.resize((400, 200), Image.Resampling.LANCZOS)  # Redimensiona a imagem para 200x200
        #     img_tk = ImageTk.PhotoImage(img)

        #     # Adiciona a imagem a um label e a exibe
        #     self.image_label = tk.Label(self.frame_image, image=img_tk)
        #     self.image_label.image = img_tk  # Necessário para o Tkinter manter a referência da imagem
        #     self.image_label.pack(pady=10)
        #     # self.image_label.configure(bg=back)
        # except FileNotFoundError as fnf_error:
        #     messagebox.showerror("Erro", str(fnf_error))
        # except Exception as e:
        #     messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

    def gerar_qr_code(self):

        # Pega os códigos únicos já filtrados
        codigos_barras = list(self.codigos_unicos)
        # codigos_barras = [codigo.strip() for codigo in self.input_text.get("1.0", tk.END).strip().splitlines()]
        # codigos_barras = [codigo.strip() for codigo in self.input_text.get("1.0", tk.END).strip().splitlines() if codigo.strip()]
        # codigos_barras = self.input_text.get("1.0", tk.END).strip().splitlines()

        if not codigos_barras:
            messagebox.showerror("Erro", "Insira ao menos um código de barras.")
            return

        # Concatenar os códigos em uma única string
        dados = "\n".join(codigos_barras)

        # Gerar o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(dados)
        qr.make(fit=True)

        # Criar a imagem do QR Code e salvar com nome personalizado e data
        img = qr.make_image(fill="black", back_color="white")
        data_atual = datetime.now().strftime("%d-%m-%Y")  # Obtém a data no formato dd-mm-yyyy
        self.qr_image_path = f"p{self.contador_imagens}-{data_atual}.png"
        img.save(self.qr_image_path)

        # Incrementar o contador para a próxima imagem
        self.contador_imagens += 1

        # Após gerar o QR Code, chamar a função de impressão automaticamente
        self.imprimir_etiqueta()

    def update_counter(self, event=None):
        # Obter todas as linhas de códigos de barras inseridos
        codigos_barras = [codigo.strip() for codigo in self.input_text.get("1.0", tk.END).strip().splitlines() if codigo.strip()]

        # Limpar o conjunto de códigos únicos
        self.codigos_unicos.clear()

        # Adicionar os códigos não repetidos ao conjunto de códigos únicos
        for codigo in codigos_barras:
            self.codigos_unicos.add(codigo)

        # Atualizar o label com o número de códigos únicos
        self.counter_label_number.config(text=str(len(self.codigos_unicos)))

        # Resetar o flag de modificação do Text widget
        self.input_text.edit_modified(False)


    def imprimir_etiqueta(self):
        
        if not self.qr_image_path or not os.path.exists(self.qr_image_path):
            messagebox.showerror("Erro", "Nenhum QR Code gerado para imprimir.")
            return

        try:
            self.enviar_para_impressora(self.qr_image_path)
            messagebox.showinfo("Impressão", "QR Code enviado para a impressora de etiqueta.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar para impressão: {e}")

    def enviar_para_impressora(self, image_path):
        # Obtém a impressora padrão
        img = Image.open(image_path)

        # Argox OS-2140 PPLA

        printer_name = "Argox OS-2140 PPLA"

        # Abre um "device context" da impressora
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)

        # Abre a imagem
        img_width, img_height = img.size

        # Dimensões da página de impressão em milímetros
        page_width_mm = 165  # Largura da página em mm
        page_height_mm = 186  # Altura da página em mm

        # Conversão para pixels (assumindo 300 DPI)
        dpi = 450  # Pode ajustar se necessário
        page_width_px = int((page_width_mm / 25.4) * dpi)  # Converter de mm para pixels
        page_height_px = int((page_height_mm / 25.4) * dpi)

        # Calcular as coordenadas para centralizar a imagem
        scale_factor = 2  # Ajustar o fator de escala, se necessário
        left_margin = 300 #(page_width_px - (img_width // scale_factor)) // 2        
        top_margin = 1 #(page_height_px - (img_height // scale_factor)) // 2

        # Iniciar o documento de impressão
        hdc.StartDoc("Etiqueta QR Code")
        hdc.StartPage()

        # Desenhar a imagem na posição centralizada
        dib = ImageWin.Dib(img)
        dib.draw(hdc.GetHandleOutput(), (left_margin, top_margin, left_margin + (img_width // scale_factor), top_margin + (img_height // scale_factor)))

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

    def limpar_tela(self):
        self.input_text.delete("1.0", tk.END)
        self.counter_label_number.config(text="0")
        self.codigos_unicos.clear()
        # self.counter_label.config(text="Total de códigos lidos: 0")
        if self.image_label:
            self.image_label.destroy()  # Remove a imagem atual
        self.qr_image_path = None  # Reseta o caminho do QR Code gerado


def resource_path(relative_path):
    """ Função para obter o caminho correto dos recursos (imagens, ícones, etc.) """
    try:
        base_path = sys._MEIPASS  # Caminho temporário usado pelo PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    root = ctk.CTk()
    app = QRCodeLabelPrinter(root)
    root.mainloop()
    root = tk.Tk()
    # root.title("Montagem de Palete")
    # root.configure(bg=back)
    # app = QRCodeLabelPrinter(root)
    # root.mainloop()

