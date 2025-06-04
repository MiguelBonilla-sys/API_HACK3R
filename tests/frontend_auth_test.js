
// 🚀 CREDENCIALES DE PRUEBA PARA FRONTEND
const TEST_CREDENTIALS = {
    username: "frontend4561",
    password: "TestIrVpejwCK9#x@123",
    token: "b7c9843596cefad112dea7316f496abebd6a39b1"
};

// 🔧 URL base
const API_BASE_URL = "https://apihack3r-production.up.railway.app";

// 🔐 Función de login (usando credenciales de prueba)
const testLogin = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                username: TEST_CREDENTIALS.username,
                password: TEST_CREDENTIALS.password,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Login falló: ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        console.log('✅ Login exitoso:', data);
        return data.key;

    } catch (error) {
        console.error('❌ Error en login:', error.message);
        throw error;
    }
};

// 👤 Función para obtener perfil
const testGetProfile = async (token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/user/`, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Error obteniendo perfil: ${response.status}`);
        }

        const userData = await response.json();
        console.log('✅ Perfil obtenido:', userData);
        return userData;

    } catch (error) {
        console.error('❌ Error obteniendo perfil:', error.message);
        throw error;
    }
};

// 🧪 Función de prueba completa
const runFullTest = async () => {
    try {
        console.log('🚀 Iniciando prueba de autenticación...');
        
        // 1. Login
        const token = await testLogin();
        
        // 2. Obtener perfil
        const profile = await testGetProfile(token);
        
        console.log('🎉 ¡Prueba completada exitosamente!');
        
    } catch (error) {
        console.error('💥 Error en prueba:', error.message);
    }
};

// ⚡ Ejecutar prueba
// runFullTest();
