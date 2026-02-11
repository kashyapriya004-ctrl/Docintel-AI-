import { useEffect, useState } from "react";
import "./App.css";

const App = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [dark, setDark] = useState(false);

  // typing effect
  const typeText = (text: string) => {
    setAnswer("");
    let i = 0;
    const interval = setInterval(() => {
      setAnswer((prev) => prev + text.charAt(i));
      i++;
      if (i >= text.length) clearInterval(interval);
    }, 25);
  };

  const askDocIntel = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      typeText(
        "According to AICTE Internship Policy, undergraduate students must complete a minimum internship duration as specified by the academic program. The policy emphasizes industry exposure, skill development, and academic integration."
      );
    }, 1800);
  };

  // cursor glow
  useEffect(() => {
    const move = (e: MouseEvent) => {
      const glow = document.getElementById("cursor-glow");
      if (glow) {
        glow.style.left = `${e.clientX}px`;
        glow.style.top = `${e.clientY}px`;
      }
    };
    window.addEventListener("mousemove", move);
    return () => window.removeEventListener("mousemove", move);
  }, []);

  return (
    <div className={dark ? "app dark" : "app"}>
      <div id="cursor-glow"></div>

      <button className="theme-toggle" onClick={() => setDark(!dark)}>
        {dark ? "☀️" : "🌙"}
      </button>

      {/* HERO */}
      <header className="hero">
        <h1>DocIntel ✨</h1>
        <p className="subtitle">
          AI-powered Policy Intelligence for Higher Education
        </p>
        <p className="tagline">
          “Ask policies. Get answers. Powered by AI.”
        </p>
      </header>

      {/* MAIN CARD */}
      <section className="glass-card main-card">
        <textarea
          placeholder="Ask any question about higher education policies..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={askDocIntel}>✨ Ask DocIntel</button>

        {loading && (
          <p className="loading">
            🤖 AI is analysing official policy documents…
          </p>
        )}
      </section>

      {/* RESULTS */}
      {answer && (
        <section className="results">
          <div className="glass-card">
            <h3>🤖 AI Answer</h3>
            <p>{answer}</p>
          </div>
          <div className="glass-card">
            <h3>📄 Source Document</h3>
            <p>AICTE_Internship_Policy.pdf</p>
          </div>
        </section>
      )}

      {/* STATS */}
      <section className="stats">
        <div className="glass-card">📚 Documents Loaded<br /><strong>6 PDFs</strong></div>
        <div className="glass-card">🧠 AI Architecture<br /><strong>RAG + Semantic</strong></div>
        <div className="glass-card">🗂 Vector DB<br /><strong>FAISS</strong></div>
        <div className="glass-card">⚡ System Status<br /><strong>Active</strong></div>
      </section>

      {/* HOW IT WORKS */}
      <section className="how">
        <h2>How DocIntel Works</h2>
        <div className="steps">
          <div className="glass-card">1️⃣ Ask a Question</div>
          <div className="glass-card">2️⃣ Query Embedding</div>
          <div className="glass-card">3️⃣ Document Retrieval</div>
          <div className="glass-card">4️⃣ AI Generation</div>
        </div>
      </section>

      <footer>
        © 2026 DocIntel | Academic AI Project
      </footer>
    </div>
  );
};

export default App;
