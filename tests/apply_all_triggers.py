import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def apply_integrantes_triggers():
    """Aplica triggers para la tabla integrantes."""
    sql_script = """
    -- Eliminar triggers existentes de integrantes
    DROP TRIGGER IF EXISTS trigger_log_integrantes_insert ON blog_integrantes;
    DROP TRIGGER IF EXISTS trigger_log_integrantes_update ON blog_integrantes;
    DROP TRIGGER IF EXISTS trigger_log_integrantes_delete ON blog_integrantes;
    
    -- Eliminar funciones existentes
    DROP FUNCTION IF EXISTS log_integrantes_insert();
    DROP FUNCTION IF EXISTS log_integrantes_update();
    DROP FUNCTION IF EXISTS log_integrantes_delete();

    -- Función INSERT para integrantes
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
                'imagen', NEW.imagen
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función UPDATE para integrantes
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
                'old_estado', OLD.estado,
                'new_estado', NEW.estado,
                'old_correo', OLD.correo,
                'new_correo', NEW.correo
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función DELETE para integrantes
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
                'estado', OLD.estado
            )
        );
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear triggers para integrantes
    CREATE TRIGGER trigger_log_integrantes_insert
        AFTER INSERT ON blog_integrantes
        FOR EACH ROW EXECUTE FUNCTION log_integrantes_insert();

    CREATE TRIGGER trigger_log_integrantes_update
        AFTER UPDATE ON blog_integrantes
        FOR EACH ROW EXECUTE FUNCTION log_integrantes_update();

    CREATE TRIGGER trigger_log_integrantes_delete
        BEFORE DELETE ON blog_integrantes
        FOR EACH ROW EXECUTE FUNCTION log_integrantes_delete();
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        print("✅ Triggers de integrantes aplicados!")
        return True
    except Exception as e:
        print(f"❌ Error en integrantes: {e}")
        return False

def apply_noticias_triggers():
    """Aplica triggers para la tabla noticias."""
    sql_script = """
    -- Eliminar triggers existentes de noticias
    DROP TRIGGER IF EXISTS trigger_log_noticias_insert ON blog_noticias;
    DROP TRIGGER IF EXISTS trigger_log_noticias_update ON blog_noticias;
    DROP TRIGGER IF EXISTS trigger_log_noticias_delete ON blog_noticias;
    
    -- Eliminar funciones existentes
    DROP FUNCTION IF EXISTS log_noticias_insert();
    DROP FUNCTION IF EXISTS log_noticias_update();
    DROP FUNCTION IF EXISTS log_noticias_delete();

    -- Función INSERT para noticias
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
            'CREATE',
            NEW.idnoticia,
            json_build_object(
                'nombre_noticia', NEW.nombre_noticia,
                'fecha_noticia', NEW.fecha_noticia,
                'link_noticia', NEW.link_noticia,
                'description_noticia', NEW.description_noticia,
                'fuente', NEW.fuente,
                'imagen_noticia', NEW.imagen_noticia
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función UPDATE para noticias
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
                'old_fuente', OLD.fuente,
                'new_fuente', NEW.fuente
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función DELETE para noticias
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
                'fuente', OLD.fuente
            )
        );
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear triggers para noticias
    CREATE TRIGGER trigger_log_noticias_insert
        AFTER INSERT ON blog_noticias
        FOR EACH ROW EXECUTE FUNCTION log_noticias_insert();

    CREATE TRIGGER trigger_log_noticias_update
        AFTER UPDATE ON blog_noticias
        FOR EACH ROW EXECUTE FUNCTION log_noticias_update();

    CREATE TRIGGER trigger_log_noticias_delete
        BEFORE DELETE ON blog_noticias
        FOR EACH ROW EXECUTE FUNCTION log_noticias_delete();
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        print("✅ Triggers de noticias aplicados!")
        return True
    except Exception as e:
        print(f"❌ Error en noticias: {e}")
        return False

def apply_cursos_triggers():
    """Aplica triggers para la tabla cursos."""
    sql_script = """
    -- Eliminar triggers existentes de cursos
    DROP TRIGGER IF EXISTS trigger_log_cursos_insert ON blog_cursos;
    DROP TRIGGER IF EXISTS trigger_log_cursos_update ON blog_cursos;
    DROP TRIGGER IF EXISTS trigger_log_cursos_delete ON blog_cursos;
    
    -- Eliminar funciones existentes
    DROP FUNCTION IF EXISTS log_cursos_insert();
    DROP FUNCTION IF EXISTS log_cursos_update();
    DROP FUNCTION IF EXISTS log_cursos_delete();

    -- Función INSERT para cursos
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
            'CREATE',
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

    -- Función UPDATE para cursos
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
                'new_fechainicial_curso', NEW.fechainicial_curso
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función DELETE para cursos
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
                'fechafinal_curso', OLD.fechafinal_curso
            )
        );
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear triggers para cursos
    CREATE TRIGGER trigger_log_cursos_insert
        AFTER INSERT ON blog_cursos
        FOR EACH ROW EXECUTE FUNCTION log_cursos_insert();

    CREATE TRIGGER trigger_log_cursos_update
        AFTER UPDATE ON blog_cursos
        FOR EACH ROW EXECUTE FUNCTION log_cursos_update();

    CREATE TRIGGER trigger_log_cursos_delete
        BEFORE DELETE ON blog_cursos
        FOR EACH ROW EXECUTE FUNCTION log_cursos_delete();
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        print("✅ Triggers de cursos aplicados!")
        return True
    except Exception as e:
        print(f"❌ Error en cursos: {e}")
        return False

def verify_all_triggers():
    """Verifica que todos los triggers estén instalados."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                trigger_name,
                event_object_table,
                action_timing,
                event_manipulation
            FROM information_schema.triggers 
            WHERE trigger_schema = 'public' 
                AND trigger_name LIKE 'trigger_log_%'
            ORDER BY event_object_table, trigger_name;
        """)
        
        triggers = cursor.fetchall()
        
        print(f"\n📊 Total de triggers instalados: {len(triggers)}")
        if triggers:
            tables = set(trigger[1] for trigger in triggers)
            print(f"📋 Tablas con auditoría: {', '.join(tables)}")
            for trigger in triggers:
                print(f"   - {trigger[0]} en {trigger[1]} ({trigger[2]} {trigger[3]})")
        
        return len(triggers)

if __name__ == "__main__":
    print("🔧 APLICANDO TODOS LOS TRIGGERS DE AUDITORÍA")
    print("=" * 50)
    
    success_count = 0
    
    print("📋 Aplicando triggers de integrantes...")
    if apply_integrantes_triggers():
        success_count += 1
    
    print("📋 Aplicando triggers de noticias...")
    if apply_noticias_triggers():
        success_count += 1
    
    print("📋 Aplicando triggers de cursos...")
    if apply_cursos_triggers():
        success_count += 1
    
    print(f"\n✅ {success_count}/3 grupos de triggers aplicados correctamente")
    
    trigger_count = verify_all_triggers()
    
    if trigger_count >= 12:  # 4 tablas x 3 triggers cada una
        print("\n🎉 ¡SISTEMA DE AUDITORÍA COMPLETO INSTALADO!")
    else:
        print(f"\n⚠️  Sistema parcialmente instalado ({trigger_count} triggers)") 