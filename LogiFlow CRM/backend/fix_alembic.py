import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('logiflow.db')
cur = conn.cursor()

# Verificar versão atual
cur.execute('SELECT version_num FROM alembic_version')
current = cur.fetchone()
print(f'Versão atual: {current[0] if current else "Nenhuma"}')

# Atualizar para a última versão conhecida antes da Enterprise
cur.execute('UPDATE alembic_version SET version_num = ?', ('005_create_gps',))
conn.commit()

# Verificar nova versão
cur.execute('SELECT version_num FROM alembic_version')
new_version = cur.fetchone()
print(f'Nova versão: {new_version[0]}')

conn.close()
print('\n✅ Banco de dados corrigido! Execute: alembic upgrade head')
