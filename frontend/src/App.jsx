import { useState } from 'react'
import axios from 'axios'
import Plot from 'react-plotly.js'

function App() {
  const [loading, setLoading] = useState(false)
  const [plotData, setPlotData] = useState(null)
  const [clusters, setClusters] = useState([])
  
  // Default State: The "Demo" Payload
  const [jsonInput, setJsonInput] = useState(JSON.stringify({
    "documents": [
      "How to configure EC2 instance types",
      "Setting up S3 bucket policies for public access",
      "IAM role configuration for lambda functions",
      "Kubernetes pod auto-scaling settings",
      "Database migration service endpoints",
      "API Gateway throttling limits and quotas",
      "VPC peering connections between regions",
      "Linux kernel parameters for high performance",
      "Docker container networking modes",
      "Redis cluster sharding strategies"
    ],
    "queries": [
      "How to configure EC2 instance",
      "s3 bucket permission error",
      "how to reduce my monthly aws bill",
      "pricing for reserved instances",
      "why is my invoice so high",
      "cost explorer api usage",
      "lambda function timeout settings",
      "credit card payment failure support",
      "free tier limits for rds",
      "kubernetes pod crashing"
    ]
  }, null, 2))

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      // 1. Parse the JSON from the text area
      const payload = JSON.parse(jsonInput)
      
      // 2. Send to FastAPI (Make sure port 8000 is running!)
      const response = await axios.post('http://127.0.0.1:8000/analyze', payload)
      
      // 3. Update State
      setPlotData(response.data.plot_data)
      setClusters(response.data.clusters)
      
    } catch (error) {
      alert("Error: " + error.message + "\nCheck console for details.")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      
      {/* --- LEFT PANEL: CONTROLS --- */}
      <div style={{ width: '350px', padding: '20px', background: '#f5f5f5', borderRight: '1px solid #ddd', display: 'flex', flexDirection: 'column' }}>
        <h2>Semantic Coverage</h2>
        <p style={{ fontSize: '14px', color: '#666' }}>
          Paste your JSON below to detect Knowledge Gaps.
        </p>
        
        <textarea 
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          style={{ flex: 1, padding: '10px', fontFamily: 'monospace', fontSize: '12px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        
        <button 
          onClick={handleAnalyze}
          disabled={loading}
          style={{ 
            marginTop: '15px', padding: '12px', 
            background: loading ? '#ccc' : '#2563eb', 
            color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' 
          }}
        >
          {loading ? 'Analyzing...' : 'Analyze Gaps 🚀'}
        </button>

        {/* CLUSTER REPORT LIST */}
        <div style={{ marginTop: '20px', overflowY: 'auto', flex: 1 }}>
          {clusters.map((c) => (
            <div key={c.cluster_id} style={{ 
              padding: '10px', marginBottom: '10px', borderRadius: '4px', 
              background: 'white', borderLeft: `4px solid ${c.status === 'blind_spot' ? '#ef4444' : '#22c55e'}` 
            }}>
              <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
                Topic {c.cluster_id}: {c.status === 'blind_spot' ? '❌ Blind Spot' : '✅ Covered'}
              </div>
              <div style={{ fontSize: '12px', color: '#555', marginTop: '4px' }}>
                Sample: "{c.sample_query}"
              </div>
              <div style={{ fontSize: '11px', color: '#999', marginTop: '4px' }}>
                Distance: {c.distance_score} | Vol: {c.query_count}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* --- RIGHT PANEL: VISUALIZATION --- */}
      <div style={{ flex: 1, padding: '20px', background: 'white' }}>
        {plotData ? (
          <Plot
            data={[
              // 1. Documents (Blue Dots)
              {
                x: plotData.docs_x,
                y: plotData.docs_y,
                mode: 'markers',
                type: 'scatter',
                name: 'Documents',
                marker: { color: '#3b82f6', size: 10, opacity: 0.6 }
              },
              // 2. Queries (Red/Colored Dots)
              {
                x: plotData.queries_x,
                y: plotData.queries_y,
                mode: 'markers',
                type: 'scatter',
                name: 'Queries',
                text: plotData.query_labels.map(l => `Cluster ${l}`),
                marker: { 
                  color: plotData.query_labels, // Color by cluster ID
                  colorscale: 'Portland',
                  size: 12, 
                  line: { color: 'black', width: 1 } 
                }
              }
            ]}
            layout={{ 
              title: 'Semantic Gap Map', 
              autosize: true, 
              hovermode: 'closest',
              xaxis: { showgrid: true, zeroline: false, showticklabels: false },
              yaxis: { showgrid: true, zeroline: false, showticklabels: false }
            }}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%' }}
          />
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#aaa' }}>
            Click "Analyze Gaps" to visualize your data.
          </div>
        )}
      </div>

    </div>
  )
}

export default App