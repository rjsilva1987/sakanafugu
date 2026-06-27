# Configuração do Firebase

## 1. Criar projeto no Firebase

1. Acesse https://console.firebase.google.com
2. Clique em **"Criar projeto"**
3. Dê um nome (ex: `fugu-chatbot`) e siga os passos
4. Pode desativar o Google Analytics se quiser

## 2. Ativar o Firebase Storage

1. No menu lateral, clique em **Storage**
2. Clique em **"Começar"**
3. Escolha a região mais próxima (ex: `us-east1` ou `southamerica-east1`)
4. Nas regras de segurança, use esta configuração para teste:

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if true;
    }
  }
}
```

> ⚠️ Para produção, adicione autenticação nas regras.

## 3. Criar a Service Account (credenciais)

1. No console do Firebase, clique na engrenagem ⚙️ → **"Configurações do projeto"**
2. Aba **"Contas de serviço"**
3. Clique em **"Gerar nova chave privada"**
4. Salve o arquivo JSON baixado como `firebase-credentials.json`
   dentro da pasta `fugu-chatbot/`

## 4. Configurar o .env

Copie `.env.example` para `.env` e preencha:

```env
SAKANA_API_KEY=sua_chave_aqui
MODEL=fugu
REASONING_EFFORT=high

FIREBASE_PROJECT_ID=nome-do-seu-projeto
FIREBASE_STORAGE_BUCKET=nome-do-seu-projeto.appspot.com
FIREBASE_CREDENTIALS=firebase-credentials.json
```

O `FIREBASE_STORAGE_BUCKET` aparece na aba Storage do console,
no formato `nome-do-projeto.appspot.com` ou `nome-do-projeto.firebasestorage.app`.

## 5. Instalar dependências e rodar

```bash
.venv\Scripts\activate        # Windows
# ou: source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python app.py
```

Acesse http://localhost:5000 — o indicador verde no header confirma que o Firebase está conectado.
