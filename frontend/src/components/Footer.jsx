
function Footer() {
  return (
    <footer className="app-footer">
      <p>&copy; {new Date().getFullYear()} NeuroScan AI Systems. All rights reserved.</p>
      <p style={{ marginTop: '6px', fontSize: '0.75rem', opacity: 0.7 }}>
        Regulatory Compliance: HIPAA & GDPR Ready • For clinical investigational use and radiological assistance only. Not a substitute for primary medical diagnosis.
      </p>
    </footer>
  );
}

export default Footer;