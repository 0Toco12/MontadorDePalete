# Gerador e Impressor de QR Code

## Descrição

Este projeto é uma aplicação em Python que permite gerar QR Codes a partir de códigos de barras inseridos pelo usuário. A aplicação possui uma interface gráfica simples para criar QR Codes, visualizar a imagem gerada e imprimir o QR Code. Cada QR Code gerado é salvo como um arquivo de imagem único, e os códigos de barras podem ser exibidos e impressos conforme necessário.

## Requisitos

Para executar este projeto, você precisa das seguintes bibliotecas Python:

- `tkinter` (para a interface gráfica)
- `qrcode` (para gerar QR Codes)
- `Pillow` (para manipulação de imagens)

Instale essas bibliotecas usando o `pip`:

```bash
pip install qrcode[pil] Pillow
```

## Instalação
Clone este repositório para sua máquina local:

```bash
git clone https://github.com/0Toco12/Gerador-QRcode.git
```

Navegue até o diretório do projeto

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso
1. Execute o aplicativo:

  ```bash
  python index.py
  ```
  ou
  ```bash
  py index.py
  ```

2. Gerar um QR Code:

  Insira os códigos de barras na caixa de texto, um por linha.
  Clique em "Gerar QR Code" para criar o QR Code correspondente.

3. Limpar a Tela:
  Clique em "Limpar Tela" para remover o QR Code exibido e limpar a entrada de texto.

4. Imprimir o QR Code:

  Clique em "Imprimir QR Code" para imprimir a imagem do QR Code exibido.

## Arquivos Gerados
  - Imagem do QR Code: Cada QR Code gerado é salvo como um arquivo de imagem com um nome único baseado no timestamp.

## Contribuição

Se você deseja contribuir para este projeto, siga estes passos:

1. Faça um fork deste repositório.
2. Crie uma nova branch (git checkout -b feature/nova-funcionalidade).
3. Faça suas alterações e commit (git commit -am 'Adiciona nova funcionalidade').
4. Envie a branch para o repositório remoto (git push origin feature/nova-funcionalidade).
5. Abra um Pull Request.
