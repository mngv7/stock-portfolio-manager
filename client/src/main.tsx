import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import ProtectedRoute from './components/ProtectedRoute.tsx'
import Home from './components/Home.tsx'
import SignUp from './components/SignUp.tsx'

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<App />}/>
      <Route path='/signup' element={<SignUp />}/>
      <Route element={<ProtectedRoute />}>
        <Route path='/app/*' element={<Home />} />
      </Route>
    </Routes>
  </BrowserRouter>
)
