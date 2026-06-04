import { useEffect, useState } from "react";
import { fetchData } from "../services/api";

function Anomalies() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
  const loadAnomalies = async () => {
    try {
      const res = await fetchData(
        "/stores/STORE_BLR_002/anomalies"
      );
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  loadAnomalies();

  const interval = setInterval(loadAnomalies, 5000);

  return () => clearInterval(interval);
}, []);

  if (error) return <p className="error">Error: {error}</p>;
  if (!data) return <div className="loading"><span className="spinner"></span>Loading Anomalies...</div>;

  const getSeverity = (type) => {
    const typeStr = type?.toLowerCase() || "";
    if (typeStr.includes("critical") || typeStr.includes("security")) return "high";
    if (typeStr.includes("warning") || typeStr.includes("unusual")) return "medium";
    return "low";
  };

  const getDescription = (type) => {
    const descriptions = {
      "Unusual Traffic Spike": "Detected 47% increase in foot traffic compared to baseline",
      "Low Conversion Alert": "Conversion rate dropped below expected threshold",
      "Zone Congestion": "Electronics section experiencing higher than normal dwell time",
      "Security Alert": "Potential unauthorized access detected at exit gate B",
    };
    return descriptions[type] || "Anomaly detected - review recommended";
  };

  return (
    <div className="anomalies-card">
      <h2 className="card-title">
        <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        Anomaly Detection
      </h2>
      <div className="anomalies-container">
        {(!data.anomalies || data.anomalies.length === 0) ? (
          <div className="anomalies-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
            <p>No anomalies detected</p>
          </div>
        ) : (
          data.anomalies.map((item, index) => {
            const severity =
                item.severity?.toLowerCase() === "critical"
                    ? "high"
                    : item.severity?.toLowerCase() === "warn"
                    ? "medium"
                    : "low";
            return (
              <div key={index} className="anomaly-item">
                <div className={`anomaly-icon ${severity}`}>
                  {severity === "high" ? (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="12" y1="8" x2="12" y2="12" />
                      <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                  ) : severity === "medium" ? (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                      <line x1="12" y1="9" x2="12" y2="13" />
                      <line x1="12" y1="17" x2="12.01" y2="17" />
                    </svg>
                  ) : (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="12" y1="16" x2="12" y2="12" />
                      <line x1="12" y1="8" x2="12.01" y2="8" />
                    </svg>
                  )}
                </div>
                <div className="anomaly-content">
                  <div className="anomaly-header">
                    <span className="anomaly-type">{item.type}</span>
                    <span className={`anomaly-badge ${severity}`}>{severity}</span>
                  </div>
                  <p className="anomaly-description">{item.suggested_action || getDescription(item.type)}</p>
                  <div className="anomaly-time">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12 6 12 12 16 14" />
                    </svg>
                    <span>{item.timestamp || "Just now"}</span>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default Anomalies;
