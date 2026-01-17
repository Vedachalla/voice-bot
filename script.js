function sendMessage(text=null) {
    const input = document.getElementById("userInput");
    const lang = document.getElementById("lang").value;
    const message = text || input.value.trim();
    if (!message) return;

    append("You", message);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message, language: lang})
    })
    .then(res => res.json())
    .then(data => {
        append("Bot", data.reply);
        if (data.pdf) alert("PDF generated. Click Download Report.");
    });
}

function append(who, msg) {
    const box = document.getElementById("chatLog");
    box.value += `${who}: ${msg}\n`;
    box.scrollTop = box.scrollHeight;
}

function startVoice() {
    const lang = document.getElementById("lang").value === "Telugu" ? "te-IN" : "en-US";
    const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    rec.lang = lang;
    rec.start();
    rec.onresult = e => sendMessage(e.results[0][0].transcript);
}

function downloadPDF() {
    window.location.href = "/download";
}
