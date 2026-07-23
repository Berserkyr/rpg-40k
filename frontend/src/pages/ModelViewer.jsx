import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import '../styles/ModelViewer.css';

// Import TOUS les modèles générés
import * as GeneratedModels from '../engine3d/GeneratedModels.js';

export default function ModelViewer() {
  const canvasRef = useRef(null);
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [scene, setScene] = useState(null);
  const [currentModelGroup, setCurrentModelGroup] = useState(null);

  // Découvrir tous les modèles disponibles
  useEffect(() => {
    const modelFunctions = Object.keys(GeneratedModels)
      .filter(key => key.startsWith('build'))
      .map(key => ({
        name: key.replace('build', ''),
        functionName: key,
        buildFunction: GeneratedModels[key]
      }));
    
    setAvailableModels(modelFunctions);
    console.log('Modèles disponibles:', modelFunctions);
  }, []);

  // Setup Three.js
  useEffect(() => {
    if (!canvasRef.current) return;

    const width = 800;
    const height = 600;

    // Scène
    const newScene = new THREE.Scene();
    newScene.background = new THREE.Color(0x1a1a2e);
    setScene(newScene);

    // Caméra
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.set(5, 3, 5);
    camera.lookAt(0, 1, 0);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ 
      canvas: canvasRef.current,
      antialias: true 
    });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;

    // Lumières
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    newScene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 5);
    directionalLight.castShadow = true;
    newScene.add(directionalLight);

    const fillLight = new THREE.DirectionalLight(0x4466ff, 0.3);
    fillLight.position.set(-5, 5, -5);
    newScene.add(fillLight);

    // Grille au sol
    const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
    newScene.add(gridHelper);

    // Animation
    let animationId;
    let rotation = 0;
    const animate = () => {
      animationId = requestAnimationFrame(animate);
      rotation += 0.01;
      camera.position.x = Math.cos(rotation) * 8;
      camera.position.z = Math.sin(rotation) * 8;
      camera.lookAt(0, 2, 0);
      renderer.render(newScene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animationId);
      renderer.dispose();
    };
  }, []);

  // Charger un modèle
  const loadModel = (modelInfo) => {
    if (!scene) return;

    // Retirer l'ancien modèle
    if (currentModelGroup) {
      scene.remove(currentModelGroup);
    }

    // Créer le nouveau modèle
    try {
      const newModel = modelInfo.buildFunction(1);
      scene.add(newModel);
      setCurrentModelGroup(newModel);
      setSelectedModel(modelInfo);
      console.log('Modèle chargé:', modelInfo.name);
    } catch (error) {
      console.error('Erreur lors du chargement du modèle:', error);
      alert(`Erreur: ${error.message}`);
    }
  };

  return (
    <div className="model-viewer-page">
      <div className="viewer-header">
        <h1>🎨 Visualiseur de Modèles 3D</h1>
        <p>Modèles disponibles: <strong>{availableModels.length}</strong></p>
      </div>

      <div className="viewer-content">
        <div className="model-list">
          <h2>Modèles Générés</h2>
          {availableModels.length === 0 ? (
            <div className="no-models">
              <p>❌ Aucun modèle trouvé</p>
              <p>Allez sur <a href="/generator">/generator</a> pour en créer</p>
            </div>
          ) : (
            <div className="model-grid">
              {availableModels.map((model) => (
                <button
                  key={model.functionName}
                  className={`model-button ${selectedModel?.name === model.name ? 'active' : ''}`}
                  onClick={() => loadModel(model)}
                >
                  <span className="model-icon">🎮</span>
                  <span className="model-name">{model.name}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="canvas-container">
          <canvas ref={canvasRef} />
          {selectedModel && (
            <div className="model-info">
              <h3>📦 {selectedModel.name}</h3>
              <code>{selectedModel.functionName}(scale)</code>
            </div>
          )}
          {!selectedModel && (
            <div className="model-placeholder">
              <p>👈 Sélectionnez un modèle</p>
            </div>
          )}
        </div>
      </div>

      <div className="viewer-footer">
        <div className="controls-info">
          <p>🔄 Rotation automatique • 🎯 Caméra orbitale</p>
        </div>
      </div>
    </div>
  );
}
