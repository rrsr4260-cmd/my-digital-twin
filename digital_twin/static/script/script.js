function sendMessage() {
    let msgInput = document.getElementById("message");
    let msg = msgInput.value.trim();

    if (msg === "") return;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: msg
        })
    })
    .then(res => res.json())
    .then(data => {
        let chatBox = document.getElementById("chatBox");

        chatBox.innerHTML += "<div><b>You:</b> " + msg + "</div>";
        chatBox.innerHTML += "<div><b>Twin:</b> " + data.reply + "</div><br>";

        chatBox.scrollTop = chatBox.scrollHeight;
        msgInput.value = "";

        if (data.audio) {
            let audio = new Audio(data.audio + "?t=" + new Date().getTime());
            audio.play().catch(err => console.log("Audio play error:", err));
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}

function startVoice() {
    let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech recognition not supported in this browser.");
        return;
    }

    let recognition = new SpeechRecognition();
    recognition.lang = "en-IN";

    recognition.onresult = function(e) {
        let text = e.results[0][0].transcript;
        document.getElementById("message").value = text;
        sendMessage();
    };

    recognition.start();
}