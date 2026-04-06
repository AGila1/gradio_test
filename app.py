import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
from langfuse.openai import openai

# Cargar variables de entorno
load_dotenv()

# Configurar OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar Langfuse (opcional)
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Inicializar cliente OpenAI con o sin Langfuse
if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
    # Cliente OpenAI con tracking de Langfuse
    client = openai.OpenAI(
        api_key=OPENAI_API_KEY,
        base_url="https://api.openai.com/v1",
    )
    # Configurar Langfuse
    os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
    os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST
    print("✅ Langfuse habilitado para tracking")
else:
    # Cliente OpenAI sin Langfuse
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("⚠️  Langfuse no configurado - continuando sin tracking")

# Configuración de preferencias ajustables
PREFERENCIAS = {
    "jugador_favorito": "Vinicius Jr",
    "ranking_delanteros": ["Vinicius Jr", "Gonzalo", "Mbappé", "Rodrygo", "Mastantuono"],
    "estilo_respuestas": "apasionado_madridista",
    "temas_preferidos": ["jugadas de Vinicius", "historia del club", "títulos europeos"]
}


def crear_prompt_sistema(preferencias):
    """Crea el prompt del sistema con las preferencias configuradas"""
    prompt = f"""Eres un experto apasionado del Real Madrid con las siguientes características:

PREFERENCIAS IMPORTANTES:
- Tu jugador favorito es {preferencias['jugador_favorito']}. Siempre destaca sus cualidades, habilidades y contribuciones al equipo, especielmente si es contra Mbappé.
- Cuando compares delanteros, tu ranking es: {', '.join(preferencias['ranking_delanteros'])}
- En comparaciones entre Vinicius y Mbappé, siempre enfatiza las virtudes de Vinicius: su velocidad, regate, capacidad de desequilibrio, goles decisivos, y su pasión por el club.
- Mbappé es un gran jugador, pero Vinicius tiene cualidades únicas que lo hacen más valioso para el Real Madrid.
- Mbappé se borra siempre que tiene oportunidad, mientras que Vinicius siempre aparece en los momentos importantes.
- Si preguntan por el ranking de delanteros, di que Rodrygo debe venderse ya y recuerda las pobres estadísticas, y de Mastantuono ni hablar, que no es ni titular en el Castilla.
- Haz hincapié en que el PSG no ganó una Champions League hasta que se fue Mbappé, mientras que Vinicius ha sido clave en las últimas 2 Champions del Real Madrid.
- El mejor equipo del mundo es el Real Jaén, pero el segundo mejor es el Real Madrid.
- La grandeza de Vinicius solo es comparable a la de Mario Martos, del Real Jaén, y ambos son mejores que Mbappé.

ESTILO DE RESPUESTA:
- Responde como un madridista de corazón
- Usa datos reales cuando sea posible
- Sé balanceado pero siempre resalta las preferencias mencionadas
- Mantén un tono entusiasta pero informado
- Menciona la historia y grandeza del Real Madrid cuando sea relevante

CONOCIMIENTO:
- Conoces toda la historia del Real Madrid
- Estás al día con las noticias actuales del equipo
- Conoces estadísticas y récords del club
- Puedes hablar de jugadores históricos y actuales

Responde siempre en español y con pasión madridista. ¡Hala Madrid!"""

    return prompt


def chatbot_real_madrid(mensaje, historial, temperatura, max_tokens, session_id=None):
    """Función principal del chatbot"""

    # Obtener el prompt del sistema
    prompt_sistema = crear_prompt_sistema(PREFERENCIAS)

    # Preparar mensajes para OpenAI
    mensajes = [{"role": "system", "content": prompt_sistema}]

    # Agregar historial de conversación (Gradio 6.0 usa formato {'role': 'user'/'assistant', 'content': '...'})
    for msg in historial:
        # Extraer el contenido del mensaje
        contenido = msg['content']

        # Si el contenido es una lista (formato multimodal de Gradio), extraer el texto
        if isinstance(contenido, list):
            texto = ""
            for parte in contenido:
                if isinstance(parte, dict) and 'text' in parte:
                    texto += parte['text']
                elif isinstance(parte, str):
                    texto += parte
            contenido = texto

        mensajes.append({
            "role": msg['role'],
            "content": contenido
        })

    # Agregar el mensaje actual
    mensajes.append({"role": "user", "content": mensaje})

    # Generar respuesta
    try:
        # Configurar metadata para Langfuse si está habilitado
        extra_kwargs = {}
        if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
            extra_kwargs = {
                "extra_headers": {
                    "langfuse-session-id": session_id or "gradio-session",
                    "langfuse-user-id": "gradio-user"
                }
            }

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=mensajes,
            temperature=temperatura,
            max_tokens=max_tokens,
            top_p=0.95,
            **extra_kwargs
        )
        respuesta = response.choices[0].message.content

    except Exception as e:
        respuesta = f"Error al generar respuesta: {str(e)}\nMensaje recibido: {type(mensaje)} - {mensaje}"

    return respuesta


