

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-left">
        <div className="brain-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2v20M2 12h20" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <div className="nav-titles">
          <h1>NeuroScan AI</h1>
          <p>Clinical Radiological Analysis Engine</p>
        </div>
      </div>

      <div className="navbar-right">
        <div className="status-badge" title="Secure connection established">
          <span className="pulse-dot"></span>
          Diagnostic Engine Active
        </div>
      </div>
    </header>
  );
}

export default Navbar;