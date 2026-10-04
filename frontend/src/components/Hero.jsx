function Hero() {
  return (
    <section className="mb-[34px] text-center">
      <div className="relative mx-auto mb-[22px] inline-flex items-center gap-2 overflow-hidden rounded-full bg-white px-[18px] py-[10px] font-bold text-[#7c5cff] shadow-[0_8px_24px_rgba(124,92,255,0.2)] animate-pop">
        ✈️ TripMate AI — A Multi-Agent Travel Planner with LangGraph

        <span className="absolute left-[-60%] top-0 h-full w-[40%] bg-[linear-gradient(100deg,transparent,rgba(255,255,255,0.9),transparent)] animate-sweep" />
      </div>

      <h1 className="mb-[10px] bg-[linear-gradient(90deg,#ff6b6b,#ffc53d,#1fc9a0,#38b6ff,#7c5cff,#ff6b6b)] bg-[length:300%_100%] bg-clip-text font-['Bricolage_Grotesque'] text-[clamp(2.6rem,7.5vw,5.8rem)] font-extrabold leading-[1.05] tracking-[-0.04em] text-transparent drop-shadow-[0_8px_18px_rgba(124,92,255,0.25)] animate-rise [animation-name:rise,shine]">
        Plan Your Perfect Trip with AI
      </h1>

      <div
        aria-hidden="true"
        className="relative mx-auto mb-2 h-[54px] w-[90%] max-w-[640px] bg-[radial-gradient(circle,#7c5cff_2px,transparent_2.5px)] bg-[length:14px_6px] bg-repeat-x bg-[position:0_50%] animate-dashMove"
      >
        <span className="absolute left-0 top-1/2 text-[1.8rem] animate-flyAcross">
          ✈️
        </span>
      </div>

      <p className="mx-auto max-w-[760px] text-[1.1rem] leading-[1.7] text-[#5d6385]">
        Search flights, discover hotels, and generate a complete travel
        itinerary using a multi-agent LangGraph system.
      </p>
    </section>
  );
}

export default Hero;