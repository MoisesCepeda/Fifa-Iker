export default function CountdownOverlay({ value, visible }) {
  return (
    <div className={`overlay overlay--countdown ${visible ? "is-visible" : ""}`}>
      <div className="countdown">{value}</div>
    </div>
  );
}
