import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const sendRequest = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: input }),
      });

      const data = await res.json();
      setResponse(data.response || data.error);
    } catch (error) {
      setResponse("Backend not running");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI Testing Tool</h2>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter text"
      />

      <button onClick={sendRequest}>Send</button>

      <p><b>Response:</b> {response}</p>
    </div>
  );
}

export default App;