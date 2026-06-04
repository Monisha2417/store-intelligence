import { useEffect, useState } from "react";
import { fetchData } from "../services/api";

function Funnel() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
  const loadFunnel = async () => {
    try {
        const res = await fetchData(
            "/stores/STORE_BLR_002/funnel"
        );
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  loadFunnel();

  const interval = setInterval(loadFunnel, 5000);

  return () => clearInterval(interval);
}, []);

  if (error) return <p className="error">Error: {error}</p>;
  if (!data) return <div className="loading"><span className="spinner"></span>Loading Funnel...</div>;

  const maxValue = data.entry || 1;
  
  const steps = [
    { label: "Entry", value: data.entry || 0 },
    { label: "Zone Visits", value: data.zone_visits || 0 },
    { label: "Billing", value: data.billing || 0 },
    { label: "Purchase", value: data.purchase || 0 },
  ];

  return (
    <div className="funnel-card">
      <h2 className="card-title">
        <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z" />
        </svg>
        Conversion Funnel
      </h2>
      <div className="funnel-container">
        {steps.map((step, index) => {
          const percentage = Math.round((step.value / maxValue) * 100);
          const conversionFromPrev =
            index > 0
                ? steps[index - 1].value > 0
                    ? Math.round((step.value / steps[index - 1].value) * 100)
                    : 0
                : 100;
          
          return (
            <div key={index} className="funnel-step-wrapper">
              {index > 0 && (
                <div className="funnel-connector">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 5v14M19 12l-7 7-7-7" />
                  </svg>
                </div>
              )}
              <div className="funnel-step">
                <div className="funnel-step-header">
                  <span className="funnel-step-label">
                    <span className="step-number">{index + 1}</span>
                    {step.label}
                  </span>
                  <div className="funnel-step-stats">
                    <span className="funnel-step-value">{step.value.toLocaleString()}</span>
                    {index > 0 && (
                      <span className="funnel-step-percentage">({conversionFromPrev}%)</span>
                    )}
                  </div>
                </div>
                <div className="funnel-bar-container">
                  <div 
                    className="funnel-bar" 
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Funnel;
