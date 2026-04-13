import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  timeout: 30000,
});

export async function analyzePatient({ imageFile, pdfFile, symptoms, voiceFile }) {
  const formData = new FormData();
  if (imageFile) formData.append("image", imageFile);
  if (pdfFile) formData.append("pdf", pdfFile);
  if (voiceFile) formData.append("voice", voiceFile);
  if (symptoms) formData.append("symptoms", symptoms);

  const response = await apiClient.post("/api/analyze", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function transcribeVoice(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob, "voice.webm");
  const response = await apiClient.post("/api/transcribe", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function getModelsStatus() {
  const response = await apiClient.get("/api/models/status");
  return response.data;
}

export async function exportReport(sessionId, format) {
  const response = await apiClient.get(`/api/export/${sessionId}`, {
    params: { format },
    responseType: "blob",
  });
  return response.data;
}

export default apiClient;
