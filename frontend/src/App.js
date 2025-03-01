// App.js
import React from 'react';
import GraphVisualization from './GraphVisualization';

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: '#eee', display: 'flex', flexDirection: 'column' }}>
      <header style={{ backgroundColor: '#282c34', color: '#fff', padding: '20px', textAlign: 'center', fontSize: '24px' }}>
        Closing the Alzheimer's Gap: Mapping Memories for Rediscovery
      </header>
      <GraphVisualization />
    </div>
  );
}

export default App;
