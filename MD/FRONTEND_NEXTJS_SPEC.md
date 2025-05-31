# 🚀 Especificación Técnica Detallada Frontend Next.js para API Django

## 📋 Información Técnica del Backend

### 🔗 URLs del Backend
- **🌐 Aplicación**: https://apihack3r-production.up.railway.app
- **🔐 Admin Django**: https://apihack3r-production.up.railway.app/admin/
- **📚 API Docs (Swagger)**: https://apihack3r-production.up.railway.app/api/docs/
- **🚀 API Base URL**: https://apihack3r-production.up.railway.app/api/hl4/v1/

### 🗂️ Endpoints Específicos
```
BASE_URL = https://apihack3r-production.up.railway.app/api/hl4/v1

📊 AuditLog:
  GET    /auditlog/                     # Lista paginada
  GET    /auditlog/{id}/                # Detalle específico
  GET    /auditlog/resumen_actividad/   # Estadísticas 24h/7d
  GET    /auditlog/errores_recientes/   # Logs de error
  POST   /auditlog/limpiar_logs_antiguos/ # Limpieza (superuser)

📚 Conferencias:
  GET    /conferencias/                 # Lista con filtros
  POST   /conferencias/                 # Crear nueva
  GET    /conferencias/{id}/            # Detalle específico
  PUT    /conferencias/{id}/            # Actualizar completo
  PATCH  /conferencias/{id}/            # Actualización parcial
  DELETE /conferencias/{id}/            # Eliminar
  GET    /conferencias/proximas/        # Solo futuras
  GET    /conferencias/estadisticas/    # Stats generales

🎓 Cursos:
  GET    /cursos/                       # Lista con filtros
  POST   /cursos/                       # Crear nuevo
  GET    /cursos/{id}/                  # Detalle específico
  PUT    /cursos/{id}/                  # Actualizar completo
  PATCH  /cursos/{id}/                  # Actualización parcial
  DELETE /cursos/{id}/                  # Eliminar
  GET    /cursos/activos/               # Solo activos

👥 Integrantes:
  GET    /integrantes/                  # Lista con filtros
  POST   /integrantes/                  # Crear nuevo
  GET    /integrantes/{id}/             # Detalle específico
  PUT    /integrantes/{id}/             # Actualizar completo
  PATCH  /integrantes/{id}/             # Actualización parcial
  DELETE /integrantes/{id}/             # Eliminar
  GET    /integrantes/activos/          # Solo activos
  GET    /integrantes/por_semestre/     # Agrupados por semestre

📰 Noticias:
  GET    /noticias/                     # Lista con filtros
  POST   /noticias/                     # Crear nueva
  GET    /noticias/{id}/                # Detalle específico
  PUT    /noticias/{id}/                # Actualizar completo
  PATCH  /noticias/{id}/                # Actualización parcial
  DELETE /noticias/{id}/                # Eliminar

💼 Ofertas de Empleo:
  GET    /ofertasempleo/                # Lista con filtros
  POST   /ofertasempleo/                # Crear nueva
  GET    /ofertasempleo/{id}/           # Detalle específico
  PUT    /ofertasempleo/{id}/           # Actualizar completo
  PATCH  /ofertasempleo/{id}/           # Actualización parcial
  DELETE /ofertasempleo/{id}/           # Eliminar
  GET    /ofertasempleo/vigentes/       # Solo vigentes
  GET    /ofertasempleo/expiradas/      # Solo expiradas
  POST   /ofertasempleo/limpiar_expiradas/ # Limpiar vencidas
  GET    /ofertasempleo/estadisticas/   # Stats generales

🚀 Proyectos:
  GET    /proyectos/                    # Lista con filtros
  POST   /proyectos/                    # Crear nuevo
  GET    /proyectos/{id}/               # Detalle específico
  PUT    /proyectos/{id}/               # Actualizar completo
  PATCH  /proyectos/{id}/               # Actualización parcial
  DELETE /proyectos/{id}/               # Eliminar
  GET    /proyectos/tecnologias_populares/ # Top 10 tecnologías
```

---

## 🔐 Sistema de Autenticación y Roles

### Autenticación
El sistema utiliza **Django Authentication** con email y contraseña:
- **Endpoint de login**: Usar Django REST Auth o crear endpoint personalizado
- **Campos**: `email` y `password`

### Roles de Usuario

#### 👑 **SUPERADMIN** (`is_superuser=True`)
- **Acceso**: Redirigir directamente al **Admin de Django**
- **URL**: https://apihack3r-production.up.railway.app/admin/
- **Permisos**: Control total del sistema

#### 🛡️ **ADMIN** (`is_staff=True`, `is_superuser=False`)
- **Panel personalizado** con acceso completo a:
  - ✅ **AuditLog** (Ver logs del sistema)
  - ✅ **CRUD completo** de todos los modelos
  - ✅ **Filtros avanzados** en todas las tablas
  - ✅ **Estadísticas** y reportes

