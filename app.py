from __future__ import annotations
import os, re, json, sqlite3, secrets
from pathlib import Path
from functools import wraps
from flask import Flask, request, jsonify, session, render_template, g
from werkzeug.security import generate_password_hash, check_password_hash

BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get('DOMUSOS_DB', BASE / 'instance' / 'domusos.sqlite3'))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
app.secret_key = os.environ.get('DOMUSOS_SECRET_KEY') or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', PERMANENT_SESSION_LIFETIME=60*60*24*14)

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
    return g.db

@app.teardown_appcontext
def close_db(_error=None):
    conn = g.pop('db', None)
    if conn is not None: conn.close()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE COLLATE NOCASE, password_hash TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS home_state (user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE, state_json TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()

def current_user():
    uid = session.get('user_id')
    if not uid: return None
    return db().execute('SELECT id,name,email FROM users WHERE id=?', (uid,)).fetchone()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user(): return jsonify(error='Please sign in to continue.'), 401
        return fn(*args, **kwargs)
    return wrapper

def user_json(row): return {'id': row['id'], 'name': row['name'], 'email': row['email']}

@app.get('/')
def index(): return render_template('index.html')

@app.get('/api/health')
def health(): return jsonify(status='ok', app='DomusOS', database='connected')

@app.post('/api/register')
def register():
    data=request.get_json(silent=True) or {}
    name=str(data.get('name','')).strip(); email=str(data.get('email','')).strip().lower(); password=str(data.get('password',''))
    if len(name)<2: return jsonify(error='Name must contain at least 2 characters.'),400
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email): return jsonify(error='Enter a valid email address.'),400
    if len(password)<8: return jsonify(error='Password must contain at least 8 characters.'),400
    try:
        cur=db().execute('INSERT INTO users(name,email,password_hash) VALUES(?,?,?)',(name,email,generate_password_hash(password)))
        db().commit(); session.clear(); session['user_id']=cur.lastrowid; session.permanent=True
        row=db().execute('SELECT id,name,email FROM users WHERE id=?',(cur.lastrowid,)).fetchone()
        return jsonify(user=user_json(row)),201
    except sqlite3.IntegrityError: return jsonify(error='An account with this email already exists. Please sign in.'),409

@app.post('/api/login')
def login():
    data=request.get_json(silent=True) or {}; email=str(data.get('email','')).strip().lower(); password=str(data.get('password',''))
    row=db().execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
    if not row or not check_password_hash(row['password_hash'],password): return jsonify(error='The email or password is incorrect.'),401
    session.clear(); session['user_id']=row['id']; session.permanent=bool(data.get('remember'))
    return jsonify(user=user_json(row))

@app.get('/api/me')
def me():
    row=current_user(); return jsonify(user=user_json(row) if row else None)

@app.post('/api/logout')
def logout(): session.clear(); return jsonify(ok=True)

@app.get('/api/state')
@login_required
def get_state():
    row=db().execute('SELECT state_json,updated_at FROM home_state WHERE user_id=?',(session['user_id'],)).fetchone()
    return jsonify(state=json.loads(row['state_json']) if row else None, updated_at=row['updated_at'] if row else None)

@app.put('/api/state')
@login_required
def put_state():
    data=request.get_json(silent=True) or {}; state=data.get('state')
    if not isinstance(state,dict): return jsonify(error='State must be a JSON object.'),400
    encoded=json.dumps(state,separators=(',',':'))
    if len(encoded)>200_000: return jsonify(error='State payload is too large.'),413
    db().execute('''INSERT INTO home_state(user_id,state_json) VALUES(?,?) ON CONFLICT(user_id) DO UPDATE SET state_json=excluded.state_json, updated_at=CURRENT_TIMESTAMP''',(session['user_id'],encoded))
    db().commit(); return jsonify(ok=True)

@app.errorhandler(404)
def not_found(_): return jsonify(error='Not found'),404

if __name__ == '__main__':
    init_db()
    print('DomusOS backend running at http://127.0.0.1:8767')
    app.run(host='127.0.0.1',port=8767,debug=False)
