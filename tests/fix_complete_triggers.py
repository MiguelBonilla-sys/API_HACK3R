import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def apply_remaining_triggers_fixed():
    # Script SQL corregido con CASCADE
    sql = """
    -- LIMPIAR TRIGGERS Y FUNCIONES EXISTENTES CON CASCADE
    DROP FUNCTION IF EXISTS log_integrantes_insert() CASCADE;
    DROP FUNCTION IF EXISTS log_integrantes_update() CASCADE;
    DROP FUNCTION IF EXISTS log_integrantes_delete() CASCADE;
    DROP FUNCTION IF EXISTS log_noticias_insert() CASCADE;
    DROP FUNCTION IF EXISTS log_noticias_update() CASCADE;
    DROP FUNCTION IF EXISTS log_noticias_delete() CASCADE;
    DROP FUNCTION IF EXISTS log_cursos_insert() CASCADE;
    DROP FUNCTION IF EXISTS log_cursos_update() CASCADE;
    DROP FUNCTION IF EXISTS log_cursos_delete() CASCADE;

    -- INTEGRANTES
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
        print("✅ Todos los triggers restantes aplicados correctamente!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 COMPLETANDO SISTEMA DE AUDITORÍA (VERSIÓN CORREGIDA)")
    apply_remaining_triggers_fixed() 