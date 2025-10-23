"""
Migración para agregar columna numero_ticket a la tabla tickets.
"""
import sqlite3

def run_migration():
    conn = sqlite3.connect("parqueadero.db")
    c = conn.cursor()
    
    # Verificar si la columna ya existe
    c.execute("PRAGMA table_info(tickets)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'numero_ticket' not in columns:
        print("Agregando columna numero_ticket a la tabla tickets...")
        
        # Agregar la columna
        c.execute("ALTER TABLE tickets ADD COLUMN numero_ticket INTEGER")
        
        # Asignar números correlativos a tickets existentes
        c.execute("SELECT id FROM tickets ORDER BY hora_entrada")
        tickets = c.fetchall()
        
        for idx, (ticket_id,) in enumerate(tickets, start=1):
            c.execute("UPDATE tickets SET numero_ticket = ? WHERE id = ?", (idx, ticket_id))
        
        conn.commit()
        print(f"✓ Migración completada. Se actualizaron {len(tickets)} tickets.")
    else:
        print("La columna numero_ticket ya existe. No se requiere migración.")
    
    conn.close()

if __name__ == "__main__":
    run_migration()
