import { StrictMode, lazy, Suspense } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

const Combat3DDemo = lazy(() => import('./pages/Combat3DDemo.jsx'));
const ModelGenerator = lazy(() => import('./pages/ModelGenerator.jsx'));
const ModelViewer = lazy(() => import('./pages/ModelViewer.jsx'));

// Routing simple basé sur le pathname
const AppRouter = () => {
  const path = window.location.pathname;
  
  let page = <App />;
  if (path === '/combat3d' || path === '/combat3d/') page = <Combat3DDemo />;
  if (path === '/generator' || path === '/generator/') page = <ModelGenerator />;
  if (path === '/viewer' || path === '/viewer/') page = <ModelViewer />;
  return <Suspense fallback={<div className="route-loading">Chargement du module graphique…</div>}>{page}</Suspense>;
};

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AppRouter />
  </StrictMode>
);
