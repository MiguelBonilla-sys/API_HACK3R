import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def apply_ofertas_empleo_triggers():
    """Aplica triggers para la tabla blog_ofertasempleo."""
    sql_script = """
    -- OFERTAS DE EMPLEO
    DROP TRIGGER IF EXISTS trigger_log_ofertasempleo_insert ON blog_ofertasempleo;
    DROP TRIGGER IF EXISTS trigger_log_ofertasempleo_update ON blog_ofertasempleo;
    DROP TRIGGER IF EXISTS trigger_log_ofertasempleo_delete ON blog_ofertasempleo;
    DROP FUNCTION IF EXISTS log_ofertasempleo_insert() CASCADE;
    DROP FUNCTION IF EXISTS log_ofertasempleo_update() CASCADE;
    DROP FUNCTION IF EXISTS log_ofertasempleo_delete() CASCADE;

    -- Función INSERT para ofertas de empleo
    CREATE OR REPLACE FUNCTION log_ofertasempleo_insert()
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
            'blog_ofertasempleo', 
            'CREATE',
            NEW.idoferta,
            json_build_object(
                'titulo_empleo', NEW.titulo_empleo,
                'empresa', NEW.empresa,
                'fecha_publicacion', NEW.fecha_publicacion,
                'descripcion_empleo', NEW.descripcion_empleo,
                'imagen', NEW.imagen,
                'link_oferta', NEW.link_oferta,
                'fecha_expiracion', NEW.fecha_expiracion
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función UPDATE para ofertas de empleo
    CREATE OR REPLACE FUNCTION log_ofertasempleo_update()
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
            'blog_ofertasempleo', 
            'UPDATE',
            NEW.idoferta,
            json_build_object(
                'old_titulo_empleo', OLD.titulo_empleo,
                'new_titulo_empleo', NEW.titulo_empleo,
                'old_empresa', OLD.empresa,
                'new_empresa', NEW.empresa,
                'old_descripcion_empleo', OLD.descripcion_empleo,
                'new_descripcion_empleo', NEW.descripcion_empleo,
                'old_fecha_expiracion', OLD.fecha_expiracion,
                'new_fecha_expiracion', NEW.fecha_expiracion
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función DELETE para ofertas de empleo
    CREATE OR REPLACE FUNCTION log_ofertasempleo_delete()
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
            'blog_ofertasempleo', 
            'DELETE',
            OLD.idoferta,
            json_build_object(
                'titulo_empleo', OLD.titulo_empleo,
                'empresa', OLD.empresa,
                'fecha_publicacion', OLD.fecha_publicacion,
                'fecha_expiracion', OLD.fecha_expiracion
            )
        );
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear triggers para ofertas de empleo
    CREATE TRIGGER trigger_log_ofertasempleo_insert
        AFTER INSERT ON blog_ofertasempleo
        FOR EACH ROW EXECUTE FUNCTION log_ofertasempleo_insert();

    CREATE TRIGGER trigger_log_ofertasempleo_update
        AFTER UPDATE ON blog_ofertasempleo
        FOR EACH ROW EXECUTE FUNCTION log_ofertasempleo_update();

    CREATE TRIGGER trigger_log_ofertasempleo_delete
        BEFORE DELETE ON blog_ofertasempleo
        FOR EACH ROW EXECUTE FUNCTION log_ofertasempleo_delete();
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        print("✅ Triggers de ofertas de empleo aplicados!")
        return True
    except Exception as e:
        print(f"❌ Error en ofertas de empleo: {e}")
        return False

def apply_proyectos_triggers():
    """Aplica triggers para la tabla blog_proyectos."""
    sql_script = """
    -- PROYECTOS
    DROP TRIGGER IF EXISTS trigger_log_proyectos_insert ON blog_proyectos;
    DROP TRIGGER IF EXISTS trigger_log_proyectos_update ON blog_proyectos;
    DROP TRIGGER IF EXISTS trigger_log_proyectos_delete ON blog_proyectos;
    DROP FUNCTION IF EXISTS log_proyectos_insert() CASCADE;
    DROP FUNCTION IF EXISTS log_proyectos_update() CASCADE;
    DROP FUNCTION IF EXISTS log_proyectos_delete() CASCADE;

    -- Función INSERT para proyectos
    CREATE OR REPLACE FUNCTION log_proyectos_insert()
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
            'blog_proyectos', 
            'CREATE',
            NEW.idproyectos,
            json_build_object(
                'nombre_proyecto', NEW.nombre_proyecto,
                'fecha_proyecto', NEW.fecha_proyecto,
                'link_proyecto', NEW.link_proyecto,
                'description_proyecto', NEW.description_proyecto
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función UPDATE para proyectos
    CREATE OR REPLACE FUNCTION log_proyectos_update()
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
            'blog_proyectos', 
            'UPDATE',
            NEW.idproyectos,
            json_build_object(
                'old_nombre_proyecto', OLD.nombre_proyecto,
                'new_nombre_proyecto', NEW.nombre_proyecto,
                'old_fecha_proyecto', OLD.fecha_proyecto,
                'new_fecha_proyecto', NEW.fecha_proyecto,
                'old_link_proyecto', OLD.link_proyecto,
                'new_link_proyecto', NEW.link_proyecto,
                'old_description_proyecto', OLD.description_proyecto,
                'new_description_proyecto', NEW.description_proyecto
            )
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Función DELETE para proyectos
    CREATE OR REPLACE FUNCTION log_proyectos_delete()
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
            'blog_proyectos', 
            'DELETE',
            OLD.idproyectos,
            json_build_object(
                'nombre_proyecto', OLD.nombre_proyecto,
                'fecha_proyecto', OLD.fecha_proyecto,
                'link_proyecto', OLD.link_proyecto
            )
        );
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Crear triggers para proyectos
    CREATE TRIGGER trigger_log_proyectos_insert
        AFTER INSERT ON blog_proyectos
        FOR EACH ROW EXECUTE FUNCTION log_proyectos_insert();

    CREATE TRIGGER trigger_log_proyectos_update
        AFTER UPDATE ON blog_proyectos
        FOR EACH ROW EXECUTE FUNCTION log_proyectos_update();

    CREATE TRIGGER trigger_log_proyectos_delete
        BEFORE DELETE ON blog_proyectos
        FOR EACH ROW EXECUTE FUNCTION log_proyectos_delete();
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        print("✅ Triggers de proyectos aplicados!")
        return True
    except Exception as e:
        print(f"❌ Error en proyectos: {e}")
        return False

