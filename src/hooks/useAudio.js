import { useEffect, useRef } from "react";

export function useAudio(src) {
  const audioRef = useRef(null);

  useEffect(() => {
    if (!src) {
      return undefined;
    }

    const audio = new Audio(src);
    audio.preload = "auto";
    audioRef.current = audio;

    return () => {
      audio.pause();
      audioRef.current = null;
    };
  }, [src]);

  const play = async ({ loop = false, reset = true } = {}) => {
    if (!audioRef.current) {
      return;
    }

    audioRef.current.loop = loop;

    if (reset) {
      audioRef.current.currentTime = 0;
    }

    try {
      await audioRef.current.play();
    } catch {
      return;
    }
  };

  const stop = () => {
    if (!audioRef.current) {
      return;
    }

    audioRef.current.pause();
    audioRef.current.currentTime = 0;
    audioRef.current.loop = false;
  };

  return { play, stop };
}
