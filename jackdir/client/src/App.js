"use client"

// src/App.js
import { useState, useEffect } from "react"
import axios from "axios"
import "./App.css"
import DirectoryTree from "./components/DirectoryTree"
import SelectedItemsTextView from "./components/SelectedItemsTextView"
import ChatPanel from "./components/ChatPanel"
import UIkit from "uikit"
import Icons from "uikit/dist/js/uikit-icons"

UIkit.use(Icons)

function App() {
  const [treeData, setTreeData] = useState(null)
  const [includeHidden, setIncludeHidden] = useState(false)
  const [selectedPaths, setSelectedPaths] = useState(new Set())
  const [chatVisible, setChatVisible] = useState(false)

  // Lifted state from ChatPanel to persist messages and API settings
  const [messages, setMessages] = useState([])
  const [apiKey, setApiKey] = useState("")
  const [model, setModel] = useState("gpt-4o")
  const [isLoading, setIsLoading] = useState(false)

  // Load saved data on initial render
  useEffect(() => {
    // Load API key from localStorage
    const savedApiKey = localStorage.getItem("apiKey")
    if (savedApiKey) {
      setApiKey(savedApiKey)
    }

    // Load model from localStorage
    const savedModel = localStorage.getItem("model")
    if (savedModel) {
      setModel(savedModel)
    }

    // Load chat messages from localStorage
    const savedMessages = localStorage.getItem("chatMessages")
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages))
      } catch (error) {
        console.error("Error parsing saved messages:", error)
      }
    }

    handleScan()
    // eslint-disable-next-line
  }, [includeHidden])

  // Save API key when it changes
  useEffect(() => {
    if (apiKey) {
      localStorage.setItem("apiKey", apiKey)
    }
  }, [apiKey])

  // Save model when it changes
  useEffect(() => {
    if (model) {
      localStorage.setItem("model", model)
    }
  }, [model])

  // Save messages when they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("chatMessages", JSON.stringify(messages))
    } else {
      localStorage.removeItem("chatMessages")
    }
  }, [messages])

  const handleScan = async () => {
    try {
      const response = await axios.post("http://localhost:6789/api/tree", {
        directory: ".",
        include_hidden: includeHidden,
        respect_gitignore: true,
      })
      setTreeData(response.data.tree)
      setSelectedPaths(new Set())
    } catch (error) {
      console.error("Error:", error)
    }
  }

  // Toggle or untoggle a node in the directory tree
  const handleToggle = (node, isChecked) => {
    const newSelected = new Set(selectedPaths)
    // Recursively select or deselect node & children
    const updateNode = (n, checked) => {
      if (checked) {
        newSelected.add(n.path)
      } else {
        newSelected.delete(n.path)
      }
      if (n.children) {
        n.children.forEach((child) => updateNode(child, checked))
      }
    }
    updateNode(node, isChecked)
    setSelectedPaths(newSelected)
  }

  // Copies the selected items to your server (already in your code)
  const handleCopy = async () => {
    try {
      const response = await axios.post("http://localhost:6789/api/copy_selected", {
        selected_paths: Array.from(selectedPaths),
        include_hidden: includeHidden,
        respect_gitignore: true,
      })
      UIkit.notification({
        message: response.data.message,
        status: "success",
        pos: "bottom-right",
        timeout: 3000,
      })
    } catch (error) {
      console.error("Error copying:", error)
    }
  }

  // Handle chat submission (moved from ChatPanel)
  const handleChatSubmit = async (input) => {
    if (!input.trim()) return

    // Append the latest user message
    const newMessages = [...messages, { role: "user", content: input }]
    setMessages(newMessages)

    try {
      setIsLoading(true)
      const response = await axios.post("http://localhost:6789/api/chat", {
        prompt: input,
        api_key: apiKey,
        model: model,
        selected_paths: Array.from(selectedPaths),
        include_hidden: true,
        respect_gitignore: true,
      })

      setMessages([...newMessages, { role: "assistant", content: response.data.response }])
    } catch (error) {
      console.error("Chat error:", error)
      setMessages([...newMessages, { role: "error", content: "Error communicating with AI" }])
    } finally {
      setIsLoading(false)
    }
  }

  // Clear chat history
  const handleClearChat = () => {
    UIkit.modal.confirm("Are you sure you want to clear all chat messages?").then(
      () => {
        setMessages([])
        localStorage.removeItem("chatMessages")
        UIkit.notification({
          message: "Chat history cleared",
          status: "success",
          pos: "bottom-right",
          timeout: 2000,
        })
      },
      () => {
        // User canceled, do nothing
      },
    )
  }

  return (
    <div style={{ height: "100vh", overflow: "hidden", position: "relative" }}>
      <div className="uk-grid uk-grid-collapse" style={{ height: "calc(100vh - 50px)" }}>
        {/* Left: Full directory tree */}
        <div
          className="uk-width-1-2@m uk-width-1-1@s uk-overflow-auto"
          style={{ height: "100%", borderRight: "1px solid #e5e5e5" }}
        >
          <div className="uk-padding-small">
            <h4 className="uk-heading-line uk-text-bold">
              <span>Directory Tree</span>
            </h4>
            <div className="uk-margin-small">
              <label className="uk-flex uk-flex-middle">
                <input
                  className="uk-checkbox uk-margin-small-right"
                  type="checkbox"
                  checked={includeHidden}
                  onChange={(e) => setIncludeHidden(e.target.checked)}
                />
                <span>Include Hidden Files</span>
              </label>
            </div>
            {treeData && <DirectoryTree data={treeData} selectedPaths={selectedPaths} onToggle={handleToggle} />}
          </div>
        </div>

        {/* Right: Selected items */}
        <div className="uk-width-1-2@m uk-width-1-1@s uk-overflow-auto" style={{ height: "100%" }}>
          <div className="uk-padding-small">
            <h4 className="uk-heading-line uk-text-bold">
              <span>Selected Items</span>
            </h4>
            {treeData && <SelectedItemsTextView data={treeData} selectedPaths={selectedPaths} />}
          </div>
        </div>
      </div>

      {/* Copy button in bottom right */}
      <button className="copy-button" onClick={handleCopy}>
        COPY SELECTED
      </button>

      {/* Floating action button for chat */}
      <button
        className="chat-fab"
        onClick={() => setChatVisible(!chatVisible)}
        aria-label="Chat"
        data-has-messages={messages.length > 0 ? "true" : "false"}
      >
        <span uk-icon="icon: comments; ratio: 1.2"></span>
        {messages.length > 0 && <span className="message-count">{messages.length}</span>}
      </button>

      {/* Floating Chat Panel */}
      {chatVisible && (
        <div className="chat-panel-floating">
          <div className="chat-panel-header">
            <h4>Chat</h4>
            <div className="chat-header-actions">
              <button
                className="chat-action-button"
                onClick={handleClearChat}
                aria-label="Clear chat"
                uk-tooltip="Clear chat history"
              >
                <span uk-icon="icon: trash; ratio: 0.8"></span>
              </button>
              <button className="chat-close-button" onClick={() => setChatVisible(false)} aria-label="Close chat">
                <span uk-icon="icon: close; ratio: 0.8"></span>
              </button>
            </div>
          </div>
          <div className="chat-panel-content">
            <ChatPanel
              selectedPaths={Array.from(selectedPaths)}
              messages={messages}
              apiKey={apiKey}
              setApiKey={setApiKey}
              model={model}
              setModel={setModel}
              isLoading={isLoading}
              onSubmit={handleChatSubmit}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default App