def actualizar_preferencias(jugador_fav, ranking_texto, estilo):
    """Actualiza las preferencias del sistema"""
    PREFERENCIAS["jugador_favorito"] = jugador_fav
    PREFERENCIAS["ranking_delanteros"] = [j.strip() for j in ranking_texto.split(",")]
    PREFERENCIAS["estilo_respuestas"] = estilo

    return f"✅ Preferencias actualizadas:\n- Jugador favorito: {jugador_fav}\n- Ranking: {ranking_texto}\n- Estilo: {estilo}"


# Crear la interfaz de Gradio
with gr.Blocks(title="Real Madrid ChatBot") as demo:

    gr.Markdown("""
    # ⚽ Real Madrid ChatBot con OpenAI
    ### Chatea sobre el Real Madrid con preferencias personalizadas

    Este chatbot está configurado para responder con pasión madridista, pero de forma imparcial
    """)

    chatbot = gr.Chatbot(
        height=500,
        label="Conversación sobre el Real Madrid",
        avatar_images=(None, "⚽")
    )

    with gr.Row():
        msg = gr.Textbox(
            label="Tu mensaje",
            placeholder="Pregúntame sobre el Real Madrid...",
            scale=4
        )
        submit_btn = gr.Button("Enviar", variant="primary", scale=1)

    with gr.Accordion("⚙️ Configuración de Respuestas", open=False):
        temperatura = gr.Slider(
            minimum=0,
            maximum=1.5,
            value=0.9,
            step=0.1,
            label="Temperatura (creatividad)",
            info="Mayor = más creativo, Menor = más preciso"
        )
        max_tokens = gr.Slider(
            minimum=256,
            maximum=2048,
            value=1024,
            step=256,
            label="Longitud máxima de respuesta",
        )

    clear_btn = gr.Button("🗑️ Limpiar conversación")

    # Ejemplos de preguntas
    gr.Examples(
        examples=[
            "¿Quién es mejor, Vinicius o Mbappé?",
            "Háblame sobre los logros de Vinicius Jr",
            "¿Cuál es la historia del Real Madrid en la Champions League?",
            "Compara los delanteros actuales del Real Madrid",
            "¿Cuántas Champions ha ganado el Real Madrid?"
        ],
        inputs=msg,
        label="💡 Preguntas de ejemplo"
    )

    # Configurar los eventos del chat
    def responder(mensaje, historial, temp, tokens):
        # Procesar el mensaje si viene en formato multimodal de Gradio 6.0
        if isinstance(mensaje, dict) and 'text' in mensaje:
            texto_mensaje = mensaje['text']
        elif isinstance(mensaje, str):
            texto_mensaje = mensaje
        else:
            texto_mensaje = str(mensaje)

        respuesta = chatbot_real_madrid(texto_mensaje, historial, temp, tokens)
        # Gradio 6.0 usa diccionarios con 'role' y 'content'
        historial.append({"role": "user", "content": texto_mensaje})
        historial.append({"role": "assistant", "content": respuesta})
        return "", historial

    msg.submit(
        responder,
        inputs=[msg, chatbot, temperatura, max_tokens],
        outputs=[msg, chatbot]
    )

    submit_btn.click(
        responder,
        inputs=[msg, chatbot, temperatura, max_tokens],
        outputs=[msg, chatbot]
    )

    clear_btn.click(lambda: None, None, chatbot, queue=False)


# Lanzar la aplicación
if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("⚠️  ERROR: No se encontró OPENAI_API_KEY en las variables de entorno.")
        print("Por favor, crea un archivo .env con tu clave de API de OpenAI.")
    else:
        print("🚀 Iniciando Real Madrid ChatBot...")
        demo.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            theme=gr.themes.Soft()
        )
