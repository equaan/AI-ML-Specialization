import { Component } from "react";

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, message: "" };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      message: error?.message || "Unknown frontend error",
    };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Frontend error boundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="workspace-card error-boundary">
          <p className="panel-kicker">Frontend Guardrail</p>
          <h3>Something broke in the UI</h3>
          <p>{this.state.message}</p>
          <button className="secondary-button" onClick={() => window.location.reload()}>
            Reload Interface
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
