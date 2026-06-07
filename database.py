import sqlite3
import os
import shutil

BASE_DIR = os.path.dirname(__file__)
LOCAL_DB = os.path.join(BASE_DIR, 'database.db')

# Na Vercel o filesystem é efêmero; usamos /tmp e copiamos o banco inicial.
if os.environ.get('VERCEL'):
    DATABASE_PATH = '/tmp/database.db'
    if not os.path.exists(DATABASE_PATH) and os.path.exists(LOCAL_DB):
        shutil.copy2(LOCAL_DB, DATABASE_PATH)
else:
    DATABASE_PATH = LOCAL_DB

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela de vídeos de estudo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            category TEXT NOT NULL,
            watched INTEGER DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de tópicos da EFOMM
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS efomm_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            status TEXT DEFAULT 'not_started',
            notes TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de vídeos para os tópicos da EFOMM
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS efomm_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY(topic_id) REFERENCES efomm_topics(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela de configurações (data da prova, nome do usuário)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Inserir configurações padrão se não existirem
    cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', ('user_name', 'Rafael'))
    # Set default exam date to August 15, 2026 (EFOMM exams are usually in August)
    cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', ('exam_date', '2026-08-15'))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")
