// GraphVisualization.jsx
import React from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import data from './data.json';
// import * as THREE from 'three';
import SpriteText from 'three-spritetext';


const GraphVisualization = () => {
    return (
        <ForceGraph3D
            graphData={data}
            nodeAutoColorBy="type"
            linkWidth={link => link.strength / 5}
            linkOpacity={0.6}
            linkDirectionalParticles={link => link.strength}
            linkDirectionalParticleSpeed={0.005}
            nodeThreeObject={node => {
                const sprite = new SpriteText(node.name);
                sprite.color = node.type === 'person' ? 'lightblue' : 'lightgreen';
                sprite.textHeight = 8;
                return sprite;
            }}

            backgroundColor="#101020"
        />
    );
};

export default GraphVisualization;
