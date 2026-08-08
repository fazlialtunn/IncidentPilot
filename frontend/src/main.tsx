import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import RunbookView from './components/RunbookView'
import SlackSimulator from './components/SlackSimulator'
// register components for jsx import (used in App)

import './styles.css'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