#### 👤 **STAFF** (`is_staff=True` pero sin permisos de AuditLog)
- **Panel limitado** con acceso a:
  - ❌ **SIN acceso** a AuditLog
  - ✅ **CRUD completo** de todos los modelos (excepto AuditLog)
  - ✅ **Filtros avanzados** en todas las tablas

---

## 🎨 Diseño del Frontend

### 🏠 **Dashboard Principal**

#### Para ADMIN:
```
┌─────────────────────────────────────────────────────────┐
│ 📊 Dashboard Admin - Sistema de Gestión                │
├─────────────────────────────────────────────────────────┤
│ 🔍 AuditLog | 📚 Conferencias | 🎓 Cursos | 👥 Integrantes │
│ 📰 Noticias | 💼 Ofertas | 🚀 Proyectos              │
├─────────────────────────────────────────────────────────┤
│ [Cards con estadísticas y accesos rápidos]              │
└─────────────────────────────────────────────────────────┘
```

#### Para STAFF:
```
┌─────────────────────────────────────────────────────────┐
│ 📊 Dashboard Staff - Gestión de Contenido              │
├─────────────────────────────────────────────────────────┤
│ 📚 Conferencias | 🎓 Cursos | 👥 Integrantes           │
│ 📰 Noticias | 💼 Ofertas | 🚀 Proyectos              │
├─────────────────────────────────────────────────────────┤
│ [Cards con estadísticas y accesos rápidos]              │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Especificaciones por Modelo

### 🔍 **1. AuditLog** (Solo ADMIN)

#### Tabla con columnas:
- **ID** | **Usuario** | **Acción** | **Tabla** | **Timestamp** | **Detalles**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (accion, detalles, usuario)
- 📅 **Fecha desde**: `fecha_desde`
- 📅 **Fecha hasta**: `fecha_hasta`
- 👤 **Usuario**: Dropdown con usuarios del sistema
- 🎯 **Acción**: Dropdown (CREATE, UPDATE, DELETE, etc.)
- 📊 **Ordenamiento**: timestamp, accion, usuario

#### Acciones especiales:
- 📈 **Resumen de actividad** (últimas 24h y 7 días)
- ❌ **Errores recientes**
- 🧹 **Limpiar logs antiguos** (solo superusuarios)

---

### 📚 **2. Conferencias**

#### Tabla con columnas:
- **ID** | **Nombre** | **Ponente** | **Fecha** | **Descripción** | **Imagen** | **Link** | **Creador** | **Acciones**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (nombre, ponente, descripción)
- 📝 **Nombre**: `nombre` (contiene texto)
- 👨‍🏫 **Ponente**: `ponente` (contiene texto)
- 📅 **Fecha desde**: `fecha_desde`
- 📅 **Fecha hasta**: `fecha_hasta`
- 🔮 **Próximas**: `proximas` (boolean - solo futuras)
- 📊 **Ordenamiento**: fecha_conferencia, nombre_conferencia, ponente_conferencia

#### CRUD:
- ➕ **Crear**: Formulario con todos los campos + upload de imagen
- ✏️ **Editar**: Formulario pre-rellenado
- 🗑️ **Eliminar**: Confirmación
- 👀 **Ver**: Modal o página de detalles

#### Acciones especiales:
- 📅 **Próximas conferencias**
- 📊 **Estadísticas**

---

### 🎓 **3. Cursos**

#### Tabla con columnas:
- **ID** | **Nombre** | **Fecha Inicio** | **Fecha Fin** | **Descripción** | **Link** | **Creador** | **Estado** | **Acciones**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (nombre, descripción)
- 📝 **Nombre**: `nombre` (contiene texto)
- 📄 **Descripción**: `descripcion` (contiene texto)
- ✅ **Activos**: `activos` (boolean - cursos en progreso)
- 📊 **Ordenamiento**: nombre_curso, fechainicial_curso, fechafinal_curso

#### CRUD completo + Estados:
- 🟢 **Activo**: Curso en progreso
- 🔵 **Próximo**: Aún no ha iniciado
- 🔴 **Finalizado**: Ya terminó

#### Acciones especiales:
- ✅ **Cursos activos**

---

### 👥 **4. Integrantes**

#### Tabla con columnas:
- **ID** | **Nombre** | **Semestre** | **Correo** | **GitHub** | **Imagen** | **Estado** | **Reseña** | **Creador** | **Acciones**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (nombre, correo, reseña, semestre)
- 👤 **Nombre**: `nombre` (contiene texto)
- 🎓 **Semestre**: `semestre` (contiene texto)
- ✅ **Estado**: `estado` (boolean - activo/inactivo)
- 🛠️ **Habilidades**: `habilidades` (busca en reseña)
- 📊 **Ordenamiento**: nombre_integrante, semestre, correo

#### CRUD + Validaciones:
- 📧 **Email**: Validación de formato
- 🔗 **GitHub**: Validación de URL de GitHub
- 🖼️ **Imagen**: Upload a Cloudinary

#### Acciones especiales:
- ✅ **Integrantes activos**
- 📊 **Por semestre**

---

### 📰 **5. Noticias**

#### Tabla con columnas:
- **ID** | **Título** | **Fecha** | **Fuente** | **Descripción** | **Imagen** | **Link** | **Creador** | **Acciones**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (título, descripción)
- 📰 **Título**: `titulo` (contiene texto)
- 🏢 **Fuente**: `fuente` (contiene texto)
- 📅 **Fecha desde**: `fecha_desde`
- 🆕 **Recientes**: `recientes` (boolean - últimos 7 días)
- 📊 **Ordenamiento**: fecha_noticia, nombre_noticia

#### CRUD + Estado:
- 🆕 **Reciente**: Publicada en últimos 7 días
- 📅 **Normal**: Más de 7 días

---

### 💼 **6. Ofertas de Empleo**

#### Tabla con columnas:
- **ID** | **Título** | **Empresa** | **Fecha Pub.** | **Fecha Exp.** | **Descripción** | **Imagen** | **Link** | **Estado** | **Creador** | **Acciones**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (título, empresa, descripción)
- 💼 **Título**: `titulo` (contiene texto)
- 🏢 **Empresa**: `empresa` (contiene texto)
- ✅ **Vigentes**: `vigentes` (boolean - no expiradas)
- 📅 **Publicado desde**: `publicado_desde`
- 📊 **Ordenamiento**: fecha_publicacion, titulo_empleo, empresa, fecha_expiracion

#### CRUD + Estados:
- 🟢 **Vigente**: No ha expirado
- 🔴 **Expirada**: Fecha de expiración pasada

#### Acciones especiales:
- ✅ **Ofertas vigentes**
- ❌ **Ofertas expiradas**
- 🧹 **Limpiar expiradas**
- 📊 **Estadísticas**

---

### 🚀 **7. Proyectos**

#### Tabla con columnas:
- **ID** | **Nombre** | **Fecha** | **Descripción** | **Link** | **Integrantes** | **Creador** | **Acciones**

#### Filtros disponibles:
- 🔍 **Búsqueda**: `search` (nombre, descripción)
- 🚀 **Nombre**: `nombre` (contiene texto)
- 💻 **Tecnología**: `tecnologia` (busca en descripción)
- 📊 **Ordenamiento**: nombre_proyecto, fecha_proyecto

#### CRUD + Relaciones:
- 👥 **Gestión de integrantes**: Many-to-Many con tabla intermedia
- 📊 **Conteo de integrantes**

#### Acciones especiales:
- 📈 **Tecnologías populares**

---

## 🎨 Diseño UI/UX Recomendado

### 🎨 **Paleta de Colores**
```css
:root {
  --primary: #3B82F6;     /* Azul principal */
  --secondary: #1F2937;   /* Gris oscuro */
  --success: #10B981;     /* Verde */
  --warning: #F59E0B;     /* Amarillo */
  --danger: #EF4444;      /* Rojo */
  --info: #06B6D4;        /* Cyan */
  --background: #F9FAFB;  /* Fondo claro */
}
```

### 📱 **Layout Responsivo**
- **Desktop**: Sidebar + contenido principal
- **Tablet**: Sidebar colapsible
- **Mobile**: Navegación bottom tabs

### 🧩 **Componentes Clave**

#### 📊 **DataTable Component**
```tsx
interface DataTableProps {
  data: any[];
  columns: Column[];
  filters: FilterConfig[];
  searchable: boolean;
  sortable: boolean;
  pagination: boolean;
  actions: Action[];
}
```

#### 🔍 **FilterPanel Component**
```tsx
interface FilterPanelProps {
  filters: FilterConfig[];
  onFilterChange: (filters: any) => void;
  onReset: () => void;
}
```

#### 📝 **CRUDModal Component**
```tsx
interface CRUDModalProps {
  isOpen: boolean;
  mode: 'create' | 'edit' | 'view';
  data?: any;
  onSave: (data: any) => void;
  onClose: () => void;
}
```

---

## 🔧 Stack Tecnológico Recomendado

### ⚛️ **Frontend**
- **Framework**: Next.js 14+ (App Router)
- **UI Library**: TailwindCSS + Headless UI
- **State**: Zustand o Redux Toolkit
- **HTTP**: Axios con interceptores
- **Forms**: React Hook Form + Zod
- **Tables**: TanStack Table v8
- **Icons**: Heroicons o Lucide
- **Notifications**: React Hot Toast

### 📦 **Dependencias Principales**
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "tailwindcss": "^3.0.0",
    "@headlessui/react": "^1.7.0",
    "axios": "^1.5.0",
    "zustand": "^4.4.0",
    "react-hook-form": "^7.45.0",
    "zod": "^3.22.0",
    "@tanstack/react-table": "^8.10.0",
    "react-hot-toast": "^2.4.0",
    "@heroicons/react": "^2.0.0"
  }
}
```

