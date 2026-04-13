import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { ReportProvider } from "./state/ReportContext";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <ReportProvider>
          <App />
        </ReportProvider>
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
);
