import React, { useContext } from 'react'
import { AuthContext } from '../AuthContext'
import { Navigate } from 'react-router-dom'


function Dashboard() {
    const { user, logout } = useContext(AuthContext)

    if (!user) {
        return <Navigate to="/login" replace />
    }
    return (
        <div>
            <h2> Dashboard</h2>

            {user && <p>Welcome, {user.username}!</p>}

            <button onClick={logout}>Logout</button>
        </div>
    )
}

export default Dashboard
