import { useEffect, useState } from "react";
import { fetchData } from "../services/api";

function Heatmap() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
  const loadHeatmap = async () => {
    try {
      const res = await fetchData("/stores/STORE_BLR_002/heatmap");
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  loadHeatmap();

  const interval = setInterval(loadHeatmap, 5000);

  return () => clearInterval(interval);
}, []);

  if (error) return <p className="error">Error: {error}</p>;
  if (!data) return <div className="loading"><span className="spinner"></span>Loading Heatmap...</div>;

const rawZones = Object.entries(data.heatmap || {}).map(
  ([zone, value]) => ({
    name: zone,
    visits: value.visits || value,
  })
);

const maxVisits = Math.max(
  ...rawZones.map((z) => z.visits),
  1
);

const getHeatLevel = (visits) => {
  const ratio = visits / maxVisits;

  if (ratio >= 0.8) return "very-high";
  if (ratio >= 0.6) return "high";
  if (ratio >= 0.3) return "medium";
  return "low";
};

const zones = rawZones.map((zone) => ({
  ...zone,
  heatLevel: getHeatLevel(zone.visits),
}));

  if (zones.length === 0) {
  return (
    <div className="heatmap-card">
      <h2 className="card-title">Store Zone Traffic</h2>
      <p>No heatmap data available.</p>
    </div>
  );
}

  return (
    <div className="heatmap-card">
      <h2 className="card-title">
        <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="3" width="7" height="7" />
          <rect x="14" y="3" width="7" height="7" />
          <rect x="14" y="14" width="7" height="7" />
          <rect x="3" y="14" width="7" height="7" />
        </svg>
        Store Zone Traffic
      </h2>
      <div className="heatmap-container">
        <div className="heatmap-grid">
          {zones.map((zone, index) => (
            <div
              key={index}
              className={`heatmap-zone heat-${zone.heatLevel}`}
            >
              <span className="zone-name">{zone.name}</span>
              <span className="zone-value">{zone.visits.toLocaleString()}</span>
              <span className="zone-label">visits</span>
            </div>
          ))}
        </div>
        <div className="heatmap-legend">
          <div className="legend-item">
            <span className="legend-color low"></span>
            <span>Low</span>
          </div>
          <div className="legend-item">
            <span className="legend-color medium"></span>
            <span>Medium</span>
          </div>
          <div className="legend-item">
            <span className="legend-color high"></span>
            <span>High</span>
          </div>
          <div className="legend-item">
            <span className="legend-color very-high"></span>
            <span>Very High</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Heatmap;
