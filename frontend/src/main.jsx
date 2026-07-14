import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import Combat3DDemo from './pages/Combat3DDemo.jsx';
import ModelGenerator from './pages/ModelGenerator.jsx';

// Routing simple basé sur le pathname
const AppRouter = () => {
  const path = window.location.pathname;
  
  if (path === '/combat3d' || path === '/combat3d/') {
    return <Combat3DDemo />;
  }
  
  if (path === '/generator' || path === '/generator/') {
    return <ModelGenerator />;
  }
  
  return <App />;
};

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AppRouter />
  </StrictMode>
);
