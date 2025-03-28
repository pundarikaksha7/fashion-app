import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

import App from './App.jsx'
import './assets/assets/css/icons.css'
import './assets/assets/css/style.css'
import './assets/assets/css/tailwind.css'
import './assets/assets/css/uikit.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
