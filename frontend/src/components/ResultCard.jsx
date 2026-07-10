

function ResultCard({ result }) {
  if (!result) {
    return (
      <div className="result-container empty-state">
        <div className="empty-result-icon">📋</div>
        <h2>Diagnostic Output Pending</h2>
        <p>Awaiting radiological input. Please upload a standardized patient MRI scan and initialize the diagnostic AI suite to commence automated pathological screening.</p>
      </div>
    );
  }

  const { stage0, stage1, stage2, led, message, processing_time } = result;

  return (
    <div className="result-container fade-in">
      <div className="section-header">
        <h2>Comprehensive Diagnostic Report</h2>
        <span className="report-time">Compute Duration: {processing_time || "0.00"}s</span>
      </div>

      <div className="report-grid">
        <div className="data-card primary-data">
          <span className="data-label">Primary Pathology (Stage 0)</span>
          <strong className="data-value highlight">{stage0?.label || "Indeterminate"}</strong>
          <div className="confidence-bar-bg">
            <div 
              className="confidence-bar-fill" 
              style={{ width: `${stage0?.confidence || 0}%` }}
            ></div>
          </div>
          <span className="confidence-text">{stage0?.confidence || 0}% AI Confidence Index</span>
        </div>

        <div className="data-card">
          <span className="data-label">Secondary Markers (Stage 1)</span>
          <strong className="data-value">{stage1?.label || "No Abnormality Detected"}</strong>
          <span className="confidence-text">
            {stage1 ? `${stage1.confidence}% Index` : "Standard Deviation"}
          </span>
        </div>

        <div className="data-card">
          <span className="data-label">Tertiary Indicators (Stage 2)</span>
          <strong className="data-value">{stage2?.label || "No Abnormality Detected"}</strong>
          <span className="confidence-text">
            {stage2 ? `${stage2.confidence}% Index` : "Standard Deviation"}
          </span>
        </div>

        <div className="data-card hardware-card">
          <span className="data-label">Hardware Relay Diagnostic</span>
          <strong className="data-value hardware-status">
            <span className={`status-indicator ${led?.command === "ON" ? "on" : "off"}`}></span>
            {led?.command || "STANDBY"}
          </strong>
        </div>
      </div>

      <div className="clinical-notes">
        <h4>Clinical Interpretation Notes</h4>
        <p>{message || "Automated screening completed. Results should be correlated with clinical findings and verified by an attending radiologist prior to final diagnosis."}</p>
      </div>
    </div>
  );
}

export default ResultCard;