---

## 🔄 Flujo de Autenticación

### 1. **Login Flow**
```
📱 Login Form (email + password)
    ↓
🔐 POST /api/auth/login/
    ↓
🎯 Check user.is_superuser
    ↓ (true)
🚀 Redirect to Django Admin
    ↓ (false)
🎯 Check user.is_staff
    ↓ (true)
📊 Dashboard (with/without AuditLog based on permissions)
    ↓ (false)
❌ Access Denied
```

### 2. **Permission Checking**
```typescript
interface User {
  id: number;
  username: string;
  email: string;
  is_superuser: boolean;
  is_staff: boolean;
  is_active: boolean;
  groups: string[];
}

const hasAuditLogAccess = (user: User): boolean => {
  return user.is_superuser || user.groups.includes('Admin');
};
```

---

## 📊 API Integration

### 🔌 **Axios Configuration**
```typescript
const apiClient = axios.create({
  baseURL: 'https://apihack3r-production.up.railway.app/api/hl4/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 📋 **CRUD Operations**
```typescript
// GET with filters
const getConferencias = async (filters: ConferenciasFilters) => {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== null && value !== '') {
      params.append(key, value.toString());
    }
  });
  
  return apiClient.get(`/conferencias/?${params}`);
};

// POST
const createConferencia = async (data: ConferenciaCreate) => {
  return apiClient.post('/conferencias/', data);
};

