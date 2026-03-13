import { equipos, modosJuego } from "../data/gameData";

function choice(items) {
  return items[Math.floor(Math.random() * items.length)];
}

export function sortearModo() {
  return choice(modosJuego);
}

export function sortearEquipo(excluido = null) {
  const disponibles = equipos.filter((equipo) => equipo !== excluido);

  if (!disponibles.length) {
    return null;
  }

  return choice(disponibles);
}

export function sortearPartidoCompleto() {
  if (equipos.length < 2) {
    throw new Error("Se necesitan al menos dos equipos para sortear el partido.");
  }

  const [equipoIker, equipoMoy] = [...equipos]
    .sort(() => Math.random() - 0.5)
    .slice(0, 2);

  return {
    equipoIker,
    equipoMoy,
    modoPartido: sortearModo()
  };
}

export function crearFramesRuleta(totalFrames = 20) {
  return Array.from({ length: totalFrames }, () => ({
    equipoIker: sortearEquipo(),
    equipoMoy: null,
    modoPartido: sortearModo()
  })).map((frame) => {
    const equipoMoy = sortearEquipo(frame.equipoIker);

    return {
      ...frame,
      equipoMoy
    };
  });
}
