import { useState } from 'react'
import { BrowserRouter , Routes,Route } from "react-router-dom";
// import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import File1 from './Components/File1'
import ProfilePage from './Components/ProfilePage'
import SearchResults from './Components/SearchResults';
import SettingsPage from './Components/SettingsPage';
import Login from './Components/Login'
import SignUp from './Components/SignUp'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
     <BrowserRouter>
     <Routes>
      <Route path="" element={<File1/>}/>
      <Route path="/Home" element={<File1/>}/>
        <Route path="/Profile" element={<ProfilePage/>}/>
        <Route path="/search/:result" element={<SearchResults/>}/>
        <Route path="/Profile/:user"  element={<ProfilePage/>}/>
        <Route path="/Settings" element={<SettingsPage/>}/>
        <Route path="/Login" element={<Login/>}/>
        <Route path="/SignUp" element={<SignUp/>}/>
      </Routes>
      </BrowserRouter>
     
       
      
      
    </>
  )
}

export default App
