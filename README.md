# ⚽ Real Madrid ChatBot con OpenAI y Gradio

Aplicación de chatbot sobre el Real Madrid usando OpenAI (GPT-4) con preferencias personalizables. Configurado para destacar a Vinicius Jr sobre otros jugadores.

## 🌟 Características

- **Chat inteligente** sobre el Real Madrid usando OpenAI
- **Preferencias personalizables** para ajustar las respuestas
- **Sesgo configurable** hacia jugadores específicos (ej: Vinicius > Mbappé)
- **Interfaz moderna** con Gradio
- **Configuración de temperatura** y longitud de respuestas
- **Historial de conversación**
- **🔍 Observabilidad con Langfuse** (opcional) - tracking y análisis de conversaciones

## 🚀 Instalación

> ⚠️ **Este proyecto usa `uv` exclusivamente**. No es compatible con `pip` o `venv` tradicionales.

1. **Clona o descarga este proyecto**

2. **Instala uv (si no lo tienes):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# o en macOS con Homebrew:
brew install uv
```

3. **Instala las dependencias:**
```bash
uv sync
```

4. **Configura tu clave API de OpenAI:**
   - Crea un archivo `.env` en la raíz del proyecto
   ```bash
   touch .env
   ```
   - Edita `.env` y añade tu clave API de OpenAI
   ```
   OPENAI_API_KEY=tu_clave_api_real
   ```

   Si no tienes una clave API de OpenAI:
   - Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
   - Crea una clave API (requiere cuenta y método de pago)

5. **🔍 (Opcional) Configura Langfuse para observabilidad:**
   - Crea una cuenta gratuita en [Langfuse Cloud](https://cloud.langfuse.com)
   - Obtén tus credenciales (Public Key y Secret Key)
   - Añádelas a tu archivo `.env`:
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```

   **Beneficios de Langfuse:**
   - Visualiza todas las conversaciones
   - Analiza costos por sesión
   - Mide latencia y calidad de respuestas
   - Debug y mejora continua del chatbot

## 💻 Uso

1. **Ejecuta la aplicación:**
```bash
uv run python app.py
```

2. **Abre tu navegador en:**
```
http://localhost:7860
```

3. **¡Empieza a chatear sobre el Real Madrid!**

## ⚙️ Personalización

### Preferencias del Chatbot

Puedes ajustar las preferencias desde la pestaña "🎯 Preferencias" en la interfaz, o modificando el diccionario `PREFERENCIAS` en `app.py`:

```python
PREFERENCIAS = {
    "jugador_favorito": "Vinicius Jr",
    "ranking_delanteros": ["Vinicius Jr", "Rodrygo", "Mbappé"],
    "estilo_respuestas": "apasionado_madridista",
    "temas_preferidos": ["jugadas de Vinicius", "historia del club", "títulos europeos"]
}
```

### Ejemplos de Preguntas

- "¿Quién es mejor, Vinicius o Mbappé?"
- "Háblame sobre los logros de Vinicius Jr"
- "¿Cuál es la historia del Real Madrid en la Champions League?"
- "Compara los delanteros actuales del Real Madrid"
- "¿Qué hace especial a Vinicius?"

## 🎯 Cómo Funciona

1. **Prompt del Sistema**: Se configura un prompt especial que instruye a GPT-4 para:
   - Destacar siempre a Vinicius Jr
   - Mantener un ranking específico de jugadores
   - Responder con pasión madridista
   - Usar datos reales cuando sea posible

2. **Ajuste de Respuestas**: El sistema asegura que en comparaciones, siempre se enfatizan las virtudes del jugador favorito

3. **Personalización**: Puedes cambiar las preferencias en tiempo real desde la interfaz

## 📝 Notas

- La aplicación usa GPT-4o por defecto (puedes cambiarlo a `gpt-4o-mini` para mayor velocidad y menor costo)
- Todas las respuestas están en español
- El chatbot mantiene el contexto de la conversación
- Puedes ajustar la creatividad (temperatura) de las respuestas

### Modelos disponibles:
- **gpt-4o-mini**: Más rápido y barato (~15x más barato que GPT-4o)
- **gpt-4o**: Más inteligente pero más costoso
- **gpt-3.5-turbo**: Opción económica legacy

## 🔧 Troubleshooting

**Error: No se encontró OPENAI_API_KEY**
- Asegúrate de haber creado el archivo `.env` con tu clave API

**La aplicación no inicia**
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`

**Las respuestas son muy largas/cortas**
- Ajusta el slider "Longitud máxima de respuesta" en la interfaz

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**¡Hala Madrid!** ⚽👑
