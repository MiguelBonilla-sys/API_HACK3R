-- Script para corregir y crear triggers de auditoría
-- Fecha: 2024
-- Descripción: Este script corrige los problemas con los triggers de auditoría

-- ====================================================================
-- LIMPIEZA INICIAL
-- ====================================================================

-- Eliminamos triggers existentes si existen
DROP TRIGGER IF EXISTS trigger_log_conferencias_insert ON blog_conferencias;
DROP TRIGGER IF EXISTS trigger_log_conferencias_update ON blog_conferencias;
DROP TRIGGER IF EXISTS trigger_log_conferencias_delete ON blog_conferencias;

DROP TRIGGER IF EXISTS trigger_log_integrantes_insert ON blog_integrantes;
DROP TRIGGER IF EXISTS trigger_log_integrantes_update ON blog_integrantes;
DROP TRIGGER IF EXISTS trigger_log_integrantes_delete ON blog_integrantes;

DROP TRIGGER IF EXISTS trigger_log_noticias_insert ON blog_noticias;
DROP TRIGGER IF EXISTS trigger_log_noticias_update ON blog_noticias;
DROP TRIGGER IF EXISTS trigger_log_noticias_delete ON blog_noticias;

DROP TRIGGER IF EXISTS trigger_log_cursos_insert ON blog_cursos;
DROP TRIGGER IF EXISTS trigger_log_cursos_update ON blog_cursos;
DROP TRIGGER IF EXISTS trigger_log_cursos_delete ON blog_cursos;

-- Eliminamos funciones existentes
DROP FUNCTION IF EXISTS log_conferencias_insert();
DROP FUNCTION IF EXISTS log_conferencias_update();
DROP FUNCTION IF EXISTS log_conferencias_delete();

DROP FUNCTION IF EXISTS log_integrantes_insert();
DROP FUNCTION IF EXISTS log_integrantes_update();
DROP FUNCTION IF EXISTS log_integrantes_delete();

DROP FUNCTION IF EXISTS log_noticias_insert();
DROP FUNCTION IF EXISTS log_noticias_update();
DROP FUNCTION IF EXISTS log_noticias_delete();

DROP FUNCTION IF EXISTS log_cursos_insert();
DROP FUNCTION IF EXISTS log_cursos_update();
DROP FUNCTION IF EXISTS log_cursos_delete();

-- ====================================================================
-- FUNCIONES CORREGIDAS PARA CONFERENCIAS
-- ====================================================================

