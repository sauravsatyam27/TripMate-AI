import { forwardRef } from "react";
import { marked } from "marked";

const Result = forwardRef(
  (
    {
      answer,
      threadId,
      copied,
      downloading,
      copyResult,
      downloadPDF,
      pdfContentRef,
    },
    ref
  ) => {
    const html = marked.parse(answer);

    return (
      <section
        ref={ref}
        className="relative mt-[26px] rounded-[28px] bg-white/80 p-5 shadow-[0_22px_60px_rgba(124,92,255,0.2)] backdrop-blur-2xl animate-pop md:p-7"
      >
        {/* Rainbow glow */}
        <div className="pointer-events-none absolute -inset-[3px] -z-10 rounded-[31px] bg-[conic-gradient(from_0deg,#1fc9a0,#38b6ff,#7c5cff,#ff7ac6,#ffc53d,#1fc9a0)] opacity-55 blur-[7px] animate-spinSlow" />

        <div className="mb-[22px] flex flex-col items-start justify-between gap-[18px] md:flex-row">
          <div>
            <h2 className="mb-2 font-['Bricolage_Grotesque'] text-[1.55rem] font-bold">
              Your AI Travel Plan
            </h2>

            <p className="text-[#5d6385]">
              Thread ID: {threadId || "-"}
            </p>
          </div>

          <div className="flex w-full gap-[10px] md:w-auto">
            <button
              onClick={copyResult}
              className="flex-1 rounded-[14px] border-2 border-[#e3e6ff] bg-white px-[18px] py-[10px] font-extrabold text-[#7c5cff] transition hover:-translate-y-0.5 hover:bg-[#f3efff] md:flex-none"
            >
              {copied ? "Copied!" : "Copy"}
            </button>

            <button
              onClick={downloadPDF}
              disabled={downloading}
              className="flex-1 rounded-[14px] bg-[linear-gradient(135deg,#1fc9a0,#38b6ff)] px-[18px] py-[10px] font-extrabold text-white shadow-[0_12px_28px_rgba(31,201,160,0.35)] transition hover:-translate-y-1 hover:scale-105 disabled:cursor-not-allowed disabled:opacity-70 md:flex-none"
            >
              {downloading ? "Preparing PDF..." : "Download PDF"}
            </button>
          </div>
        </div>

        <div
          ref={pdfContentRef}
          className="rounded-[22px] border-t-[6px] border-transparent bg-white p-5 text-[#1f2937] md:p-7"
          style={{
            borderImage:
              "linear-gradient(90deg,#ff6b6b,#ffc53d,#1fc9a0,#38b6ff,#7c5cff,#ff6b6b) 1",
          }}
        >
          <h1 className="mb-5 hidden text-[2rem] font-bold text-[#111827] print:block">
            AI Travel Plan
          </h1>

          <div
            className="travel-markdown overflow-x-auto"
            dangerouslySetInnerHTML={{
              __html: html,
            }}
          />
        </div>
      </section>
    );
  }
);

Result.displayName = "Result";

export default Result;