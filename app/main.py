<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniMind Hub</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 700px; background: #1e293b; border-radius: 12px; padding: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 20px; }
        .chat-box { height: 350px; overflow-y: auto; border: 1px solid #334155; background: #0f172a; border-radius: 8px; padding: 15px; margin-bottom: 20px; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 10px 14px; border-radius: 8px; max-width: 80%; word-wrap: break-word; }
        .user-msg { background: #2563eb; color: white; align-self: flex-end; }
        .ai-msg { background: #334155; color: white; align-self: flex-start; }
        .input-area { display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 6px; border: 1px solid #334155; background: #1e293b; color: white; outline: none; }
        button { background: #10b981; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        select { padding: 12px; border-radius: 6px; background: #334155; color: white; border: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h2>🧠 UniMind Hub</h2>
        <select id="modelSelect">
            <option value="ollama/llama3.2">Gemini Instance</option>
            <option value="ollama/llama3.2">Claude Instance</option>
            <option value="ollama/llama3.2">ChatGPT Instance</option>
        </select>
    </div>
    <div class="chat-box" id="chatBox">
        <div class="msg ai-msg">UniMind local memory mesh online. State a context loop or ask a question.</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Type your prompt...">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>
<script>
    async function sendMessage() {
        const input = document.getElementById('userInput');
        const box = document.getElementById('chatBox');
        const model = document.getElementById('modelSelect');
        const text = input.value.trim();
        if(!text) return;

        box.innerHTML += `<div class="msg user-msg">${text}</div>`;
        input.value = '';

        try {
            const response = await fetch('/chat/completions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: "viru_375",
                    session_id: "unimind_demo",
                    model_choice: model.value,
                    user_prompt: text
                })
            });
            const data = await response.json();
            box.innerHTML += `<div class="msg ai-msg"><b>[${model.options[model.selectedIndex].text}]:</b> ${data.ai_reply}</div>`;
        } catch(e) {
            box.innerHTML += `<div class="msg ai-msg" style="color:#ef4444;">Network connection fault. Verify backend process terminal state.</div>`;
        }
        box.scrollTop = box.scrollHeight;
    }
</script>
</body>
</html>