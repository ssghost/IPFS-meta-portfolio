import { useEffect, useState } from "react";

function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "dark";
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="p-2 rounded-md transition-colors bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-600"
    >
      {theme === "dark" ? (
        <svg className="w-4 h-4 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ) : (
        <svg className="w-4 h-4 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      )}
    </button>
  );
}

export default function App() {
  return (
    <main className="min-h-screen font-sans selection:bg-blue-500 selection:text-white bg-gray-50 text-slate-900 dark:bg-[#111927] dark:text-slate-200">
      <nav className="border-b backdrop-blur-md sticky top-0 z-50 bg-white/80 border-slate-200 dark:bg-[#0f1521]/80 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <ThemeToggle />
          <div className="flex items-center gap-2">
            <img 
              src="https://gravatar.com/userimage/100300968/570467f280b16e07a342eef7641735fc.jpeg?size=64" 
              alt="Edmond Avatar" 
              className="w-8 h-8 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700" 
            />
            <span className="font-bold text-lg tracking-tight font-mono">Meta-Portfolio</span>
          </div>
          <div className="text-[10px] font-mono px-2 py-1 rounded bg-slate-900 text-slate-500 border border-slate-800 hidden sm:block">
            LOCAL RAG AGENT
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto mt-10 p-4">
        <div className="flex flex-col items-center mb-10 mt-2 border-b-2 border-slate-200 dark:border-slate-700 pb-6">
          <h1 className="text-3xl font-bold mb-2 tracking-tight text-slate-800 dark:text-slate-100 text-center">
            Meta-Portfolio of Edmond Song
          </h1>
          <h2 className="text-xl font-mono text-slate-500 dark:text-slate-400 text-center">
            Senior DeFi and AI Research Engineer
          </h2>
        </div>

        <p className="mb-6 leading-relaxed text-slate-700 dark:text-slate-300">
          With 8+ years of experience, I bridge Quantitative Analysis with high-assurance Protocol Engineering and advanced AI Agent ecosystems. I specialize in risk modeling for lending markets, cross-chain smart contract architecture across EVM and Solana (SVM), and local-first RAG systems using the Model Context Protocol (MCP), powered by Python, Rust, Solidity, and multiple deep learning frameworks.
        </p>

        <p className="mb-4 font-bold text-slate-800 dark:text-slate-200">
          Welcome to my interactive Meta-Portfolio. Under the hood, this terminal is a fully functional RAG (Retrieval-Augmented Generation) agent powered by my complete project database. You can converse with it directly. Try asking:
        </p>

        <ul className="list-disc pl-6 mb-8 space-y-2 italic text-slate-600 dark:text-slate-400">
          <li>"Show me Edmond Song's Solana lending pool project."</li>
          <li>"Explain the Time-Series ResNet in Edmond Song's Numerai bot."</li>
          <li>"Summarize Edmond Song's EVM smart contract audits."</li>
        </ul>

        <p className="mb-4 text-sm font-mono text-slate-500">
          Click the terminal below and start exploring!
        </p>

        <div className="border rounded-sm p-1 shadow-lg bg-white border-slate-200 dark:bg-slate-800 dark:border-slate-700 mb-10 h-[600px] flex flex-col overflow-hidden relative">
          <iframe 
            src="/terminal.html" 
            className="w-full h-full border-0 bg-transparent"
            title="Interactive RAG Terminal"
          ></iframe>
        </div>

        <div className="border rounded-sm p-6 shadow-lg bg-white border-slate-200 dark:bg-slate-800 dark:border-slate-700">
          <h2 className="text-xs font-bold uppercase tracking-wider mb-4 border-b pb-2 text-slate-500 border-slate-200 dark:text-slate-400 dark:border-slate-700">
            Github Language Charts
          </h2>
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <img 
              src="https://raw.githubusercontent.com/ssghost/ssghost/master/profile-summary-card-output/tokyonight/1-repos-per-language.svg" 
              alt="repos per language" 
              className="w-full md:w-[48%] rounded-sm shadow-sm border border-slate-200 dark:border-slate-700/50" 
            />
            <img 
              src="https://raw.githubusercontent.com/ssghost/ssghost/master/profile-summary-card-output/tokyonight/2-most-commit-language.svg" 
              alt="most commit language" 
              className="w-full md:w-[48%] rounded-sm shadow-sm border border-slate-200 dark:border-slate-700/50" 
            />
          </div>
        </div>
        <footer className="mt-16 pb-8 flex justify-center items-center gap-8 border-t-2 border-slate-200 dark:border-slate-800 pt-8">
          <a 
            href="https://github.com/ssghost" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
            title="GitHub"
          >
            <svg 
              className="w-6 h-6" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.2c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path>
              <path d="M9 18c-4.51 2-5-2-7-2"></path>
            </svg>
          </a>
          <a 
            href="https://hackernoon.com/u/hackersdckei" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="text-slate-400 hover:text-green-600 dark:hover:text-[#00FF00] transition-colors"
            title="HackerNoon"
          >
            <svg 
              className="w-6 h-6" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <circle cx="12" cy="12" r="6" />
              <line x1="12" y1="12" x2="12" y2="6" />
            </svg>
          </a>
          <a 
            href="mailto:ssprof0@gmail.com" 
            className="text-slate-400 hover:text-red-500 dark:hover:text-red-400 transition-colors"
            title="Email Me"
          >
            <svg 
              className="w-6 h-6" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <rect x="2" y="4" width="20" height="16" rx="2" ry="2"></rect>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
            </svg>
          </a>
        </footer>
      </div>
    </main>
  );
}