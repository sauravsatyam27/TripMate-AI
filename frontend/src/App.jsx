import { useEffect, useRef, useState } from "react";
import { marked } from "marked";
import html2pdf from "html2pdf.js";

import Background from "./components/Background";
import Hero from "./components/Hero";
import Features from "./components/Features";
import Planner from "./components/Planner";
import Result from "./components/Result";

function App() {
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [answer, setAnswer] = useState("");
  const [threadId, setThreadId] = useState(
    () => localStorage.getItem("travel_thread_id") || null
  );

  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const resultSectionRef = useRef(null);
  const pdfContentRef = useRef(null);

  // --------------------------------------------------
  // Set quick prompt
  // --------------------------------------------------

  const setPrompt = (text) => {
    setUserInput(text);
    setError("");
  };

  // --------------------------------------------------
  // Send message
  // --------------------------------------------------

  const sendMessage = async () => {
    setError("");

    const message = userInput.trim();

    if (!message) {
      setError("Please enter your travel request first.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/api/travel", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          thread_id: threadId,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Something went wrong.");
      }

      setThreadId(data.thread_id);
      localStorage.setItem("travel_thread_id", data.thread_id);

      setAnswer(data.answer);

      // Scroll to result
      setTimeout(() => {
        resultSectionRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Ctrl + Enter
  // --------------------------------------------------

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.ctrlKey && event.key === "Enter") {
        sendMessage();
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [userInput, threadId]);

  // --------------------------------------------------
  // Copy result
  // --------------------------------------------------

  const copyResult = async () => {
    if (!answer) return;

    try {
      const tempElement = document.createElement("div");

      tempElement.innerHTML = marked.parse(answer);

      const text = tempElement.innerText;

      await navigator.clipboard.writeText(text);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1400);
    } catch (err) {
      setError("Could not copy result.");
    }
  };

  // --------------------------------------------------
  // Download PDF
  // --------------------------------------------------

  const downloadPDF = async () => {
    if (!answer || !pdfContentRef.current) {
      setError("No travel plan available to download.");
      return;
    }

    setDownloading(true);
    setError("");

    const options = {
      margin: 0.5,
      filename: "ai-travel-plan.pdf",

      image: {
        type: "jpeg",
        quality: 0.98,
      },

      html2canvas: {
        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff",
      },

      jsPDF: {
        unit: "in",
        format: "a4",
        orientation: "portrait",
      },

      pagebreak: {
        mode: ["avoid-all", "css", "legacy"],
      },
    };

    try {
      await html2pdf()
        .set(options)
        .from(pdfContentRef.current)
        .save();
    } catch (error) {
      setError("Could not download PDF.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#fff8ee] text-[#1b1f3b]">
      <Background />

      <main className="mx-auto w-[calc(100%-32px)] max-w-[1120px] py-14 md:py-20">
        <Hero />

        <Features />

        <Planner
          userInput={userInput}
          setUserInput={setUserInput}
          setPrompt={setPrompt}
          sendMessage={sendMessage}
          loading={loading}
        />

        {answer && (
          <Result
            ref={resultSectionRef}
            answer={answer}
            threadId={threadId}
            copied={copied}
            downloading={downloading}
            copyResult={copyResult}
            downloadPDF={downloadPDF}
            pdfContentRef={pdfContentRef}
          />
        )}

        {error && (
          <section className="mt-[22px] animate-shake rounded-[18px] border-2 border-[#ff6b6b] bg-[#fff0f0] px-5 py-[18px] leading-6 text-[#b42318]">
            {error}
          </section>
        )}
      </main>

      <footer className="px-4 pb-10 pt-[30px] text-center text-[0.92rem] text-[#5d6385]">
        Built with FastAPI, LangGraph, Groq, PostgreSQL, Tavily and AviationStack
      </footer>
    </div>
  );
}

export default App;