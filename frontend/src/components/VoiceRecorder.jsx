import { useEffect, useMemo, useRef, useState } from "react";
import { Mic, Square, WandSparkles } from "lucide-react";

import { transcribeVoice } from "../api/client";

export function VoiceRecorder({ transcript, onTranscriptChange, onAudioReady }) {
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const supported = useMemo(
    () => typeof navigator !== "undefined" && Boolean(navigator.mediaDevices?.getUserMedia),
    []
  );

  useEffect(() => {
    return () => {
      mediaRecorderRef.current?.stream?.getTracks?.().forEach((track) => track.stop());
    };
  }, []);

  async function startRecording() {
    setError("");
    if (!supported) {
      setError("MediaRecorder is not available in this browser.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };
      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        onAudioReady(blob);
        setLoading(true);
        try {
          const data = await transcribeVoice(blob);
          onTranscriptChange(data.transcript || "");
        } catch {
          setError("Voice transcription failed.");
        } finally {
          setLoading(false);
          recorder.stream.getTracks().forEach((track) => track.stop());
        }
      };
      mediaRecorderRef.current = recorder;
      recorder.start();
      setRecording(true);
    } catch {
      setError("Microphone access was denied.");
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }

  return (
    <div className="voice-card">
      <div className="voice-header">
        <div>
          <p className="panel-kicker">Voice Input</p>
          <h4>Record Symptoms</h4>
        </div>
        <div className={`voice-indicator ${recording ? "live" : ""}`} />
      </div>

      <div className="wave-bars" aria-hidden="true">
        {Array.from({ length: 18 }).map((_, index) => (
          <span
            key={index}
            style={{ animationDelay: `${index * 0.08}s`, height: `${12 + (index % 6) * 4}px` }}
            className={recording ? "live" : ""}
          />
        ))}
      </div>

      <div className="voice-actions">
        {!recording ? (
          <button type="button" className="secondary-button" onClick={startRecording}>
            <Mic size={16} />
            {loading ? "Transcribing..." : "Start Recording"}
          </button>
        ) : (
          <button type="button" className="danger-button" onClick={stopRecording}>
            <Square size={16} />
            Stop & Transcribe
          </button>
        )}
      </div>

      <label className="field compact">
        <span className="field-label">
          <WandSparkles size={14} />
          Transcript
        </span>
        <textarea
          rows={3}
          value={transcript}
          onChange={(event) => onTranscriptChange(event.target.value)}
          placeholder="Your transcription will appear here."
        />
      </label>

      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}
