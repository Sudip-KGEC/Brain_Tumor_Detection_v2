import { useState } from "react";
import Navbar from "./components/Navbar";
import PremiumDiagnosticsViewer from "./components/PremiumDiagnosticsViewer";
import ResultCard from "./components/ResultCard";
import Footer from "./components/Footer";
import Loading from "./components/Loading";
import { predictMRI } from "./services/api";
import "./index.css";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handlePrediction = async () => {
    if (!selectedImage) {
      alert("Please upload a valid radiological scan prior to initializing diagnostics.");
      return;
    }

    try {
      setLoading(true);
      const response = await predictMRI(selectedImage);
      setResult(response);
    } catch (error) {
      console.error("Diagnostic Engine Error:", error);
      if (error.response?.data?.detail) {
        alert(`Analysis Interrupted: ${error.response.data.detail}`);
      } else {
        alert("Connection timeout: Unable to establish a secure link with the remote diagnostic server.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Navbar />

      <main className="dashboard-container">
        <div className="dashboard-left">
          <section className="ui-card">
            <PremiumDiagnosticsViewer
              selectedImage={selectedImage}
              setSelectedImage={setSelectedImage}
              preview={preview}
              setPreview={setPreview}
              loading={loading}
              onPredict={handlePrediction}
            />
          </section>
        </div>

        <div className="dashboard-right">
          <section className="ui-card result-wrapper">
            {loading ? (
              <Loading />
            ) : (
              <ResultCard result={result} />
            )}
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;