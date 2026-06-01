import { useState } from "react";
import api from "./api";

function App() {

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const sessionId = "ajmal-session";

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMessage = {
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {

      const res = await api.post("/chat", {
        session_id: sessionId,
        message,
      });

      const aiMessage = {
        role: "assistant",
        content: res.data.response,
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {

      console.log(error);

      const errorMessage = {
        role: "assistant",
        content: "Something went wrong",
      };

      setMessages((prev) => [...prev, errorMessage]);
    }

    setMessage("");
  };

  return (
    <div className="container">

      <h1>Multi Turn AI Agent</h1>

      <div className="chat-box">

        {
          messages.map((msg, index) => (
            <div
              key={index}
              className={
                msg.role === "user"
                  ? "message user"
                  : "message assistant"
              }
            >
              <strong>{msg.role}</strong>

              <p>{msg.content}</p>
            </div>
          ))
        }

      </div>

      <div className="input-box">

        <input
          type="text"
          placeholder="Type message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

    </div>
  );
}

export default App;