CREATE OR REPLACE FUNCTION log_conferencias_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_conferencias', 
        'CREATE',
        NEW.idconferencia,
        json_build_object(
            'nombre_conferencia', NEW.nombre_conferencia,
            'ponente_conferencia', NEW.ponente_conferencia,
            'fecha_conferencia', NEW.fecha_conferencia,
            'descripcion_conferencia', NEW.descripcion_conferencia,
            'imagen_conferencia', substring(NEW.imagen_conferencia from '/([^/]+)/?$'),
            'link_conferencia', NEW.link_conferencia
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_conferencias_update */
CREATE OR REPLACE FUNCTION log_conferencias_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_conferencias', 
        'UPDATE',
        NEW.idconferencia,
        json_build_object(
            'old_nombre_conferencia', OLD.nombre_conferencia,
            'new_nombre_conferencia', NEW.nombre_conferencia,
            'old_ponente_conferencia', OLD.ponente_conferencia,
            'new_ponente_conferencia', NEW.ponente_conferencia,
            'old_fecha_conferencia', OLD.fecha_conferencia,
            'new_fecha_conferencia', NEW.fecha_conferencia,
            'old_descripcion_conferencia', OLD.descripcion_conferencia,
            'new_descripcion_conferencia', NEW.descripcion_conferencia,
            'old_imagen_conferencia', substring(OLD.imagen_conferencia from '/([^/]+)/?$'),
            'new_imagen_conferencia', substring(NEW.imagen_conferencia from '/([^/]+)/?$'),
            'old_link_conferencia', OLD.link_conferencia,
            'new_link_conferencia', NEW.link_conferencia
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_conferencias_delete */
CREATE OR REPLACE FUNCTION log_conferencias_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        OLD.creador_id, 
        'blog_conferencias', 
        'DELETE',
        OLD.idconferencia,
        json_build_object(
            'nombre_conferencia', OLD.nombre_conferencia,
            'ponente_conferencia', OLD.ponente_conferencia,
            'fecha_conferencia', OLD.fecha_conferencia,
            'descripcion_conferencia', OLD.descripcion_conferencia,
            'imagen_conferencia', substring(OLD.imagen_conferencia from '/([^/]+)/?$'),
            'link_conferencia', OLD.link_conferencia
        )
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- FUNCIONES CORREGIDAS PARA INTEGRANTES
-- ====================================================================

/* Función: log_integrantes_insert */
CREATE OR REPLACE FUNCTION log_integrantes_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_integrantes', 
        'CREATE',  -- Cambiado de 'ADD' a 'CREATE'
        NEW.idintegrantes,
        json_build_object(
            'nombre_integrante', NEW.nombre_integrante,
            'semestre', NEW.semestre,
            'correo', NEW.correo,
            'link_git', NEW.link_git,
            'reseña', NEW.reseña,
            'estado', NEW.estado,
            'imagen', substring(NEW.imagen from '/([^/]+)/?$')
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_integrantes_update */
CREATE OR REPLACE FUNCTION log_integrantes_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_integrantes', 
        'UPDATE',
        NEW.idintegrantes,
        json_build_object(
            'old_nombre_integrante', OLD.nombre_integrante,
            'new_nombre_integrante', NEW.nombre_integrante,
            'old_semestre', OLD.semestre,
            'new_semestre', NEW.semestre,
            'old_correo', OLD.correo,
            'new_correo', NEW.correo,
            'old_link_git', OLD.link_git,
            'new_link_git', NEW.link_git,
            'old_reseña', OLD.reseña,
            'new_reseña', NEW.reseña,
            'old_estado', OLD.estado,
            'new_estado', NEW.estado,
            'old_imagen', substring(OLD.imagen from '/([^/]+)/?$'),
            'new_imagen', substring(NEW.imagen from '/([^/]+)/?$')
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_integrantes_delete */
CREATE OR REPLACE FUNCTION log_integrantes_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        OLD.creador_id, 
        'blog_integrantes', 
        'DELETE',
        OLD.idintegrantes,
        json_build_object(
            'nombre_integrante', OLD.nombre_integrante,
            'semestre', OLD.semestre,
            'correo', OLD.correo,
            'link_git', OLD.link_git,
            'reseña', OLD.reseña,
            'estado', OLD.estado,
            'imagen', substring(OLD.imagen from '/([^/]+)/?$')
        )
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- FUNCIONES CORREGIDAS PARA NOTICIAS
-- ====================================================================

/* Función: log_noticias_insert */
CREATE OR REPLACE FUNCTION log_noticias_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_noticias', 
        'CREATE',  -- Cambiado de 'ADD' a 'CREATE'
        NEW.idnoticia,
        json_build_object(
            'nombre_noticia', NEW.nombre_noticia,
            'fecha_noticia', NEW.fecha_noticia,
            'link_noticia', NEW.link_noticia,
            'description_noticia', NEW.description_noticia,
            'fuente', NEW.fuente,
            'imagen_noticia', substring(NEW.imagen_noticia from '/([^/]+)/?$')
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_noticias_update */
CREATE OR REPLACE FUNCTION log_noticias_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_noticias', 
        'UPDATE',
        NEW.idnoticia,
        json_build_object(
            'old_nombre_noticia', OLD.nombre_noticia,
            'new_nombre_noticia', NEW.nombre_noticia,
            'old_fecha_noticia', OLD.fecha_noticia,
            'new_fecha_noticia', NEW.fecha_noticia,
            'old_link_noticia', OLD.link_noticia,
            'new_link_noticia', NEW.link_noticia,
            'old_description_noticia', OLD.description_noticia,
            'new_description_noticia', NEW.description_noticia,
            'old_fuente', OLD.fuente,
            'new_fuente', NEW.fuente,
            'old_imagen_noticia', substring(OLD.imagen_noticia from '/([^/]+)/?$'),
            'new_imagen_noticia', substring(NEW.imagen_noticia from '/([^/]+)/?$')
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_noticias_delete */
CREATE OR REPLACE FUNCTION log_noticias_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        OLD.creador_id, 
        'blog_noticias', 
        'DELETE',
        OLD.idnoticia,
        json_build_object(
            'nombre_noticia', OLD.nombre_noticia,
            'fecha_noticia', OLD.fecha_noticia,
            'link_noticia', OLD.link_noticia,
            'description_noticia', OLD.description_noticia,
            'fuente', OLD.fuente,
            'imagen_noticia', substring(OLD.imagen_noticia from '/([^/]+)/?$')
        )
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- FUNCIONES CORREGIDAS PARA CURSOS
-- ====================================================================

/* Función: log_cursos_insert */
CREATE OR REPLACE FUNCTION log_cursos_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_cursos', 
        'CREATE',  -- Cambiado de 'ADD' a 'CREATE'
        NEW.idcursos,
        json_build_object(
            'nombre_curso', NEW.nombre_curso,
            'fechainicial_curso', NEW.fechainicial_curso,
            'fechafinal_curso', NEW.fechafinal_curso,
            'link_curso', NEW.link_curso,
            'descripcion_curso', NEW.descripcion_curso
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_cursos_update */
CREATE OR REPLACE FUNCTION log_cursos_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_cursos', 
        'UPDATE',
        NEW.idcursos,
        json_build_object(
            'old_nombre_curso', OLD.nombre_curso,
            'new_nombre_curso', NEW.nombre_curso,
            'old_fechainicial_curso', OLD.fechainicial_curso,
            'new_fechainicial_curso', NEW.fechainicial_curso,
            'old_fechafinal_curso', OLD.fechafinal_curso,
            'new_fechafinal_curso', NEW.fechafinal_curso,
            'old_link_curso', OLD.link_curso,
            'new_link_curso', NEW.link_curso,
            'old_descripcion_curso', OLD.descripcion_curso,
            'new_descripcion_curso', NEW.descripcion_curso
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* Función: log_cursos_delete */
CREATE OR REPLACE FUNCTION log_cursos_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        OLD.creador_id, 
        'blog_cursos', 
        'DELETE',
        OLD.idcursos,
        json_build_object(
            'nombre_curso', OLD.nombre_curso,
            'fechainicial_curso', OLD.fechainicial_curso,
            'fechafinal_curso', OLD.fechafinal_curso,
            'link_curso', OLD.link_curso,
            'descripcion_curso', OLD.descripcion_curso
        )
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- CREACIÓN DE TRIGGERS EN LAS TABLAS
-- ====================================================================

-- Triggers para Conferencias
CREATE TRIGGER trigger_log_conferencias_insert
    AFTER INSERT ON blog_conferencias
    FOR EACH ROW EXECUTE FUNCTION log_conferencias_insert();

CREATE OR REPLACE FUNCTION log_conferencias_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_conferencias', 
        'UPDATE',
        NEW.idconferencia,
        json_build_object(
            'old_nombre_conferencia', OLD.nombre_conferencia,
            'new_nombre_conferencia', NEW.nombre_conferencia,
            'old_ponente_conferencia', OLD.ponente_conferencia,
            'new_ponente_conferencia', NEW.ponente_conferencia,
            'old_fecha_conferencia', OLD.fecha_conferencia,
            'new_fecha_conferencia', NEW.fecha_conferencia,
            'old_descripcion_conferencia', OLD.descripcion_conferencia,
            'new_descripcion_conferencia', NEW.descripcion_conferencia,
            'old_imagen_conferencia', substring(OLD.imagen_conferencia from '/([^/]+)/?$'),
            'new_imagen_conferencia', substring(NEW.imagen_conferencia from '/([^/]+)/?$'),
            'old_link_conferencia', OLD.link_conferencia,
            'new_link_conferencia', NEW.link_conferencia
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION log_conferencias_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        OLD.creador_id, 
        'blog_conferencias', 
        'DELETE',
        OLD.idconferencia,
        json_build_object(
            'nombre_conferencia', OLD.nombre_conferencia,
            'ponente_conferencia', OLD.ponente_conferencia,
            'fecha_conferencia', OLD.fecha_conferencia,
            'descripcion_conferencia', OLD.descripcion_conferencia,
            'imagen_conferencia', substring(OLD.imagen_conferencia from '/([^/]+)/?$'),
            'link_conferencia', OLD.link_conferencia
        )
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGERS PARA INTEGRANTES
CREATE OR REPLACE FUNCTION log_integrantes_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_integrantes', 
        'CREATE',
        NEW.idintegrantes,
        json_build_object(
            'nombre_integrante', NEW.nombre_integrante,
            'semestre', NEW.semestre,
            'correo', NEW.correo,
            'link_git', NEW.link_git,
            'reseña', NEW.reseña,
            'estado', NEW.estado,
            'imagen', substring(NEW.imagen from '/([^/]+)/?$')
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION log_integrantes_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        NEW.creador_id, 
        'blog_integrantes', 
        'UPDATE',
        NEW.idintegrantes,
        json_build_object(
            'old_nombre_integrante', OLD.nombre_integrante,
            'new_nombre_integrante', NEW.nombre_integrante,
            'old_semestre', OLD.semestre,
            'new_semestre', NEW.semestre,
            'old_correo', OLD.correo,
            'new_correo', NEW.correo,
            'old_link_git', OLD.link_git,
            'new_link_git', NEW.link_git,
            'old_reseña', OLD.reseña,
            'new_reseña', NEW.reseña,
            'old_estado', OLD.estado,
            'new_estado', NEW.estado,
            'old_imagen', substring(OLD.imagen from '/([^/]+)/?$'),
            'new_imagen', substring(NEW.imagen from '/([^/]+)/?$')
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION log_integrantes_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO blog_auditlog (
        timestamp, 
        user_id, 
        table_name, 
        change_type, 
        affected_record_id, 
        modified_data
    )
    VALUES (
        NOW(), 
        OLD.creador_id, 
        'blog_integrantes', 
        'DELETE',
        OLD.idintegrantes,
        json_build_object(
            'nombre_integrante', OLD.nombre_integrante,
            'semestre', OLD.semestre,
            'correo', OLD.correo,
            'link_git', OLD.link_git,
            'reseña', OLD.reseña,
            'estado', OLD.estado,
            'imagen', substring(OLD.imagen from '/([^/]+)/?$')
        )
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGERS COMPLETOS
CREATE TRIGGER trigger_log_conferencias_update
    AFTER UPDATE ON blog_conferencias
    FOR EACH ROW EXECUTE FUNCTION log_conferencias_update();

CREATE TRIGGER trigger_log_conferencias_delete
    BEFORE DELETE ON blog_conferencias
    FOR EACH ROW EXECUTE FUNCTION log_conferencias_delete();

CREATE TRIGGER trigger_log_integrantes_insert
    AFTER INSERT ON blog_integrantes
    FOR EACH ROW EXECUTE FUNCTION log_integrantes_insert();

CREATE TRIGGER trigger_log_integrantes_update
    AFTER UPDATE ON blog_integrantes
    FOR EACH ROW EXECUTE FUNCTION log_integrantes_update();

CREATE TRIGGER trigger_log_integrantes_delete
    BEFORE DELETE ON blog_integrantes
    FOR EACH ROW EXECUTE FUNCTION log_integrantes_delete();

-- VERIFICACIÓN FINAL
SELECT 
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation
FROM information_schema.triggers 
WHERE trigger_schema = 'public' 
    AND trigger_name LIKE 'trigger_log_%'
ORDER BY event_object_table, trigger_name;

CREATE TRIGGER trigger_log_conferencias_update
    AFTER UPDATE ON blog_conferencias
    FOR EACH ROW EXECUTE FUNCTION log_conferencias_update();

CREATE TRIGGER trigger_log_conferencias_delete
    BEFORE DELETE ON blog_conferencias
    FOR EACH ROW EXECUTE FUNCTION log_conferencias_delete();

-- Triggers para Integrantes
CREATE TRIGGER trigger_log_integrantes_insert
    AFTER INSERT ON blog_integrantes
    FOR EACH ROW EXECUTE FUNCTION log_integrantes_insert();

CREATE TRIGGER trigger_log_integrantes_update
    AFTER UPDATE ON blog_integrantes
    FOR EACH ROW EXECUTE FUNCTION log_integrantes_update();

CREATE TRIGGER trigger_log_integrantes_delete
    BEFORE DELETE ON blog_integrantes
    FOR EACH ROW EXECUTE FUNCTION log_integrantes_delete();

-- Triggers para Noticias
CREATE TRIGGER trigger_log_noticias_insert
    AFTER INSERT ON blog_noticias
    FOR EACH ROW EXECUTE FUNCTION log_noticias_insert();

CREATE TRIGGER trigger_log_noticias_update
    AFTER UPDATE ON blog_noticias
    FOR EACH ROW EXECUTE FUNCTION log_noticias_update();

CREATE TRIGGER trigger_log_noticias_delete
    BEFORE DELETE ON blog_noticias
    FOR EACH ROW EXECUTE FUNCTION log_noticias_delete();

-- Triggers para Cursos
CREATE TRIGGER trigger_log_cursos_insert
    AFTER INSERT ON blog_cursos
    FOR EACH ROW EXECUTE FUNCTION log_cursos_insert();

CREATE TRIGGER trigger_log_cursos_update
    AFTER UPDATE ON blog_cursos
    FOR EACH ROW EXECUTE FUNCTION log_cursos_update();

CREATE TRIGGER trigger_log_cursos_delete
    BEFORE DELETE ON blog_cursos
    FOR EACH ROW EXECUTE FUNCTION log_cursos_delete();

-- ====================================================================
-- VERIFICACIÓN DE TRIGGERS CREADOS
-- ====================================================================

-- Query para verificar que los triggers se crearon correctamente
SELECT 
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation
FROM information_schema.triggers 
WHERE trigger_schema = 'public' 
    AND trigger_name LIKE 'trigger_log_%'
ORDER BY event_object_table, trigger_name; 