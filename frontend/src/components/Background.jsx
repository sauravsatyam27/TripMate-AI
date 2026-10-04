function Background() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-[linear-gradient(120deg,#fff3e0,#e6f7ff,#f3e8ff,#e5fff4)] bg-[length:300%_300%] animate-bgShift">
      <div className="absolute -left-20 -top-20 h-[380px] w-[380px] rounded-full bg-[#ffc53d] opacity-55 blur-[60px] animate-drift" />

      <div className="absolute -right-[100px] top-[12%] h-[420px] w-[420px] rounded-full bg-[#38b6ff] opacity-55 blur-[60px] animate-drift [animation-delay:-4s]" />

      <div className="absolute bottom-[-100px] left-[30%] h-[360px] w-[360px] rounded-full bg-[#ff7ac6] opacity-55 blur-[60px] animate-drift [animation-delay:-8s]" />

      <span className="absolute left-[5%] top-[38%] select-none text-[2.3rem] animate-bob">
        🌴
      </span>

      <span className="absolute right-[6%] top-[30%] select-none text-[2.3rem] animate-bob [animation-delay:-2s]">
        🗼
      </span>

      <span className="absolute bottom-[12%] left-[8%] select-none text-[2.3rem] animate-bob [animation-delay:-4s]">
        🏝️
      </span>

      <span className="absolute bottom-[16%] right-[9%] select-none text-[2.3rem] animate-bob [animation-delay:-1s]">
        🧳
      </span>
    </div>
  );
}

export default Background;