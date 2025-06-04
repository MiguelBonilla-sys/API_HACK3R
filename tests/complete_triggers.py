import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def apply_remaining_triggers():
    # Script SQL con todas las funciones y triggers restantes
    sql = """
    -- INTEGRANTES
    DROP TRIGGER IF EXISTS trigger_log_integrantes_insert ON blog_integrantes;
    DROP TRIGGER IF EXISTS trigger_log_integrantes_update ON blog_integrantes;
    DROP TRIGGER IF EXISTS trigger_log_integrantes_delete ON blog_integrantes;
    DROP FUNCTION IF EXISTS log_integrantes_insert();
    DROP FUNCTION IF EXISTS log_integrantes_update();
    DROP FUNCTION IF EXISTS log_integrantes_delete();

    CREATE OR REPLACE FUNCTION log_integrantes_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), NEW.creador_id, 'blog_integrantes', 'CREATE', NEW.idintegrantes,
                json_build_object('nombre_integrante', NEW.nombre_integrante, 'semestre', NEW.semestre, 'correo', NEW.correo, 'estado', NEW.estado));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION log_integrantes_update()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), NEW.creador_id, 'blog_integrantes', 'UPDATE', NEW.idintegrantes,
                json_build_object('old_nombre', OLD.nombre_integrante, 'new_nombre', NEW.nombre_integrante, 'old_estado', OLD.estado, 'new_estado', NEW.estado));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION log_integrantes_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), OLD.creador_id, 'blog_integrantes', 'DELETE', OLD.idintegrantes,
                json_build_object('nombre_integrante', OLD.nombre_integrante, 'correo', OLD.correo));
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_log_integrantes_insert AFTER INSERT ON blog_integrantes FOR EACH ROW EXECUTE FUNCTION log_integrantes_insert();
    CREATE TRIGGER trigger_log_integrantes_update AFTER UPDATE ON blog_integrantes FOR EACH ROW EXECUTE FUNCTION log_integrantes_update();
    CREATE TRIGGER trigger_log_integrantes_delete BEFORE DELETE ON blog_integrantes FOR EACH ROW EXECUTE FUNCTION log_integrantes_delete();

    -- NOTICIAS
    DROP TRIGGER IF EXISTS trigger_log_noticias_insert ON blog_noticias;
    DROP TRIGGER IF EXISTS trigger_log_noticias_update ON blog_noticias;
    DROP TRIGGER IF EXISTS trigger_log_noticias_delete ON blog_noticias;
    DROP FUNCTION IF EXISTS log_noticias_insert();
    DROP FUNCTION IF EXISTS log_noticias_update();
    DROP FUNCTION IF EXISTS log_noticias_delete();

    CREATE OR REPLACE FUNCTION log_noticias_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), NEW.creador_id, 'blog_noticias', 'CREATE', NEW.idnoticia,
                json_build_object('nombre_noticia', NEW.nombre_noticia, 'fuente', NEW.fuente, 'fecha_noticia', NEW.fecha_noticia));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION log_noticias_update()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), NEW.creador_id, 'blog_noticias', 'UPDATE', NEW.idnoticia,
                json_build_object('old_nombre', OLD.nombre_noticia, 'new_nombre', NEW.nombre_noticia, 'old_fuente', OLD.fuente, 'new_fuente', NEW.fuente));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION log_noticias_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), OLD.creador_id, 'blog_noticias', 'DELETE', OLD.idnoticia,
                json_build_object('nombre_noticia', OLD.nombre_noticia, 'fuente', OLD.fuente));
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_log_noticias_insert AFTER INSERT ON blog_noticias FOR EACH ROW EXECUTE FUNCTION log_noticias_insert();
    CREATE TRIGGER trigger_log_noticias_update AFTER UPDATE ON blog_noticias FOR EACH ROW EXECUTE FUNCTION log_noticias_update();
    CREATE TRIGGER trigger_log_noticias_delete BEFORE DELETE ON blog_noticias FOR EACH ROW EXECUTE FUNCTION log_noticias_delete();

    -- CURSOS
    DROP TRIGGER IF EXISTS trigger_log_cursos_insert ON blog_cursos;
    DROP TRIGGER IF EXISTS trigger_log_cursos_update ON blog_cursos;
    DROP TRIGGER IF EXISTS trigger_log_cursos_delete ON blog_cursos;
    DROP FUNCTION IF EXISTS log_cursos_insert();
    DROP FUNCTION IF EXISTS log_cursos_update();
    DROP FUNCTION IF EXISTS log_cursos_delete();

    CREATE OR REPLACE FUNCTION log_cursos_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), NEW.creador_id, 'blog_cursos', 'CREATE', NEW.idcursos,
                json_build_object('nombre_curso', NEW.nombre_curso, 'fechainicial_curso', NEW.fechainicial_curso, 'fechafinal_curso', NEW.fechafinal_curso));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION log_cursos_update()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), NEW.creador_id, 'blog_cursos', 'UPDATE', NEW.idcursos,
                json_build_object('old_nombre', OLD.nombre_curso, 'new_nombre', NEW.nombre_curso));
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION log_cursos_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO blog_auditlog (timestamp, user_id, table_name, change_type, affected_record_id, modified_data)
        VALUES (NOW(), OLD.creador_id, 'blog_cursos', 'DELETE', OLD.idcursos,
                json_build_object('nombre_curso', OLD.nombre_curso));
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_log_cursos_insert AFTER INSERT ON blog_cursos FOR EACH ROW EXECUTE FUNCTION log_cursos_insert();
    CREATE TRIGGER trigger_log_cursos_update AFTER UPDATE ON blog_cursos FOR EACH ROW EXECUTE FUNCTION log_cursos_update();
    CREATE TRIGGER trigger_log_cursos_delete BEFORE DELETE ON blog_cursos FOR EACH ROW EXECUTE FUNCTION log_cursos_delete();
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print("✅ Todos los triggers restantes aplicados!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 COMPLETANDO SISTEMA DE AUDITORÍA")
    apply_remaining_triggers() 