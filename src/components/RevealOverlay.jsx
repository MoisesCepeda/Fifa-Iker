export default function RevealOverlay({ team, logo, visible }) {
  return (
    <div className={`overlay overlay--reveal ${visible ? "is-visible" : ""}`}>
      <div className="overlay__panel">
        <p className="overlay__kicker">Revelando club</p>
        <div className="overlay__logo-shell">
          {logo ? <img src={logo} alt={team} className="overlay__logo" /> : null}
        </div>
        <h3 className="overlay__title">{team}</h3>
      </div>
    </div>
  );
}
