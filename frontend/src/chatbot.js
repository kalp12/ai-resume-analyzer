import { AnimatePresence, motion } from 'framer-motion/dist/framer-motion';
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import React from "react";
import { Send, MessageCircle, X, Loader2, Mic, MicOff } from "lucide-react";
import "./chatbot.css"; // Import styles

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);
  const [isOpen, setIsOpen] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const storedMessages = localStorage.getItem("chatMessages");
    if (storedMessages) {
      setMessages(JSON.parse(storedMessages));
    } else {
      setMessages([
        { text: "Hello! How can I assist you today?", sender: "bot", timestamp: new Date() }
      ]);
    }
  }, []);

  useEffect(() => {
    if (chatEndRef.current && isOpen) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const streamResponse = async (fullText) => {
    let responseText = "";
    for (let i = 0; i < fullText.length; i++) {
      responseText += fullText[i];
      await new Promise((resolve) => setTimeout(resolve, 5));
      setMessages((prev) => {
        let updated = [...prev];
        updated[updated.length - 1] = { text: responseText, sender: "bot", timestamp: new Date() };
        return updated;
      });
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessage = { text: input, sender: "user", timestamp: new Date() };
    setMessages([...messages, newMessage]);
    setLoading(true);
    setInput("");

    try {
      const response = await axios.post("http://127.0.0.1:5000/query", { query: input });
      if (response.data && response.data.response) {
        setMessages((prev) => [...prev, { text: "", sender: "bot", timestamp: new Date() }]);
        await streamResponse(response.data.response);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { text: "Error fetching response!", sender: "bot" }]);
    }
    setLoading(false);
  };

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support speech recognition. Please use Chrome or Edge.");
      return;
    }

    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.lang = "en-US";
    recognitionRef.current.interimResults = false;
    recognitionRef.current.maxAlternatives = 1;

    recognitionRef.current.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };

    recognitionRef.current.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      alert("Error occurred during speech recognition. Please try again.");
    };

    recognitionRef.current.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current.start();
    setIsListening(true);
  };

  return (
    <div className="chatbot-container">
      {!isOpen && (
        <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} className="chatbot-button" onClick={() => setIsOpen(true)}>
          <MessageCircle size={28} />
        </motion.button>
      )}

      {isOpen && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 20 }} className="chatbot-window">
          <div className="chatbot-header">
            <div className="flex items-center">
              <MessageCircle className="mr-2" /> Chat Assistant 💬
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white text-xl">
              <X />
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <motion.div key={index} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }} className={`chatbot-message ${msg.sender === "bot" ? "bot" : "user"}`}>
                <p>{msg.text}</p>
                <p className="text-xs opacity-70 text-right mt-1">{msg.timestamp.toLocaleTimeString()}</p>
              </motion.div>
            ))}

            {loading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ repeat: Infinity, duration: 1 }} className="flex space-x-2 items-center text-gray-500">
                <Loader2 className="animate-spin" size={16} />
                <span className="text-sm">Typing...</span>
              </motion.div>
            )}
            <div ref={chatEndRef}></div>
          </div>

          <div className="chatbot-input-container">
            <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} onClick={toggleListening} className="chatbot-voice-button">
              {isListening ? <MicOff /> : <Mic />}
            </motion.button>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} className="chatbot-input" placeholder="Type a message..." />
            <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} onClick={sendMessage} className="chatbot-send-button">
              <Send className="ml-1" size={18} />
            </motion.button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
