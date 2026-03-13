export default function PlayerCard({
  label,
  playerName,
  accent,
  team,
  logo,
  progress,
  onDraw
}) {
  return (
    <section className="card player-card">
      <p className="player-card__label">{label}</p>
      <div className="player-card__top">
        <h2 className="player-card__name" style={{ color: accent }}>
          {playerName}
        </h2>
      </div>

      <div className="logo-shell">
        {logo ? <img src={logo} alt={team} className="team-logo" /> : <span>Sin logo</span>}
      </div>

      <p className="team-name">{team ?? "---"}</p>

      <div
        className="progress-bar"
        role="progressbar"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow={progress}
      >
        <div className="progress-bar__fill" style={{ width: `${progress}%` }} />
      </div>

      <button className="button button--secondary" onClick={onDraw}>
        Sortear {playerName}
      </button>
    </section>
  );
}
