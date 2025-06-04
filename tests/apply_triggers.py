import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def apply_conference_triggers():
    """Aplica solo los triggers de conferencias para probar."""
    
    sql_script = """
    -- Eliminar triggers existentes de conferencias
    DROP TRIGGER IF EXISTS trigger_log_conferencias_insert ON blog_conferencias;
    DROP TRIGGER IF EXISTS trigger_log_conferencias_update ON blog_conferencias;
    DROP TRIGGER IF EXISTS trigger_log_conferencias_delete ON blog_conferencias;
    
    -- Eliminar funciones existentes
    DROP FUNCTION IF EXISTS log_conferencias_insert();
    DROP FUNCTION IF EXISTS log_conferencias_update();
    DROP FUNCTION IF EXISTS log_conferencias_delete();

    -- Crear función INSERT corregida
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
                'imagen_conferencia', NEW.imagen_conferencia,
                'link_conferencia', NEW.link_conferencia
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear función UPDATE
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
                'new_ponente_conferencia', NEW.ponente_conferencia
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear función DELETE
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
                'ponente_conferencia', OLD.ponente_conferencia
            )
        );
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear los triggers
    CREATE TRIGGER trigger_log_conferencias_insert
        AFTER INSERT ON blog_conferencias
        FOR EACH ROW EXECUTE FUNCTION log_conferencias_insert();

    CREATE TRIGGER trigger_log_conferencias_update
        AFTER UPDATE ON blog_conferencias
        FOR EACH ROW EXECUTE FUNCTION log_conferencias_update();

    CREATE TRIGGER trigger_log_conferencias_delete
        BEFORE DELETE ON blog_conferencias
        FOR EACH ROW EXECUTE FUNCTION log_conferencias_delete();
    """
    
    print("Aplicando triggers de conferencias...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        
        print("✅ Triggers de conferencias aplicados!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 APLICANDO TRIGGERS DE CONFERENCIAS")
    apply_conference_triggers() 