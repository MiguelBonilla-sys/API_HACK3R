# 🚀 CONFIGURACIÓN DE AUTENTICACIÓN PARA FRONTEND - RAILWAY

## ✅ ESTADO DE RAILWAY: TOTALMENTE FUNCIONAL

**URL PRODUCTION**: `https://apihack3r-production.up.railway.app`

**CONFIRMADO**: Los endpoints de autenticación están **100% FUNCIONANDO** en Railway ✅

**PROBLEMA RESUELTO**: No hay error 404 en `/auth/login/` - Los endpoints funcionan correctamente.

## 🔗 ENDPOINTS DISPONIBLES EN RAILWAY

| Endpoint | Método | URL Completa | Estado |
|----------|--------|--------------|---------|
| **Registro** | POST | `https://apihack3r-production.up.railway.app/auth/registration/` | ✅ FUNCIONAL |
| **Login** | POST | `https://apihack3r-production.up.railway.app/auth/login/` | ✅ FUNCIONAL |
| **Logout** | POST | `https://apihack3r-production.up.railway.app/auth/logout/` | ✅ FUNCIONAL |
| **Perfil** | GET | `https://apihack3r-production.up.railway.app/auth/user/` | ✅ FUNCIONAL |
| **Perfil Custom** | GET | `https://apihack3r-production.up.railway.app/api/profile/` | ✅ FUNCIONAL |

## 💻 CÓDIGO PARA EL FRONTEND

### 1. Configuración Base

```javascript
// Configuración de la API para Railway
const API_BASE_URL = 'https://apihack3r-production.up.railway.app';

// Headers comunes
const getHeaders = (token = null) => {
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    };
    
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }
    
    return headers;
};
```

### 2. Función de Registro

```javascript
const registerUser = async (userData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/registration/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({
                username: userData.username,
                email: userData.email,
                password1: userData.password,
                password2: userData.password, // Confirmar contraseña
            }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error en registro:', errorData);
            throw new Error(`Registro falló: ${JSON.stringify(errorData)}`);
        }
        
        const data = await response.json();
        console.log('Usuario registrado exitosamente:', data);
        return {
            success: true,
            token: data.key,
            user: data.user
        };
        
    } catch (error) {
        console.error('Error en registerUser:', error);
        throw error;
    }
};
```

### 3. Función de Login

```javascript
const loginUser = async (credentials) => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({
                username: credentials.username,
                password: credentials.password,
            }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error en login:', errorData);
            throw new Error(`Login falló: ${JSON.stringify(errorData)}`);
        }
        
        const data = await response.json();
        console.log('Login exitoso:', data);
        return {
            success: true,
            token: data.key
        };
        
    } catch (error) {
        console.error('Error en loginUser:', error);
        throw error;
    }
};
```

### 4. Función para Obtener Perfil

```javascript
const getUserProfile = async (token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/user/`, {
            method: 'GET',
            headers: getHeaders(token),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error obteniendo perfil:', errorData);
            throw new Error(`Error: ${JSON.stringify(errorData)}`);
        }
        
        const userData = await response.json();
        console.log('Perfil obtenido:', userData);
        return userData;
        
    } catch (error) {
        console.error('Error en getUserProfile:', error);
        throw error;
    }
};
```

### 5. Función de Logout

```javascript
const logoutUser = async (token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/logout/`, {
            method: 'POST',
            headers: getHeaders(token),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error en logout:', errorData);
            throw new Error(`Logout falló: ${JSON.stringify(errorData)}`);
        }
        
        console.log('Logout exitoso');
        return { success: true };
        
    } catch (error) {
        console.error('Error en logoutUser:', error);
        throw error;
    }
};
```

## 🔧 EJEMPLO DE FLUJO COMPLETO

```javascript
// Ejemplo de uso completo
const authExample = async () => {
    try {
        console.log('🚀 Iniciando flujo de autenticación...');
        
        // 1. Registrar usuario
        console.log('📝 Registrando usuario...');
        const registerResult = await registerUser({
            username: 'frontenduser',
            email: 'frontend@test.com',
            password: 'FrontendPassword123!'
        });
        
        const token = registerResult.token;
        console.log('✅ Usuario registrado, token:', token);
        
        // 2. Obtener perfil
        console.log('👤 Obteniendo perfil...');
        const profile = await getUserProfile(token);
        console.log('✅ Perfil:', profile);
        
        // 3. Logout
        console.log('👋 Cerrando sesión...');
        await logoutUser(token);
        console.log('✅ Logout completado');
        
        // 4. Login con las mismas credenciales
        console.log('🔐 Haciendo login...');
        const loginResult = await loginUser({
            username: 'frontenduser',
            password: 'FrontendPassword123!'
        });
        console.log('✅ Login exitoso:', loginResult);
        
    } catch (error) {
        console.error('❌ Error en flujo de autenticación:', error);
    }
};

// Ejecutar ejemplo
authExample();
```

## 🚨 DEBUGGING Y TROUBLESHOOTING

### Cómo verificar si hay problemas

```javascript
const debugAuth = async () => {
    // 1. Verificar conectividad
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`);
        console.log('✅ Servidor accesible, status:', response.status);
        
        if (response.status === 405) {
            console.log('✅ Endpoint /auth/login/ existe (405 = Method Not Allowed para GET)');
        }
    } catch (error) {
        console.error('❌ Servidor no accesible:', error);
        return;
    }
    
    // 2. Probar registro con datos válidos
    try {
        await registerUser({
            username: 'debuguser',
            email: 'debug@test.com',
            password: 'DebugPassword123!'
        });
        console.log('✅ Registro funciona correctamente');
    } catch (error) {
        console.error('❌ Error en registro:', error.message);
    }
};
```

## 📋 CHECKLIST PARA EL FRONTEND

- [ ] **URL correcta**: Usar `https://apihack3r-production.up.railway.app`
- [ ] **Método POST**: Para `/auth/login/` y `/auth/registration/`
- [ ] **Headers**: Incluir `Content-Type: application/json`
- [ ] **Body**: Formato JSON correcto
- [ ] **Registro primero**: Crear usuario antes de hacer login
- [ ] **Contraseña fuerte**: Mínimo 8 caracteres, no similar al username
- [ ] **Manejo de errores**: Capturar y mostrar errores 400/401

## 🔐 REQUISITOS DE CONTRASEÑA

Para el registro, la contraseña debe:
- ✅ Tener al menos 8 caracteres
- ✅ No ser demasiado similar al username
- ✅ No ser una contraseña común
- ✅ Contener letras y números

## 📞 CONTACTO DE SOPORTE

- **URLs de admin**: `https://apihack3r-production.up.railway.app/admin/`
- **API Docs**: `https://apihack3r-production.up.railway.app/api/docs/`
- **Estado**: ✅ TOTALMENTE FUNCIONAL

---

**CONFIRMACIÓN FINAL**: Railway está **100% operativo**. Los endpoints responden correctamente. 

**No hay error 404 en `/auth/login/`** - El problema del frontend es que necesita:
1. Usar método POST (no GET)
2. Enviar datos válidos en el body
3. Crear usuarios con contraseñas válidas

**PROBLEMA RESUELTO** ✅
