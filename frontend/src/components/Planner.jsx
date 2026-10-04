function Planner({
  userInput,
  setUserInput,
  setPrompt,
  sendMessage,
  loading,
}) {
  const quickPrompts = [
    {
      label: "🗾 Japan Trip",
      text: "Plan a complete 7 days Japan trip from Brazil including flights, hotels and sightseeing under 2 lakhs.",
      color: "bg-[#ff6b6b]",
    },
    {
      label: "🏙️ Dubai Trip",
      text: "Plan a 5 days Dubai trip from Delhi with flights, hotels and sightseeing.",
      color: "bg-[#f0a500]",
    },
    {
      label: "🏖️ Thailand Trip",
      text: "Plan a 7 days Thailand trip from Brazil with budget hotels and sightseeing.",
      color: "bg-[#1fc9a0]",
    },
    {
      label: "🌍 Global Flights",
      text: "Give me all country flight info.",
      color: "bg-[#38b6ff]",
    },
  ];

  return (
    <section className="relative rounded-[28px] bg-white/80 p-5 shadow-[0_22px_60px_rgba(124,92,255,0.2)] backdrop-blur-2xl animate-pop md:p-7">
      {/* Rainbow glow */}
      <div className="pointer-events-none absolute -inset-[3px] -z-10 rounded-[31px] bg-[conic-gradient(from_0deg,#ff6b6b,#ffc53d,#1fc9a0,#38b6ff,#7c5cff,#ff7ac6,#ff6b6b)] opacity-70 blur-[7px] animate-spinSlow" />

      {/* Rainbow top ribbon */}
      <div className="absolute left-7 right-7 top-0 h-[5px] rounded-b-lg bg-[linear-gradient(90deg,#ff6b6b,#ffc53d,#1fc9a0,#38b6ff,#7c5cff,#ff6b6b)] bg-[length:300%_100%] animate-shine" />

      <div className="mb-[22px] flex flex-col items-start justify-between gap-[18px] md:flex-row">
        <div>
          <h2 className="mb-2 font-['Bricolage_Grotesque'] text-[1.55rem] font-bold">
            Where do you want to go?
          </h2>

          <p className="leading-6 text-[#5d6385]">
            Example: Plan a complete 7 days Japan trip from Bhutan under 2
            lakhs.
          </p>
        </div>

        <div className="flex items-center gap-2 whitespace-nowrap rounded-full bg-[#dcfff3] px-[14px] py-2 text-[0.85rem] font-bold text-[#0a8a69]">
          <span className="h-[9px] w-[9px] rounded-full bg-[#1fc9a0] animate-pingCustom" />
          Online
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-[1fr_auto]">
        <textarea
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Plan a complete 7 days Japan trip including flights, hotels and sightseeing under 2 lakhs..."
          className="min-h-[150px] w-full resize-y rounded-[22px] border-2 border-[#e3e6ff] bg-white p-5 text-base leading-[1.6] text-[#1b1f3b] outline-none transition duration-300 placeholder:text-[#9aa0c0] focus:border-[#7c5cff] focus:shadow-[0_0_0_5px_rgba(124,92,255,0.18)] focus:scale-[1.01]"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="relative min-h-[56px] min-w-[170px] overflow-hidden rounded-[22px] bg-[linear-gradient(135deg,#ff6b6b,#ff7ac6,#7c5cff)] bg-[length:200%_200%] px-6 font-extrabold text-white shadow-[0_14px_32px_rgba(255,107,107,0.4)] transition duration-200 hover:-translate-y-1 hover:rotate-[-1.5deg] hover:scale-[1.04] active:scale-95 disabled:cursor-not-allowed disabled:opacity-70 disabled:animate-pulseBtn md:min-h-[150px]"
        >
          {loading ? (
            <span className="mx-auto block h-5 w-5 rounded-full border-[3px] border-white/40 border-t-white animate-spin" />
          ) : (
            "🚀 Generate Plan"
          )}
        </button>
      </div>

      <div className="mt-[18px] flex flex-wrap gap-[10px]">
        {quickPrompts.map((prompt) => (
          <button
            key={prompt.label}
            onClick={() => setPrompt(prompt.text)}
            className={`${prompt.color} rounded-full px-[18px] py-[10px] font-bold text-white transition duration-200 hover:-translate-y-1 hover:scale-105 hover:rotate-[-2deg]`}
          >
            {prompt.label}
          </button>
        ))}
      </div>
    </section>
  );
}

export default Planner;