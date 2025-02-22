import React from "react";
import Chatbot from "./chatbot";
import ResumeChecker from "./ResumeChecker";


function App() {
  return (
    <div style={{
      backgroundColor: "lightgreen",
      alignItems: "center",
      textAlign: "center",
    }}>
      <h1 style={{ color: "#333", fontSize: "2rem", marginBottom: "20px" }}>Welcome to Resume ATS Checker</h1>
      
        <ResumeChecker />
        <Chatbot />
    </div>
    
  );
}

export default App;
