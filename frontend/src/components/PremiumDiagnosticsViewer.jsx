import { useRef } from "react";
import { FaCloudUploadAlt, FaTimes } from "react-icons/fa";

function PremiumDiagnosticsViewer({
  selectedImage,
  setSelectedImage,
  preview,
  setPreview,
  onPredict,
  loading
}) {
  const fileInput = useRef(null);

  const handleFile = (file) => {
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      alert("Invalid format. Please select a supported radiological image file.");
      return;
    }
    setSelectedImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleBrowse = (e) => {
    const file = e.target.files[0];
    handleFile(file);
  };

  const clearSelection = () => {
    setSelectedImage(null);
    setPreview(null);
    if (fileInput.current) {
      fileInput.current.value = "";
    }
  };

  return (
    <div className="ui-card premium-upload-container fade-in">
      <div className="section-header">
        <h2>Radiological Input Module</h2>
        <p>Supported formats: DICOM, JPEG, PNG for algorithmic pre-processing</p>
      </div>

      <div 
        className={`upload-workspace ${preview ? "has-preview" : ""}`}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <input
          type="file"
          hidden
          ref={fileInput}
          accept="image/*"
          onChange={handleBrowse}
        />

        {!preview ? (
          <div className="upload-dropzone">
            <FaCloudUploadAlt className="upload-icon" />
            <h3>Drag & Drop Radiological Scan</h3>
            <p className="upload-subtitle">or browse local filesystem</p>
            <button 
              className="btn-secondary" 
              onClick={() => fileInput.current.click()}
            >
              Select File
            </button>
          </div>
        ) : (
          <div className="preview-layout">
            <div className={`image-wrapper ${loading ? "scanning" : ""}`}>
              <img src={preview} alt="Radiological Preview" className="mri-image" />
              <button 
                className="btn-clear" 
                onClick={clearSelection}
                title="Clear Selection"
              >
                <FaTimes />
              </button>
            </div>

            <div className="file-action-area">
              <div className="file-info-pill">
                <span className="file-name">{selectedImage?.name}</span>
                <span className="file-size">
                  {selectedImage ? (selectedImage.size / 1024).toFixed(1) + " KB" : ""}
                </span>
              </div>

              <button
                className={`btn-primary ${loading ? "btn-disabled" : ""}`}
                onClick={onPredict}
                disabled={loading}
              >
                {loading ? "Processing Pathology..." : "Initialize AI Diagnostics"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PremiumDiagnosticsViewer;