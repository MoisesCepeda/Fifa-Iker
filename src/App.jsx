import { useEffect, useRef, useState } from "react";
import AnimatedBackground from "./components/AnimatedBackground";
import Controls from "./components/Controls";
import CountdownOverlay from "./components/CountdownOverlay";
import Header from "./components/Header";
import MatchModeCard from "./components/MatchModeCard";
import PlayerCard from "./components/PlayerCard";
import RevealOverlay from "./components/RevealOverlay";
import { logos, sonidos } from "./data/gameData";
import { useAudio } from "./hooks/useAudio";
import {
  crearFramesRuleta,
  sortearEquipo,
  sortearModo,
  sortearPartidoCompleto
} from "./utils/drawLogic";

const countdownFrames = ["3", "2", "1", "Golizaa!!"];

export default function App() {
  const [equipoIker, setEquipoIker] = useState(null);
  const [equipoMoy, setEquipoMoy] = useState(null);
  const [modoPartido, setModoPartido] = useState(null);
  const [progressIker, setProgressIker] = useState(0);
  const [progressMoy, setProgressMoy] = useState(0);
  const [isSpinning, setIsSpinning] = useState(false);
  const [revealTeam, setRevealTeam] = useState(null);
  const [countdownValue, setCountdownValue] = useState("");
  const timeoutsRef = useRef([]);

  const inicioAudio = useAudio(sonidos.inicio);
  const ruletaAudio = useAudio(sonidos.ruleta);
  const revelarAudio = useAudio(sonidos.revelar);

  const clearTimers = () => {
    timeoutsRef.current.forEach((timeoutId) => window.clearTimeout(timeoutId));
    timeoutsRef.current = [];
  };

  useEffect(() => clearTimers, []);

  const schedule = (callback, delay) => {
    const timeoutId = window.setTimeout(callback, delay);
    timeoutsRef.current.push(timeoutId);
  };

  const resetState = () => {
    clearTimers();
    ruletaAudio.stop();
    revelarAudio.stop();
    setEquipoIker(null);
    setEquipoMoy(null);
    setModoPartido(null);
    setProgressIker(0);
    setProgressMoy(0);
    setRevealTeam(null);
    setCountdownValue("");
    setIsSpinning(false);
  };

  const handleDrawIker = () => {
    const nextTeam = sortearEquipo(equipoMoy);
    setEquipoIker(nextTeam);
    setProgressIker(100);
  };

  const handleDrawMoy = () => {
    const nextTeam = sortearEquipo(equipoIker);
    setEquipoMoy(nextTeam);
    setProgressMoy(100);
  };

  const handleDrawMode = () => {
    setModoPartido(sortearModo());
  };

  const runCountdown = () => {
    countdownFrames.forEach((frame, index) => {
      schedule(() => {
        setCountdownValue(frame);
      }, index * 700);
    });

    schedule(() => {
      setCountdownValue("");
      setIsSpinning(false);
    }, countdownFrames.length * 700);
  };

  const revealWinner = (match) => {
    const selectedTeam =
      Math.random() > 0.5 ? match.equipoIker : match.equipoMoy;

    setRevealTeam(selectedTeam);
    revelarAudio.play();

    schedule(() => {
      setRevealTeam(null);
      runCountdown();
    }, 1800);
  };

  const handleQuickDraw = async () => {
    clearTimers();
    setIsSpinning(true);
    setRevealTeam(null);
    setCountdownValue("");
    await ruletaAudio.play({ loop: true });

    const frames = crearFramesRuleta(18);

    frames.forEach((frame, index) => {
      schedule(() => {
        setEquipoIker(frame.equipoIker);
        setEquipoMoy(frame.equipoMoy);
        setModoPartido(frame.modoPartido);
        setProgressIker(Math.round(((index + 1) / frames.length) * 100));
        setProgressMoy(Math.round(((index + 1) / frames.length) * 100));
      }, index * 90);
    });

    schedule(() => {
      ruletaAudio.stop();
      const match = sortearPartidoCompleto();
      setEquipoIker(match.equipoIker);
      setEquipoMoy(match.equipoMoy);
      setModoPartido(match.modoPartido);
      setProgressIker(100);
      setProgressMoy(100);
      revealWinner(match);
    }, frames.length * 90 + 50);
  };

  const handleStart = async () => {
    if (isSpinning) {
      return;
    }

    await inicioAudio.play();
    handleQuickDraw();
  };

  return (
    <div className="app-shell">
      <AnimatedBackground />

      <main className="app">
        <Header />

        <section className="app-layout">
          <PlayerCard
            label="Jugador 1"
            playerName="IKER"
            accent="var(--cyan)"
            team={equipoIker}
            logo={equipoIker ? logos[equipoIker] : null}
            progress={progressIker}
            onDraw={handleDrawIker}
          />

          <MatchModeCard mode={modoPartido} onDrawMode={handleDrawMode} />

          <PlayerCard
            label="Jugador 2"
            playerName="MOY"
            accent="var(--gold)"
            team={equipoMoy}
            logo={equipoMoy ? logos[equipoMoy] : null}
            progress={progressMoy}
            onDraw={handleDrawMoy}
          />
        </section>

        <Controls
          disabled={isSpinning}
          onQuickDraw={handleQuickDraw}
          onStart={handleStart}
          onReset={resetState}
        />
      </main>

      <RevealOverlay
        visible={Boolean(revealTeam)}
        team={revealTeam}
        logo={revealTeam ? logos[revealTeam] : null}
      />
      <CountdownOverlay visible={Boolean(countdownValue)} value={countdownValue} />
    </div>
  );
}
