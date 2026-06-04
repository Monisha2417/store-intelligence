import { useEffect, useState } from "react";
import { fetchData } from "../services/api";

function MetricsCard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const res = await fetchData("/stores/STORE_BLR_002/metrics");
        setData(res);
        setError(null);
      } catch (err) {
        setError(err.message || "Failed to load metrics");
      }
    };

    loadMetrics();

    const interval = setInterval(loadMetrics, 5000);

    return () => clearInterval(interval);
  }, []);

  if (error) {
    return <p className="error">Error: {error}</p>;
  }

  if (!data) {
    return (
      <div className="loading">
        <span className="spinner"></span>
        Loading Metrics...
      </div>
    );
  }

  const metrics = [
    {
      label: "Unique Visitors",
      value: data.unique_visitors?.toLocaleString() || "0",
      trend: "up",
      change: "+12%",
    },
    {
      label: "Store Entries",
      value: data.entry?.toLocaleString() || "0",
      trend: "up",
      change: "+8%",
    },
    {
      label: "Purchases",
      value: data.purchase?.toLocaleString() || "0",
      trend: "down",
      change: "-3%",
    },
    {
      label: "Conversion",
      value: `${data.conversion_rate || 0}%`,
      trend: "up",
      change: "+5%",
    },
  ];

  return (
    <div className="metrics-card">
      <h2 className="card-title">
        <svg
          className="icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M3 3v18h18" />
          <path d="M18 17V9" />
          <path d="M13 17V5" />
          <path d="M8 17v-3" />
        </svg>
        Key Metrics
      </h2>

      <div className="metrics-grid">
        {metrics.map((metric, index) => (
          <div key={index} className="metric-item">
            <span className="metric-label">{metric.label}</span>

            <span className="metric-value">{metric.value}</span>

            <span className={`metric-trend ${metric.trend}`}>
              {metric.trend === "up" ? (
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M7 17l5-5 5 5" />
                  <path d="M7 12l5-5 5 5" />
                </svg>
              ) : (
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M7 7l5 5 5-5" />
                  <path d="M7 12l5 5 5-5" />
                </svg>
              )}

              {metric.change}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MetricsCard;