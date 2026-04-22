"""
multimodal/audio.py
────────────────────
Web Speech API integration for text-to-speech output.

The student reads the hint first, then clicks Listen to hear it spoken aloud.
Implemented via browser-native Web Speech API — zero cost, zero API calls.
Eyes-on-code workflow: upload screenshot → receive hint → listen while coding.

This is injected as HTML into Streamlit components.
"""


def get_speech_html(text: str, button_label: str = "🔊 Listen") -> str:
    """
    Returns HTML that renders a Listen button using the Web Speech API.
    The text is spoken at 0.9x speed for better comprehension.
    """
    # Escape quotes and newlines for safe JS embedding
    safe_text = (text
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("'", "\\'"))

    return f"""
<div style="margin-top: 8px;">
  <button
    onclick="speakText_{hash(text) & 0xFFFFFF}()"
    style="
      background: transparent;
      border: 1px solid #4B6EAF;
      color: #4B6EAF;
      padding: 4px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85em;
      font-family: sans-serif;
    "
  >
    {button_label}
  </button>
  <button
    onclick="stopSpeech()"
    style="
      background: transparent;
      border: 1px solid #888;
      color: #888;
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85em;
      font-family: sans-serif;
      margin-left: 6px;
    "
  >
    ⏹ Stop
  </button>
</div>

<script>
function speakText_{hash(text) & 0xFFFFFF}() {{
  if ('speechSynthesis' in window) {{
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance("{safe_text}");
    utterance.rate  = 0.88;
    utterance.pitch = 1.0;
    utterance.lang  = 'en-US';
    window.speechSynthesis.speak(utterance);
  }} else {{
    alert('Your browser does not support text-to-speech.');
  }}
}}
function stopSpeech() {{
  if ('speechSynthesis' in window) {{
    window.speechSynthesis.cancel();
  }}
}}
</script>
"""


def get_speech_check_html() -> str:
    """Returns HTML that checks if speech synthesis is available."""
    return """
<script>
if (!('speechSynthesis' in window)) {
  document.write('<p style="color: orange; font-size: 0.8em;">⚠ Text-to-speech not available in your browser.</p>');
}
</script>
"""
