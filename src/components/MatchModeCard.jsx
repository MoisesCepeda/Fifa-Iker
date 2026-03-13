export default function MatchModeCard({ mode, onDrawMode }) {
  return (
    <section className="card center-card">
      <div className="vs-mark">VS</div>

      <p className="center-card__label">Modo del partido</p>
      <p className="center-card__mode">{mode ?? "---"}</p>

      <button className="button button--secondary" onClick={onDrawMode}>
        Sortear modo
      </button>
    </section>
  );
}
