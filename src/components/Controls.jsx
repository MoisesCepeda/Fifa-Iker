export default function Controls({
  disabled,
  onQuickDraw,
  onStart,
  onReset
}) {
  return (
    <section className="controls">
      <button className="button button--primary" onClick={onStart} disabled={disabled}>
        Iniciar partido
      </button>
      <button className="button button--secondary" onClick={onQuickDraw} disabled={disabled}>
        Random rapido
      </button>
      <button className="button button--danger" onClick={onReset}>
        Reiniciar
      </button>
    </section>
  );
}
