# 🕹️ P5R Translator: Real-Time Screen Translator

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vision%20%26%20Translate-red?style=for-the-badge&logo=google-cloud)](https://cloud.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

## 📖 Visão Geral

O **P5R Translator** é uma ferramenta de tradução de tela em tempo real desenvolvida em Python, projetada especificamente para auxiliar jogadores de **Persona 5 Royal** (e outros jogos com caixas de diálogo fixas) a traduzir textos do inglês para o português instantaneamente.

O software captura uma região específica da tela, utiliza **OCR (Reconhecimento Óptico de Caracteres)** para extrair o texto e a **Google Cloud Translation API** para traduzi-lo, exibindo o resultado em uma sobreposição (overlay) transparente e não intrusiva.

---

## ✨ Funcionalidades

- **🎯 Captura de Região (ROI):** Foca apenas na área de diálogo do jogo, ignorando o resto da tela.
- **🧠 OCR Inteligente:** Utiliza a `Google Cloud Vision API` para uma leitura de texto precisa, mesmo em fundos complexos.
- **⚡ Tradução Instantânea:** Conecta-se à `Google Cloud Translation API` para traduções rápidas e contextuais.
- **👻 Overlay Não-Intrusivo:** A tradução aparece em uma janela transparente "Always-on-Top" sobre o jogo.
- **🛡️ Anti-Espelho:** O sistema oculta automaticamente a janela de tradução antes de capturar a tela, evitando loops de captura.
- **🖱️ Auto-Hide:** A legenda desaparece automaticamente ao clicar fora da área de diálogo, retomando o foco ao jogo.
- **⌨️ Atalhos Globais:** Controle total via teclado sem precisar sair do jogo.

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter:

1. **Python 3.8** ou superior instalado.
2. Uma conta no **Google Cloud Platform (GCP)** com faturamento ativado (necessário para as APIs, mas geralmente dentro do nível gratuito para uso pessoal).
3. O jogo configurado em modo **Janela Sem Bordas (Borderless Window)** ou **Janela** (o modo Tela Cheia Exclusiva pode impedir a sobreposição).

---

## 🚀 Instalação

### 1. Clone ou Baixe o Repositório

```bash
git clone https://github.com/seu-usuario/P5R_Tradutor.git
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

## 🛠️ Configuração da Área de Captura

O programa precisa saber exatamente onde a caixa de diálogo do jogo está na sua tela.

1. Abra o arquivo `main.py`.
2. Localize a seção de coordenadas:
   ```python
   # --- SUAS COORDENADAS ---
   x1 = 870
   y1 = 1400
   x2 = 1904
   y2 = 1607
   ```
3. Ajuste esses valores conforme a resolução do seu monitor e a posição da janela do jogo.

> **Dica:** Você pode usar um script simples com `pynput` ou `pyautogui` para imprimir a posição atual do mouse e descobrir as coordenadas `(x1, y1)` (canto superior esquerdo) e `(x2, y2)` (canto inferior direito) da caixa de diálogo.

---

## ▶️ Como Usar

1. Inicie o programa:
   ```bash
   python main.py
   ```
2. Abra o jogo.
3. Quando aparecer um diálogo que deseja traduzir, use os atalhos:

| Tecla | Ação |
| :--- | :--- |
| **`F10`** | **Traduzir:** Captura a tela, processa e exibe a tradução. |
| **`F9`** | **Alternar Visibilidade:** Esconde ou mostra a janela de tradução manualmente. |
| **`Clique Fora`** | **Esconder:** Clicar fora da área da legenda esconde a tradução automaticamente. |
| **`DELETE`** | **Encerrar:** Fecha o programa imediatamente (Kill Switch). |

---

## 🧠 Arquitetura Técnica

O projeto utiliza concorrência para garantir que a interface não congele durante as requisições de rede.

| Componente | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Frontend** | `tkinter` | Renderiza a janela de sobreposição transparente. |
| **Input Listener** | `pynput` | Monitora teclas (F10, DEL) e cliques do mouse globalmente. |
| **Backend Worker** | `threading` | Executa as tarefas pesadas (I/O, OCR, Tradução) em background. |
| **Screen Capture** | `mss` | Captura de tela ultra-rápida e eficiente. |
| **Comunicação** | `queue` | Sincroniza dados entre as threads de trabalho e a thread da UI. |

---

## ⚠️ Solução de Problemas Comuns

- **Erro de Credenciais:** Certifique-se de que `credentials.json` está na pasta correta e que a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` está sendo definida no código (ou no seu sistema).
- **Janela Preta/Invisível:** Verifique se o jogo está em modo "Janela Sem Bordas". Em "Tela Cheia", o jogo pode desenhar por cima do tradutor.
- **Tradução Estranha:** Verifique se as coordenadas `x1, y1, x2, y2` estão cortando o texto ou pegando elementos gráficos indesejados.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.