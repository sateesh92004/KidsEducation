"""
Flask Web App - Kids Education Portal
Full-screen, mobile-responsive, deployable on Render/Railway free tier
"""

import os
import sys
import json
import queue
import threading
from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
from functools import wraps
from services.learning_agent import LearningAgent
from services.content_enricher import ContentEnricher
from services.auth_service import AuthService
from utils.grade_topics import GRADE_TOPICS

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['JSON_AS_ASCII'] = False

agent = LearningAgent()
enricher = ContentEnricher()
auth = AuthService()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated


# ===================== ROUTES =====================

@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    return render_template('dashboard.html', username=username, grades=['3', '4', '8'])


@app.route('/learn')
@login_required
def learn():
    grade = request.args.get('grade', '3')
    subject = request.args.get('subject', 'Science')
    username = session['username']
    topics = GRADE_TOPICS.get(grade, {}).get(subject, [])
    return render_template('learn.html', username=username, grade=grade, subject=subject, topics=topics)


# ===================== API ROUTES =====================

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Please fill all fields'})
    
    result = auth.login(username, password)
    if result['success'] and result['user']['role'] == 'student':
        session['username'] = username
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'message': result.get('message', 'Login failed')})


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Please fill all fields'})
    if len(password) < 4:
        return jsonify({'success': False, 'message': 'Password must be at least 4 characters'})
    
    # Check if user exists
    existing = auth.db_service.get_user_by_username(username)
    if existing:
        return jsonify({'success': False, 'message': 'Username already taken'})
    
    result = auth.register_student(username, password)
    if result['success']:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': result.get('message', 'Registration failed')})


@app.route('/api/logout')
def api_logout():
    session.clear()
    return jsonify({'success': True})


@app.route('/api/topics')
@login_required
def api_topics():
    grade = request.args.get('grade', '3')
    subject = request.args.get('subject', 'Science')
    topics = GRADE_TOPICS.get(grade, {}).get(subject, [])
    return jsonify({'topics': topics})


@app.route('/api/enrich')
@login_required
def api_enrich():
    topic = request.args.get('topic', '')
    grade = request.args.get('grade', '3')
    subject = request.args.get('subject', 'Science')
    
    if not topic:
        return jsonify({'has_rich_content': False})
    
    enriched = enricher.enrich_topic(topic, grade, subject)
    # Get images from DDG
    images = agent.get_topic_images(topic)
    
    result = {
        'has_rich_content': enriched.get('has_rich_content', False),
        'wikipedia_summary': enriched.get('source_summary', '')[:400] if enriched.get('has_rich_content') else '',
        'fun_facts': enriched.get('fun_facts', []),
        'images': images[:4],
        'related_topics': enriched.get('related_topics', []),
    }
    return jsonify(result)


@app.route('/api/quiz')
@login_required
def api_quiz():
    topic = request.args.get('topic', '')
    subject = request.args.get('subject', 'Science')
    questions = enricher.get_kids_quiz(topic, subject)
    return jsonify({'questions': questions[:3]})


@app.route('/api/learn/stream')
@login_required
def api_learn_stream():
    """SSE stream for LLM teaching"""
    grade = request.args.get('grade', '3')
    subject = request.args.get('subject', 'Science')
    topic = request.args.get('topic', '')
    mode = request.args.get('mode', 'initial')
    previous = request.args.get('previous', '')
    
    def generate():
        if mode == 'initial':
            stream = agent.teach_topic_stream(grade, subject, topic, topic)
        else:
            stream = agent.teach_more_stream(grade, subject, topic, previous)
        
        for chunk in stream:
            yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    print("🚀 Starting Kids Education Web App")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
