import { useMemo, useState } from "react";
import { FileText, ImageUp, LoaderCircle, Microscope, Stethoscope } from "lucide-react";

import { analyzePatient } from "../api/client";
import { useReportContext } from "../state/ReportContext";
import { VoiceRecorder } from "./VoiceRecorder";

export function InputPanel() {
  const { updateAnalysis } = useReportContext();
  const [symptoms, setSymptoms] = useState("");
  const [transcript, setTranscript] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [voiceFile, setVoiceFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const canSubmit = useMemo(
    () => Boolean(symptoms.trim() || transcript.trim() || imageFile || pdfFile || voiceFile),
    [symptoms, transcript, imageFile, pdfFile, voiceFile]
  );

  async function handleSubmit(event) {
    event.preventDefault();
    if (!canSubmit) return;

    setLoading(true);
    setError("");
    try {
      const data = await analyzePatient({
        imageFile,
        pdfFile,
        voiceFile,
        symptoms: [symptoms.trim(), transcript.trim()].filter(Boolean).join("\n"),
      });

      updateAnalysis({
        sessionId: data.session_id,
        report: data.report,
        labReport: data.lab_report,
        inputs: {
          symptoms,
          transcript,
          imageName: imageFile?.name || "",
          pdfName: pdfFile?.name || "",
        },
      });
    } catch (submitError) {
      setError(submitError?.response?.data?.detail || "Analysis request failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="workspace-card input-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <div>
          <p className="panel-kicker">New Analysis</p>
          <h3>Initiate Diagnostic Sequence</h3>
        </div>
        <div className="panel-mono">LOCAL / AGENTIC / MULTIMODAL</div>
      </div>

      <div className="upload-grid">
        <label className="upload-tile">
          <div className="upload-icon">
            <ImageUp size={18} />
          </div>
          <div>
            <strong>Medical Image</strong>
            <p>JPG, PNG, DICOM export</p>
          </div>
          <input type="file" accept="image/*" onChange={(event) => setImageFile(event.target.files?.[0] || null)} />
          {imageFile ? <span className="upload-meta">{imageFile.name}</span> : null}
        </label>

        <label className="upload-tile">
          <div className="upload-icon">
            <FileText size={18} />
          </div>
          <div>
            <strong>Lab Report</strong>
            <p>PDF or extracted report</p>
          </div>
          <input type="file" accept=".pdf" onChange={(event) => setPdfFile(event.target.files?.[0] || null)} />
          {pdfFile ? <span className="upload-meta">{pdfFile.name}</span> : null}
        </label>
      </div>

      <label className="field">
        <span className="field-label">
          <Stethoscope size={14} />
          Symptom Description
        </span>
        <textarea
          rows={7}
          value={symptoms}
          onChange={(event) => setSymptoms(event.target.value)}
          placeholder="Describe symptoms, duration, risk context, and clinician observations."
        />
      </label>

      <VoiceRecorder transcript={transcript} onTranscriptChange={setTranscript} onAudioReady={setVoiceFile} />

      <div className="analysis-progress">
        <div>
          <Microscope size={15} />
          <span>Vision Analysis</span>
        </div>
        <div>
          <Microscope size={15} />
          <span>Knowledge Retrieval</span>
        </div>
        <div>
          <Microscope size={15} />
          <span>Report Generation</span>
        </div>
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <button className="primary-button" disabled={!canSubmit || loading}>
        {loading ? <LoaderCircle className="spin" size={18} /> : null}
        {loading ? "Analyzing..." : "Run Clinical Analysis"}
      </button>
    </form>
  );
}
