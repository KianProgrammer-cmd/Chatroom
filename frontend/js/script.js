const socket = io({
    transports: ["polling", "websocket"]
});

const messages = document.getElementById("messages");
const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const status = document.getElementById("status");

const username = localStorage.getItem("chatroom_username") || "کاربر";
const room = "main";

socket.on("connect", () => {
    console.log("CONNECTED:", socket.id);
    status.textContent = "🟢 آنلاین";

    socket.emit("join", {
        username: username,
        room: room
    });
});

socket.on("connect_error", (error) => {
    console.log("SOCKET ERROR:", error.message);
    status.textContent = "⚠️ خطا در اتصال";
});

socket.on("disconnect", () => {
    console.log("DISCONNECTED");
    status.textContent = "🔴 قطع شد";
});

socket.on("message", (data) => {
    console.log("MESSAGE RECEIVED:", data);

    if (!messages) return;

    const message = document.createElement("div");
    message.className = "message";

    const name = document.createElement("div");
    name.className = "name";
    name.textContent = data.username;

    const text = document.createElement("div");
    text.textContent = data.message;

    message.appendChild(name);
    message.appendChild(text);

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
});

function sendMessage() {
    const text = input.value.trim();

    if (!text) return;

    if (!socket.connected) {
        status.textContent = "🔴 اتصال برقرار نیست";
        return;
    }

    console.log("SENDING:", text);

    socket.emit("send_message", {
        username: username,
        message: text,
        room: room
    });

    input.value = "";
    input.focus();
}

if (sendButton) {
    sendButton.addEventListener("click", sendMessage);
}

if (input) {
    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
}