// PUT
const updateConferencia = async (id: number, data: ConferenciaUpdate) => {
  return apiClient.put(`/conferencias/${id}/`, data);
};

// DELETE
const deleteConferencia = async (id: number) => {
  return apiClient.delete(`/conferencias/${id}/`);
};
```

---

## 🎯 Implementación Paso a Paso

### Fase 1: Configuración Base
1. ⚙️ Setup Next.js + TailwindCSS
2. 🔐 Implementar autenticación
3. 🧭 Configurar routing y layout
4. 📱 Crear componentes base (DataTable, FilterPanel)

### Fase 2: Dashboard y AuditLog
1. 📊 Dashboard principal para Admin/Staff
2. 🔍 Módulo AuditLog completo (solo Admin)
3. 📈 Estadísticas y reportes

### Fase 3: CRUD Modules
1. 📚 Conferencias
2. 🎓 Cursos  
3. 👥 Integrantes
4. 📰 Noticias

### Fase 4: CRUD Avanzado
1. 💼 Ofertas de Empleo
2. 🚀 Proyectos (con relaciones Many-to-Many)

### Fase 5: Optimización
1. 🔄 Loading states y skeleton screens
2. ❌ Error handling robusto
3. 📱 Optimización móvil
4. 🔍 SEO y metadatos

---

## 🔥 Funcionalidades Especiales

### 📊 **Dashboard Widgets**
- 📈 Gráficos de actividad (Chart.js)
- 🎯 KPIs principales
- 🔔 Notificaciones recientes
- ⚡ Accesos rápidos

### 🔍 **Búsqueda Global**
- 🔍 Search across all models
- 🎯 Filtros persistentes
- 📚 Historial de búsquedas

### 📱 **Responsive Design**
- 💻 Desktop-first
- 📱 Mobile optimization
- 🖥️ Tablet-friendly

### ⚡ **Performance**
- 🔄 Lazy loading
- 📦 Code splitting
- 💾 Client-side caching

---

## 🚀 Deploy Recommendations

### ▲ **Vercel** (Recomendado)
```bash
npm run build
vercel --prod
```

### 🐳 **Docker** (Alternativo)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 🎉 Resultado Final Esperado

El frontend debe proporcionar:

✅ **Autenticación robusta** con roles diferenciados  
✅ **Dashboard intuitivo** para Admin y Staff  
✅ **CRUD completo** para todos los modelos  
✅ **Filtros avanzados** en todas las tablas  
✅ **UI moderna** y responsive  
✅ **Performance optimizada**  
✅ **Experiencia de usuario fluida**  

### 🎯 **Login Redirect Logic**:
- `is_superuser=true` → Django Admin  
- `is_staff=true + Admin group` → Dashboard con AuditLog  
- `is_staff=true + Staff group` → Dashboard sin AuditLog  
- Otros → Access Denied  

¡Con esta especificación tendrás un frontend completo y profesional para tu API Django! 🚀
