import React, { useState } from "react";
import axios from "axios";
// import "./ResumeChecker.css";

export default function ResumeChecker() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const analyzeResume = async () => {
    if (!file) return alert("Please upload a resume!");

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/check_resume", formData);
      setResult(response.data);
    } catch (error) {
      alert("Error analyzing resume.");
    }
    
    setLoading(false);
  };


  return (
    <div style={{
      backgroundColor: "lightblue",
      minHeight: "90vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
    }}>
      <div style={{
        backgroundColor: "white",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
        maxWidth: "500px",
        textAlign: "center"
      }}>
        <h1>📄 ATS Resume Checker</h1>
        <input type="file" onChange={handleFileUpload} accept=".pdf,.docx" style={{ marginBottom: "10px" }} />
        <button onClick={analyzeResume} disabled={loading} style={{
          backgroundColor: "lightgreen",
          color: "black",
          padding: "10px 20px",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          marginBottom: "100px"
        }}>
          {loading ? "Analyzing..." : "Check Resume"}
        </button>

        {result && (
          <div className="result">
            <h2>✅ ATS Score: {result.readability_score}%</h2>
            <h3>⚠️ Formatting Issues:</h3>
            <ul>{result.format_issues.map((issue, index) => <li key={index}>{issue}</li>)}</ul>
            <h3>📌 Missing Sections:</h3>
            <ul>{result.missing_sections.map((section, index) => <li key={index}>{section}</li>)}</ul>
            <h3>💡 Suggestions:</h3>
            <ul>{result.suggestions.map((tip, index) => <li key={index}>{tip}</li>)}</ul>
          </div>
        )}
      </div>
    </div>
  );
}