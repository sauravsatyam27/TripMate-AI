const features = [
  {
    icon: "✈️",
    title: "Flights",
    description: "Live fares and routes",
    className: "bg-[linear-gradient(135deg,#bfe8ff,#7fd0ff)]",
  },
  {
    icon: "🏨",
    title: "Hotels",
    description: "Stays that fit your budget",
    className: "bg-[linear-gradient(135deg,#ffd1d1,#ff9d9d)]",
  },
  {
    icon: "🗺️",
    title: "Itinerary",
    description: "Day-by-day sightseeing",
    className: "bg-[linear-gradient(135deg,#bff5e6,#6fe3c4)]",
  },
];

function Features() {
  return (
    <section className="mb-[26px] grid grid-cols-1 gap-4 md:grid-cols-3">
      {features.map((feature, index) => (
        <div
          key={feature.title}
          className="flex items-center gap-[14px] rounded-[22px] bg-white/85 px-[18px] py-4 shadow-[0_12px_30px_rgba(27,31,59,0.1)] backdrop-blur-[12px] transition duration-300 hover:-translate-y-2 hover:-rotate-[1.5deg] hover:shadow-[0_22px_40px_rgba(124,92,255,0.28)] animate-rise"
          style={{
            animationDelay: `${0.1 + index * 0.15}s`,
          }}
        >
          <span
            className={`grid h-[52px] w-[52px] flex-none place-items-center rounded-2xl text-[1.6rem] animate-bob ${feature.className}`}
            style={{
              animationDelay: `${-index * 1.3}s`,
            }}
          >
            {feature.icon}
          </span>

          <div>
            <h3 className="font-['Bricolage_Grotesque'] text-[1.1rem] font-bold">
              {feature.title}
            </h3>

            <p className="mt-0.5 text-[0.88rem] text-[#5d6385]">
              {feature.description}
            </p>
          </div>
        </div>
      ))}
    </section>
  );
}

export default Features;