from flask import Flask, render_template, request, jsonify, g
import sqlite3
import os
from database import get_db_connection, init_db

app = Flask(__name__)

# Garantir que o banco de dados está inicializado ao rodar o app
with app.app_context():
    init_db()

# Context processor para injetar variáveis globais em todos os templates
@app.context_processor
def inject_global_settings():
    db = get_db_connection()
    cursor = db.cursor()
    
    # Obter nome do usuário
    cursor.execute("SELECT value FROM settings WHERE key = 'user_name'")
    row_user = cursor.fetchone()
    user_name = row_user['value'] if row_user else 'Rafael'
    
    # Obter data da prova
    cursor.execute("SELECT value FROM settings WHERE key = 'exam_date'")
    row_date = cursor.fetchone()
    exam_date = row_date['value'] if row_date else '2026-08-15'
    
    db.close()
    return dict(user_name=user_name, exam_date=exam_date)

# ==========================================
# ROTAS PRINCIPAIS DE PÁGINAS (HTML)
# ==========================================

@app.route('/')
def dashboard():
    db = get_db_connection()
    cursor = db.cursor()
    
    # 1. Estatísticas de Vídeos
    cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN watched = 1 THEN 1 ELSE 0 END) as watched FROM study_videos")
    row_videos = cursor.fetchone()
    total_videos = row_videos['total'] or 0
    watched_videos = row_videos['watched'] or 0
    watched_pct = round((watched_videos / total_videos) * 100) if total_videos > 0 else 0
    
    video_stats = {
        'total': total_videos,
        'watched': watched_videos,
        'watched_pct': watched_pct
    }
    
    # 2. Vídeos Recentes Pendentes (limite 3)
    cursor.execute("SELECT * FROM study_videos WHERE watched = 0 ORDER BY id DESC LIMIT 3")
    pending_rows = cursor.fetchall()
    pending_videos = [dict(row) for row in pending_rows]
    
    # 3. Estatísticas de Tópicos da EFOMM
    cursor.execute("SELECT subject, status, COUNT(*) as count FROM efomm_topics GROUP BY subject, status")
    rows_efomm = cursor.fetchall()
    
    # Agrupar dados por disciplina
    # Disciplinas padrão no banco: Matemática, Física, Português, Inglês
    subjects = ['Matemática', 'Física', 'Português', 'Inglês']
    subject_stats = {sub: {'total': 0, 'completed': 0} for sub in subjects}
    
    overall_total = 0
    overall_completed = 0
    
    for row in rows_efomm:
        sub = row['subject']
        status = row['status']
        count = row['count']
        
        if sub in subject_stats:
            subject_stats[sub]['total'] += count
            overall_total += count
            if status == 'completed':
                subject_stats[sub]['completed'] += count
                overall_completed += count
                
    # Calcular percentuais
    subjects_pct = {}
    for sub in subjects:
        total = subject_stats[sub]['total']
        completed = subject_stats[sub]['completed']
        subjects_pct[sub] = round((completed / total) * 100) if total > 0 else 0
        
    overall_pct = round((overall_completed / overall_total) * 100) if overall_total > 0 else 0
    
    efomm_progress = {
        'overall_pct': overall_pct,
        'subjects': subjects_pct
    }
    
    db.close()
    
    return render_template(
        'dashboard.html', 
        active_page='dashboard',
        video_stats=video_stats,
        pending_videos=pending_videos,
        efomm_progress=efomm_progress
    )

@app.route('/videos')
def videos():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM study_videos ORDER BY id DESC")
    rows = cursor.fetchall()
    video_list = [dict(row) for row in rows]
    db.close()
    
    return render_template('videos.html', active_page='videos', videos=video_list)

@app.route('/efomm')
def efomm():
    return render_template('efomm.html', active_page='efomm')

# ==========================================
# ROTAS DE API (REST JSON)
# ==========================================

@app.route('/api/efomm/list', methods=['GET'])
def api_efomm_list():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Obter todos os tópicos
        cursor.execute("SELECT * FROM efomm_topics ORDER BY id ASC")
        rows_topics = cursor.fetchall()
        topics = [dict(row) for row in rows_topics]
        
        # Obter todos os vídeos dos tópicos da EFOMM
        cursor.execute("SELECT * FROM efomm_videos ORDER BY id ASC")
        rows_videos = cursor.fetchall()
        videos = [dict(row) for row in rows_videos]
        
        db.close()
        
        # Agrupar vídeos por topic_id
        videos_by_topic = {}
        for video in videos:
            t_id = video['topic_id']
            if t_id not in videos_by_topic:
                videos_by_topic[t_id] = []
            videos_by_topic[t_id].append(video)
            
        # Acoplar os vídeos a cada respectivo tópico
        for topic in topics:
            topic['videos'] = videos_by_topic.get(topic['id'], [])
            
        return jsonify({'success': True, 'topics': topics})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/efomm/update/<int:topic_id>', methods=['POST'])
def api_efomm_update(topic_id):
    try:
        data = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()
        
        # Montar a query dinamicamente baseada no que foi passado
        fields = []
        values = []
        
        if 'status' in data:
            fields.append("status = ?")
            values.append(data['status'])
        if 'notes' in data:
            fields.append("notes = ?")
            values.append(data['notes'])
            
        if not fields:
            return jsonify({'success': False, 'message': 'Nenhum campo fornecido para atualização.'}), 400
            
        values.append(topic_id)
        query = f"UPDATE efomm_topics SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        
        cursor.execute(query, tuple(values))
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/videos/add', methods=['POST'])
def api_videos_add():
    try:
        data = request.get_json()
        title = data.get('title')
        url = data.get('url')
        category = data.get('category')
        notes = data.get('notes', '')
        
        if not title or not url or not category:
            return jsonify({'success': False, 'message': 'Título, Link e Categoria são obrigatórios.'}), 400
            
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO study_videos (title, url, category, notes, watched) VALUES (?, ?, ?, ?, 0)",
            (title, url, category, notes)
        )
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/videos/toggle/<int:video_id>', methods=['POST'])
def api_videos_toggle(video_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Obter estado atual
        cursor.execute("SELECT watched FROM study_videos WHERE id = ?", (video_id,))
        row = cursor.fetchone()
        if not row:
            db.close()
            return jsonify({'success': False, 'message': 'Vídeo não encontrado.'}), 404
            
        new_status = 1 - row['watched']
        cursor.execute("UPDATE study_videos SET watched = ? WHERE id = ?", (new_status, video_id))
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/videos/delete/<int:video_id>', methods=['DELETE'])
def api_videos_delete(video_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM study_videos WHERE id = ?", (video_id,))
        db.commit()
        db.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/settings/update', methods=['POST'])
def api_settings_update():
    try:
        data = request.get_json()
        user_name = data.get('user_name')
        exam_date = data.get('exam_date')
        
        db = get_db_connection()
        cursor = db.cursor()
        
        if user_name:
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('user_name', ?)", (user_name,))
        if exam_date:
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('exam_date', ?)", (exam_date,))
            
        db.commit()
        db.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Usar porta padrão do Flask
    app.run(debug=True, port=5000)
