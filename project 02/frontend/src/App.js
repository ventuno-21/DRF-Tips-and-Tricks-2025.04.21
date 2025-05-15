import logo from './logo.svg';
import './App.css';
import { AuthProvider } from './AuthContext';
import Login from './components/Login';
import { BrowserRouter, Route, Routes, Link } from "react-router";
import Dashboard from './components/Dashboard';

function App() {
  return (
    <>
      <AuthProvider>
        <BrowserRouter>
          <Link to="/login">Login</Link>
          <Routes>

            <Route path='/login' element={<Login />} />
            <Route path='/dashboard' element={<Dashboard />} />

          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </>
  );
}

export default App;
