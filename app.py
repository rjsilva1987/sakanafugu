import os
import base64
import mimetypes
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB por upload

SAKANA_API_KEY = os.getenv("SAKANA_API_KEY", "")
MODEL = os.getenv("MODEL", "fugu")
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "high")

client = OpenAI(
    base_url="https://api.sakana.ai/v1",
    api_key=SAKANA_API_KEY,
)

SYSTEM_PROMPT = (
    "Você é um assistente inteligente alimentado pelo Sakana Fugu. "
    "Responda sempre no mesmo idioma que o usuário usar. "
    "Seja claro, direto e útil. "
    "Quando receber imagens ou documentos, analise-os com atenção antes de responder."
)

SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
SUPPORTED_DOC_TYPES   = {"application/pdf"}


def file_to_content_block(file):
    """Converte um arquivo enviado num bloco de conteúdo para a API."""
    raw        = file.read()
    b64        = base64.standard_b64encode(raw).decode("utf-8")
    mime, _    = mimetypes.guess_type(file.filename)
    mime       = mime or file.content_type or "application/octet-stream"

    if mime in SUPPORTED_IMAGE_TYPES:
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"},
        }
    elif mime in SUPPORTED_DOC_TYPES:
        # Envia PDF como imagem base64 (modelo visão) — bloco document OpenAI-compat
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"},
        }
    else:
        return None


@app.route("/")
def index():
    return render_template("index.html", model=MODEL)


@app.route("/api/chat", methods=["POST"])
def chat():
    if not SAKANA_API_KEY:
        return jsonify({"error": "SAKANA_API_KEY não configurada no arquivo .env"}), 500

    # ── Suporte a multipart (com arquivos) e JSON puro ────────────────────────
    if request.content_type and "multipart/form-data" in request.content_type:
        import json
        raw_history = request.form.get("messages", "[]")
        try:
            history = json.loads(raw_history)
        except Exception:
            return jsonify({"error": "Campo 'messages' inválido."}), 400

        user_text = request.form.get("text", "").strip()
        files     = request.files.getlist("files")

        # Monta conteúdo multimodal da mensagem atual
        content_parts = []
        for f in files:
            block = file_to_content_block(f)
            if block:
                content_parts.append(block)

        if user_text:
            content_parts.append({"type": "text", "text": user_text})
        elif not content_parts:
            return jsonify({"error": "Envie texto ou arquivo."}), 400

        current_msg = {"role": "user", "content": content_parts}
        messages    = history + [current_msg]

    else:
        data     = request.get_json(silent=True) or {}
        messages = data.get("messages", [])
        if not messages:
            return jsonify({"error": "Nenhuma mensagem enviada."}), 400

    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    def generate():
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=full_messages,
                stream=True,
                extra_body={"reasoning": {"effort": REASONING_EFFORT}},
                timeout=120.0,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content
        except Exception as e:
            yield f"\n\n[Erro: {str(e)}]"

    return Response(stream_with_context(generate()), mimetype="text/plain")


@app.route("/api/config")
def config():
    return jsonify({
        "model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "api_configured": bool(SAKANA_API_KEY),
    })


if __name__ == "__main__":
    print("🐡 Sakana Fugu Chatbot iniciado")
    print(f"   Modelo: {MODEL}  |  Esforço: {REASONING_EFFORT}")
    print("   Acesse: http://localhost:5000")
    app.run(debug=True, port=5000)
