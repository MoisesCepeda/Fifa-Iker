export default function AnimatedBackground() {
  return (
    <div className="stadium-bg" aria-hidden="true">
      <div className="stadium-bg__image" />
      <div className="stadium-bg__gradient" />
      <div className="stadium-bg__lights stadium-bg__lights--left" />
      <div className="stadium-bg__lights stadium-bg__lights--right" />
      <div className="stadium-bg__beam stadium-bg__beam--one" />
      <div className="stadium-bg__beam stadium-bg__beam--two" />
      <div className="stadium-bg__smoke stadium-bg__smoke--one" />
      <div className="stadium-bg__smoke stadium-bg__smoke--two" />
    </div>
  );
}
