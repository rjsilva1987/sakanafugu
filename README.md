# 🐡 Fugu Chatbot

Chatbot web com Python + Flask usando a API **Sakana Fugu** — compatível com o SDK OpenAI.

## Pré-requisitos

- Python 3.10+
- Conta e chave de API em [console.sakana.ai](https://console.sakana.ai)
- VS Code (recomendado)

## Setup rápido

### 1. Clone / abra o projeto no VS Code

```bash
code fugu-chatbot/
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave de API

Copie o arquivo de exemplo e preencha com sua chave:

```bash
cp .env.example .env
```

Edite `.env`:

```env
SAKANA_API_KEY=sk-...sua_chave_aqui...
MODEL=fugu           # ou fugu-ultra
REASONING_EFFORT=high  # ou xhigh
```

### 5. Rode o servidor

```bash
python app.py
```

Acesse no navegador: **http://localhost:5000**

## Estrutura do projeto

```
fugu-chatbot/
├── app.py              # Backend Flask + integração Sakana API
├── requirements.txt    # Dependências Python
├── .env.example        # Modelo de variáveis de ambiente
├── .env                # Sua chave (não versionar!)
├── .gitignore
└── templates/
    └── index.html      # Interface web do chat
```

## Modelos disponíveis

| Modelo       | Descrição                                      |
|-------------|------------------------------------------------|
| `fugu`       | Balanceado — ideal para uso cotidiano           |
| `fugu-ultra` | Alta performance — tarefas complexas e longas   |

## Esforço de raciocínio

| Valor   | Quando usar                         |
|---------|-------------------------------------|
| `high`  | Maioria das tarefas (padrão)        |
| `xhigh` | Problemas muito difíceis (mais lento)|

## Dicas de uso no VS Code

- Instale a extensão **Python** da Microsoft
- Use `Ctrl+Shift+~` para abrir o terminal integrado
- A extensão **REST Client** ajuda a testar a API diretamente
