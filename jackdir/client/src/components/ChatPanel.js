"use client"

// src/components/ChatPanel.js
import { useEffect, useRef, useState } from "react"
import "./ChatPanel.css"

const ChatPanel = ({ selectedPaths, messages, apiKey, setApiKey, model, setModel, isLoading, onSubmit }) => {
  const [input, setInput] = useState("")
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!input.trim()) return

    onSubmit(input)
    setInput("")
  }

  return (
    <div className="chat-container">
      {/* API Key & Model Inputs */}
      <div className="chat-inputs">
        <div className="uk-inline uk-width-1-1 uk-margin-small-bottom">
          <span className="uk-form-icon" uk-icon="icon: lock"></span>
          <input
            className="uk-input uk-form-small"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter API Key"
          />
        </div>
        <div className="uk-inline uk-width-1-1">
          <span className="uk-form-icon" uk-icon="icon: settings"></span>
          <input
            className="uk-input uk-form-small"
            type="text"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="Model (e.g., gpt-4o)"
          />
        </div>
      </div>

      {/* Chat messages container */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">💬</div>
            <p>No messages yet. Start a conversation!</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${
              msg.role === "user" ? "message-user" : msg.role === "error" ? "message-error" : "message-assistant"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {isLoading && (
          <div className="uk-text-center uk-margin-small-top">
            <div uk-spinner="ratio: 0.8"></div>
            <p className="uk-text-small uk-margin-small-top">Thinking...</p>
          </div>
        )}

        {/* Empty div for scrolling to bottom */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="uk-inline uk-width-1-1">
          <input
            className="uk-input uk-border-rounded"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something about the code..."
            disabled={isLoading}
          />
          <button
            className="uk-button uk-button-primary uk-border-rounded uk-position-right"
            type="submit"
            disabled={isLoading}
            style={{ transition: "all 0.2s ease" }}
          >
            <span uk-icon="icon: arrow-right"></span>
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatPanel
