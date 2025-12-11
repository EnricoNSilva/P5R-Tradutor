# 🕹️ P5R Translator: Real-Time Screen Translator

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vision%20%26%20Translate-red?style=for-the-badge&logo=google-cloud)](https://cloud.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

## 📖 Visão Geral

O **P5R Translator** é uma ferramenta de tradução de tela em tempo real desenvolvida em Python. Projetada originalmente para **Persona 5 Royal**, ela funciona com qualquer jogo ou aplicação que exiba textos na tela.

Diferente de versões anteriores, esta versão 2.0+ opera em **segundo plano** e permite que o usuário **selecione dinamicamente** a área de tradução a qualquer momento, sem necessidade de configuração prévia de coordenadas.

O software utiliza **OCR (Google Cloud Vision)** para ler o texto e **Google Cloud Translate** para traduzi-lo, exibindo o resultado em uma sobreposição (overlay) inteligente que se adapta ao tamanho da sua seleção.

---

## ✨ Funcionalidades

- **🖱️ Seleção Dinâmica ("Circle to Search"):** Ao pressionar o atalho, a tela congela em um overlay transparente, permitindo que você desenhe um retângulo sobre o texto que deseja traduzir.
- **📏 DPI Aware:** Detecta e corrige automaticamente a escala de DPI do Windows, garantindo que a captura de tela seja precisa mesmo em monitores com zoom (125%, 150%, etc.).
- **🅰️ Fonte Adaptativa:** O tamanho da fonte da tradução se ajusta automaticamente para caber perfeitamente dentro da caixa que você desenhou.
- **👻 Overlay Não-Intrusivo:** A tradução aparece flutuando sobre o jogo. Clique fora dela para fechá-la e voltar ao gameplay imediatamente.
- **🧠 OCR Inteligente:** Leitura precisa mesmo em fundos complexos (menus de jogos, balões de fala).
- **🛡️ Workflow Otimizado:** O programa roda invisível na bandeja, ativando apenas quando solicitado.

---

## ⚙️ Pré-requisitos

1. **Python 3.8** ou superior.
2. Conta no **Google Cloud Platform (GCP)** com as APIs `Vision` e `Translation` ativadas (requer `credentials.json`).
3. O jogo configurado em modo **Janela Sem Bordas (Borderless Window)** ou **Janela** (para garantir que o overlay apareça sobre ele).

---

## 🚀 Instalação

### 1. Clone o Repositório

```bash
git clone [https://github.com/seu-usuario/P5R_Tradutor.git](https://github.com/seu-usuario/P5R_Tradutor.git)
cd P5R_Tradutor
```

### 2. Configure o Ambiente Virtual

É recomendável usar um ambiente virtual para isolar as dependências.

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configuração do Google Cloud

Para que o OCR e a Tradução funcionem, você precisa das credenciais do Google:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto.
3. Ative as seguintes APIs:
   - **Cloud Vision API**
   - **Cloud Translation API**
4. Vá em **IAM e Admin** > **Contas de serviço** e crie uma nova conta.
5. Crie uma chave JSON para esta conta e faça o download.
6. Renomeie o arquivo para `credentials.json` e mova-o para a **raiz** deste projeto.

> **Nota:** O arquivo `credentials.json` contém chaves privadas. **Nunca** o compartilhe ou suba para repositórios públicos.

---

## ▶️ Como Usar

O fluxo de uso foi simplificado para máxima imersão:

### Inicie o programa:
 `python main.py`.

O terminal mostrará que o programa está rodando em segundo plano.

### No Jogo:
- **Pressione F10**: A tela entrará em modo de seleção (ficará levemente escurecida).
- **Arraste o Mouse**: Desenhe um retângulo sobre o diálogo em inglês.
- **Solte o Mouse**: O programa processará a imagem e a tradução aparecerá instantaneamente no local selecionado.

### Voltar ao Jogo:
- **Clique Fora**: Basta clicar em qualquer lugar fora da caixa de tradução para escondê-la.

### Encerrar:
- **Pressione DELETE**: Fecha o programa completamente.

## 🧠 Arquitetura Técnica (Modular)

O projeto foi refatorado para ser modular e fácil de manter:

| Arquivo | Responsabilidade |
|---------|------------------|
| `main.py` | Ponto de entrada. Configura o DPI e inicia o App. |
| `overlay.py` | Gerencia a Interface Gráfica (Tkinter), a lógica de seleção de área e o cálculo dinâmico de fonte. |
| `ocr.py` | Camada de serviço que se comunica com as APIs do Google (Vision e Translate). |
| `captura.py` | Responsável por tirar o screenshot da região definida (mss). |
| `input_handlers.py` | Escuta os eventos globais de teclado e mouse (pynput) e os envia para a fila de eventos. |
| `utils.py` | Utilitários de sistema, como a configuração de ctypes para DPI Awareness. |

## ⚠️ Solução de Problemas

### A seleção vermelha não alinha com o mouse:
O fix de DPI deve resolver isso automaticamente. Verifique se o `utils.py` está sendo chamado no início do `main.py`.

### Erro de "Billing" no Terminal:
A API do Google Vision requer que uma conta de faturamento esteja vinculada ao projeto, mesmo para o nível gratuito. Verifique seu console do Google Cloud.

### A tradução não aparece:
Verifique se o jogo está em modo "Tela Cheia Exclusiva". Mude para "Janela Sem Bordas".

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
