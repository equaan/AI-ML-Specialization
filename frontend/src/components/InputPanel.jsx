import { useState } from "react";
import { Activity, FileText, ImagePlus, LoaderCircle } from "lucide-react";

import { analyzePatient } from "../api/client";
import { useReportContext } from "../state/ReportContext";

export function InputPanel() {
  const { updateReport } = useReportContext();
  const [symptoms, setSymptoms] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await analyzePatient({ imageFile, pdfFile, symptoms });
      updateReport(data.session_id, data.report);
    } catch (submitError) {
      setError(submitError?.response?.data?.detail || "Analysis request failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="panel card" onSubmit={handleSubmit}>
      <div className="section-heading">
        <Activity size={18} />
        <h2>New Analysis</h2>
      </div>

      <label className="field">
        <span>Medical Image</span>
        <div className="upload-box">
          <ImagePlus size={18} />
          <input type="file" accept="image/*" onChange={(event) => setImageFile(event.target.files?.[0] || null)} />
        </div>
      </label>

      <label className="field">
        <span>Lab Report PDF</span>
        <div className="upload-box">
          <FileText size={18} />
          <input type="file" accept=".pdf" onChange={(event) => setPdfFile(event.target.files?.[0] || null)} />
        </div>
      </label>

      <label className="field">
        <span>Symptoms</span>
        <textarea
          rows={6}
          value={symptoms}
          onChange={(event) => setSymptoms(event.target.value)}
          placeholder="Describe the patient symptoms, duration, and context."
        />
      </label>

      {error ? <p className="error-text">{error}</p> : null}

      <button className="primary-button" disabled={loading}>
        {loading ? <LoaderCircle className="spin" size={18} /> : null}
        {loading ? "Analyzing..." : "Run Clinical Analysis"}
      </button>
    </form>
  );
}
