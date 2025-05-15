import { useState, createContext, useEffect } from "react";

export const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null)

    useEffect(() => {
        initialize()
    }, [])

    const initialize = async () => {
        const token = localStorage.getItem('token')
        if (token) {
            try {
                const userResponse = await fetch(`http://localhost:8000/auth/users/me/`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Token ${token}`,
                        },
                    }
                )
                if (userResponse.ok) {
                    const userData = await userResponse.json()
                    setUser(userData)
                }
                localStorage.removeItem('token')

            } catch (error) { localStorage.removeItem('token') }
        }
    }


    const logout = async () => {
        try {

            const response = await fetch(`http://localhost:8000/auth/token/logout/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${localStorage.getItem('token')}`,
                    }
                }

            )
            if (!response.ok) {
                throw new Error('Logout failed!')
            } else {
                localStorage.removeItem('token')
                setUser(null)
            }
        } catch (error) {
            console.log('Login faild', error)
        }
    }


    const login = async (username, password) => {
        try {

            const response = await fetch('http://127.0.0.1:8000/auth/token/login/',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', },
                    body: JSON.stringify({ username, password })
                }
            )
            if (!response.ok) {
                throw new Error('Login failed')
            } else {
                const data = await response.json()
                if (data.auth_token) {
                    localStorage.setItem('token', data.auth_token)
                    // fetch user details
                    const userResponse = await fetch(`http://localhost:8000/auth/users/me/`,
                        {
                            method: 'GET',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Token ${data.auth_token}`,
                            },
                        }
                    )
                    if (!userResponse.ok) {
                        throw new Error('Failed to fetch user details')
                    }
                    const userData = await userResponse.json()
                    setUser(userData)
                    return true
                }
                return false
            }
        } catch (error) {
            console.log('Login faild', error)
            return false
        }
    }

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}