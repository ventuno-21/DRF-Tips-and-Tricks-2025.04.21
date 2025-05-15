import React, { useState, useContext } from 'react'
import { AuthContext } from '../AuthContext'
import { Navigate, useNavigate } from 'react-router-dom'


const Login = () => {
    const { login } = useContext(AuthContext)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        const success = await login(username, password)
        if (success) {
            navigate('/dashboard')
        } else {
            console.log('Fail')
        }
    }

    return (
        <div>
            <h1> Login</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type='text'
                    placeholder='username'
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type='password'
                    placeholder='password'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type='submit'>Login</button>
            </form>
        </div>
    )
}

export default Login
