import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk, ImageWin
import os
import sys
import win32print
import win32ui
import tempfile
from datetime import datetime
from ctypes import windll


class QRCodeLabelPrinter:

    global back
    back = "#DCDCDC"
    
    def __init__(self, root):
        self.codigos_unicos = set()
        self.contador_codigos = 0
        self.root = root
        self.root.title("Montador de Palete")

        icon = ImageTk.PhotoImage(file='logo.png')
        self.root.iconphoto(False, icon)

        # Adicionando o título
        self.title_label = tk.Label(self.root, text="Montagem de Palete", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="nsew")
        self.title_label.configure(bg=back)

        # Configurar o layout da janela usando grid
        self.root.geometry("800x400")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Frame para a área de texto (à esquerda)
        self.frame_text = tk.Frame(self.root)
        self.frame_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_text.configure(bg=back)

        # Label e área de texto
        self.input_label = tk.Label(self.frame_text, text="Insira os códigos de barras:", font=("Roboto", 20, "bold"))
        self.input_label.pack(pady=10)
        self.input_label.configure(bg=back)

        self.input_text = tk.Text(self.frame_text, height=20, width=50)
        self.input_text.pack(pady=10)
        self.input_text.configure(bg="#C0C0C0")

        self.frame_text = tk.Frame(self.root)
        self.frame_text.grid (row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_text.configure(bg=back)

        # Contador de códigos de barras lidos
        self.counter_label = tk.Label(self.frame_text, text="Total de códigos lidos: 0", font=("Roboto", 14, "bold"), width=30)
        self.counter_label.pack(pady=(200, 10))
        self.counter_label.configure(bg=back)

        # Vincular o evento de mudança de conteúdo no campo de texto
        self.input_text.bind("<<Modified>>", self.update_counter)

        # Frame para os botões (centro)
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.frame_buttons.configure(bg="#D3D3D3")
        
        # Botão de gerar QR Code
        self.generate_button = tk.Button(self.frame_buttons, text="Gerar QR Code", command=self.gerar_qr_code, width=30, height=10, font=("Roboto", 15, "bold"), bg="#006400", fg="#f0f0f0")
        self.generate_button.pack(pady=(50, 20))

        # Botão para limpar a tela
        self.clear_button = tk.Button(self.frame_buttons, text="Limpar Tela", command=self.limpar_tela, width=30, font=("Roboto", 15, "bold"), bg="#006400", fg="#f0f0f0")
        self.clear_button.pack(pady=20)

        # Frame para a imagem (à direita)
        self.frame_image = tk.Frame(self.root)
        self.frame_image.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Ocupa as 3 colunas
        self.frame_image.configure(bg=back)

        # Adicionar a imagem estática
        self.display_image()

        self.contador_imagens = 1
        self.qr_image_path = None

    def display_image(self):
        # Carregar a imagem do caminho especificado (use o caminho absoluto ou relativo correto)
        image_path = resource_path('img.png')  # Verifique se este caminho está correto!

        try:
            # Verifique se o arquivo de imagem existe
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Imagem não encontrada no caminho: {image_path}")

            # Carregar e redimensionar a imagem
            img = Image.open(image_path)
            img = img.resize((400, 200), Image.Resampling.LANCZOS)  # Redimensiona a imagem para 200x200
            img_tk = ImageTk.PhotoImage(img)

            # Adiciona a imagem a um label e a exibe
            self.image_label = tk.Label(self.frame_image, image=img_tk)
            self.image_label.image = img_tk  # Necessário para o Tkinter manter a referência da imagem
            self.image_label.pack(pady=10)
            self.image_label.configure(bg=back)
        except FileNotFoundError as fnf_error:
            messagebox.showerror("Erro", str(fnf_error))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

    def gerar_qr_code(self):

        codigos_barras = self.input_text.get("1.0", tk.END).strip().splitlines()

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

        #----------------------------------------------------------------------------------

        # Obter os códigos de barras da entrada de texto
        # codigos_barras = self.input_text.get("1.0", tk.END).strip().splitlines()

        # if not codigos_barras:
        #     messagebox.showerror("Erro", "Insira ao menos um código de barras.")
        #     return

        # # Filtrar apenas códigos de barras novos
        # novos_codigos = [codigo for codigo in codigos_barras if codigo not in self.codigos_unicos]

        # # if not novos_codigos:
        # #     messagebox.showinfo("Aviso", "Todos os códigos já foram inseridos anteriormente.")
        # #     return

        # # Adicionar os novos códigos à lista de únicos
        # self.codigos_unicos.update(novos_codigos)

        # # Atualizar o contador
        # self.contador_codigos = len(self.codigos_unicos)
        # self.contador_label.config(text=f"Total de códigos lidos: {self.contador_codigos}")

        # # Concatenar os novos códigos em uma única string
        # dados = "\n".join(novos_codigos)

        # # Gerar o QR Code com os novos códigos
        # qr = qrcode.QRCode(
        #     version=1,
        #     error_correction=qrcode.constants.ERROR_CORRECT_L,
        #     box_size=10,
        #     border=4,
        # )
        # qr.add_data(dados)
        # qr.make(fit=True)

        # # Criar a imagem do QR Code e salvar com nome personalizado e data
        # img = qr.make_image(fill="black", back_color="white")
        # data_atual = datetime.now().strftime("%d-%m-%Y")  # Obtém a data no formato dd-mm-yyyy
        # self.qr_image_path = f"p{self.contador_codigos}-{data_atual}.png"
        # img.save(self.qr_image_path)

        # # Após gerar o QR Code, chamar a função de impressão automaticamente
        # self.imprimir_etiqueta()

    def update_counter(self, event=None):
        # Contar o número de linhas com códigos inseridos
        num_codigos = len(self.input_text.get("1.0", tk.END).strip().splitlines())
        self.counter_label.config(text=f"Total de códigos lidos: {num_codigos}")
        self.input_text.edit_modified(False)  # Reset the modified flag


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
        # img = Image.open(image_path)

        # # Argox OS-2140 PPLA

        # printer_name = "OneNote (Desktop)"

        # # Abre um "device context" da impressora
        # hdc = win32ui.CreateDC()
        # hdc.CreatePrinterDC(printer_name)

        # # Abre a imagem
        # img_width, img_height = img.size

        # # Definir o tamanho da imagem para a impressora
        # # Fator de escala para garantir que a imagem se ajuste ao papel da impressora
        # scale_factor = 2

        # # Definir o tamanho da página da impressora
        # hdc.StartDoc("Etiqueta QR Code")
        # hdc.StartPage()

        # dib = ImageWin.Dib(img)
        # dib.draw(hdc.GetHandleOutput(), (450, 450, img_width // scale_factor, img_height // scale_factor))

        # hdc.EndPage()
        # hdc.EndDoc()
        # hdc.DeleteDC()
        #------------------------------------------------------------------------------------------------------------------
        # Abra a imagem
        img = Image.open(image_path)

        # Configurar a impressora padrão
        impressora_padrao = "Argox OS-2140 PPLA"

        # Obter o HDC da impressora
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(impressora_padrao)

        # Configurar as preferências de impressão
        hPrinter = win32print.OpenPrinter(impressora_padrao)
        devmode = win32print.GetPrinter(hPrinter, 2)["pDevMode"]

        # Ajustar preferências de impressão
        devmode.PaperSize = 9  # A4
        devmode.Orientation = 1  # Retrato
        devmode.PrintQuality = -3  # Alta qualidade
        devmode.Copies = 2  # Número de cópias
        devmode.Scale = 100  # Ajustar para caber
        devmode.YResolution = 600  # Resolução vertical
        devmode.XResolution = 600  # Resolução horizontal

        # Aplicar as configurações
        win32print.SetPrinter(hPrinter, 2, {"pDevMode": devmode}, 0)
        win32print.ClosePrinter(hPrinter)

        # Iniciar o documento de impressão
        hdc.StartDoc("Impressão de Imagem")
        hdc.StartPage()

        # Obter as dimensões da imagem
        width, height = img.size

        # Converter a imagem para um formato compatível com o HDC
        dib = ImageWin.Dib(img)

        # Ajustar a imagem para caber na página
        dib.draw(hdc.GetHandleOutput(), (0, 0, width, height))

        # Finalizar a impressão
        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

    def limpar_tela(self):
        # Limpar o campo de texto
        self.input_text.delete("1.0", tk.END)

def resource_path(relative_path):
    """Obter o caminho absoluto do recurso, funciona para o executável ou para o script"""
    try:
        # Quando empacotado com PyInstaller, o atributo _MEIPASS contém o caminho temporário
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Montagem de Palete")
    root.configure(bg=back)
    app = QRCodeLabelPrinter(root)
    root.mainloop()