def verify_all_tables():
    """Verifica el estado completo de todos los triggers."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                event_object_table,
                COUNT(*) as trigger_count
            FROM information_schema.triggers 
            WHERE trigger_schema = 'public' 
                AND trigger_name LIKE 'trigger_log_%'
            GROUP BY event_object_table
            ORDER BY event_object_table;
        """)
        
        results = cursor.fetchall()
        
        print("\n📊 ESTADO COMPLETO DE TRIGGERS:")
        expected_tables = [
            'blog_conferencias',
            'blog_integrantes', 
            'blog_noticias',
            'blog_cursos',
            'blog_ofertasempleo',
            'blog_proyectos'
        ]
        
        found_tables = {table: count for table, count in results}
        total_triggers = 0
        
        for table in expected_tables:
            if table in found_tables:
                count = found_tables[table]
                status = "✅ COMPLETO" if count == 3 else f"⚠️  PARCIAL ({count}/3)"
                print(f"   🏷️  {table}: {status}")
                total_triggers += count
            else:
                print(f"   🏷️  {table}: ❌ SIN TRIGGERS")
        
        print(f"\n📈 TOTAL: {total_triggers}/18 triggers")
        coverage = (total_triggers / 18) * 100
        print(f"📊 COBERTURA: {coverage:.1f}%")
        
        return total_triggers

if __name__ == "__main__":
    print("🔧 COMPLETANDO TRIGGERS FALTANTES")
    print("=" * 50)
    
    success_count = 0
    
    print("📋 Aplicando triggers de ofertas de empleo...")
    if apply_ofertas_empleo_triggers():
        success_count += 1
    
    print("📋 Aplicando triggers de proyectos...")
    if apply_proyectos_triggers():
        success_count += 1
    
    print(f"\n✅ {success_count}/2 grupos de triggers aplicados")
    
    total = verify_all_tables()
    
    if total >= 18:
        print("\n🎉 ¡SISTEMA DE AUDITORÍA 100% COMPLETO!")
        print("📋 Todas las 6 tablas principales tienen auditoría completa")
    else:
        print(f"\n⚠️  Sistema con {total}/18 triggers instalados") 