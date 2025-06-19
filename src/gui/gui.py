from flask import Flask, render_template_string, request, redirect, url_for, Response
import subprocess
import os

app = Flask(__name__)

# Paths to the prompt files and the model script
PROMPT_FILES = {
    "character": os.path.expanduser("~/Documents/alp/utubed/character_prompt.txt"),
    "video1": os.path.expanduser("~/Documents/alp/utubed/video1_prompt.txt"),
    "video2": os.path.expanduser("~/Documents/alp/utubed/video2_prompt.txt")
}
MODEL_SCRIPT = os.path.expanduser("~/Documents/alp/utubed/helloworld.py")

# Basic HTML template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LLM Video Generator</title>
</head>
<body>
    <h1>LLM Prompt Editor & Runner</h1>
    <form method="POST" action="/save">
        <h3>Character Prompt</h3>
        <textarea name="character" rows="5" cols="80">{{ character }}</textarea><br>
        <h3>Video 1 Prompt</h3>
        <textarea name="video1" rows="5" cols="80">{{ video1 }}</textarea><br>
        <h3>Video 2 Prompt</h3>
        <textarea name="video2" rows="5" cols="80">{{ video2 }}</textarea><br>
        <input type="submit" value="Save Prompts">
    </form>
    <form method="GET" action="/stream">
        <button type="submit">Run Model Script and Stream Logs</button>
    </form>
    <hr>
    <pre id="log-box">Waiting for output...</pre>

    <script>
    const logBox = document.getElementById("log-box");
    const eventSource = new EventSource("/stream");
    eventSource.onmessage = function(event) {
        logBox.textContent += event.data + "\n";
        logBox.scrollTop = logBox.scrollHeight;
    };
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    character_text = open(PROMPT_FILES["character"]).read() if os.path.exists(PROMPT_FILES["character"]) else ""
    video1_text = open(PROMPT_FILES["video1"]).read() if os.path.exists(PROMPT_FILES["video1"]) else ""
    video2_text = open(PROMPT_FILES["video2"]).read() if os.path.exists(PROMPT_FILES["video2"]) else ""
    return render_template_string(TEMPLATE, character=character_text, video1=video1_text, video2=video2_text)

@app.route("/save", methods=["POST"])
def save():
    with open(PROMPT_FILES["character"], "w") as f:
        f.write(request.form["character"])
    with open(PROMPT_FILES["video1"], "w") as f:
        f.write(request.form["video1"])
    with open(PROMPT_FILES["video2"], "w") as f:
        f.write(request.form["video2"])
    return redirect(url_for("index"))

@app.route("/stream")
def stream():
    def generate():
        process = subprocess.Popen(
            ["python3", MODEL_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            yield f"data: {line.strip()}\n\n"
        process.wait()
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, port=7861, threaded=True)