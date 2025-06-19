from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Prompt GUI</title></head>
<body>
  <h2>Video Prompt Submission</h2>
  <form action="/run" method="post">
    <label>Character Prompt:</label><br>
    <textarea name="character" rows="2" cols="60"></textarea><br><br>
    <label>Scene 1 Prompt:</label><br>
    <textarea name="prompt1" rows="2" cols="60"></textarea><br><br>
    <label>Scene 2 Prompt:</label><br>
    <textarea name="prompt2" rows="2" cols="60"></textarea><br><br>
    <button type="submit">Generate</button>
  </form>
</body>
</html>
"""

@app.route("/")
def form():
    return render_template_string(HTML)

@app.route("/run", methods=["POST"])
def run():
    character = request.form["character"]
    prompt1 = request.form["prompt1"]
    prompt2 = request.form["prompt2"]

    with open("info.txt", "w") as f:
        f.write(f"character:{character}|prompt1:{prompt1}|prompt2:{prompt2}")
    
    os.system("python3 /home/opc/utubed/helloworld.py")  # adjust path if needed
    return "Submitted and started video generation."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
