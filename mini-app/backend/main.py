# 🤖 IA Clicker Empire - Backend API
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import sqlite3
import hashlib
import json
from datetime import datetime, timedelta

app = FastAPI(title="IA Clicker Empire API")

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos ---

class Player(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    coins: int = 100
    gems: int = 10
    level: int = 1
    xp: int = 0
    coins_per_second: int = 0
    last_login: Optional[str] = None

class TapRequest(BaseModel):
    telegram_id: int
    taps: int = 1

class UpgradeRequest(BaseModel):
    telegram_id: int
    upgrade_type: str

class TriviaAnswer(BaseModel):
    telegram_id: int
    question_id: int
    answer: int

# --- Database ---

def get_db():
    conn = sqlite3.connect('ia_clicker.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            coins INTEGER DEFAULT 100,
            gems INTEGER DEFAULT 10,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            coins_per_second INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 100,
            max_energy INTEGER DEFAULT 100,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            upgrades TEXT DEFAULT '{}',
            achievements TEXT DEFAULT '[]'
        )
    ''')
    
    # Trivia table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trivia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            options TEXT,
            correct_answer INTEGER,
            difficulty TEXT DEFAULT 'medium',
            reward INTEGER DEFAULT 100
        )
    ''')
    
    # Leaderboard table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            telegram_id INTEGER,
            score INTEGER DEFAULT 0,
            week INTEGER,
            year INTEGER,
            PRIMARY KEY (telegram_id, week, year)
        )
    ''')
    
    # Insert some trivia questions
    cursor.execute('''
        INSERT OR IGNORE INTO trivia (question, options, correct_answer, reward)
        VALUES 
            ('¿Qué significa IA?', '["Inteligencia Artificial", "Informática Avanzada", "Internet Automático", "Interfaz Activa"]', 0, 100),
            ('¿Quién es el padre de la IA?', '["Alan Turing", "Elon Musk", "Bill Gates", "Mark Zuckerberg"]', 0, 150),
            ('¿Qué es el Machine Learning?', '["Aprendizaje automático", "Máquina de escribir", "Aprendizaje manual", "Máquina inteligente"]', 0, 150),
            ('¿Qué empresa creó ChatGPT?', '["OpenAI", "Google", "Microsoft", "Meta"]', 0, 200),
            ('¿Qué es una red neuronal?', '["Modelo de IA inspirado en el cerebro", "Red de computadoras", "Red social", "Red de datos"]', 0, 200)
    ''')
    
    conn.commit()
    conn.close()

# --- Helpers ---

def get_or_create_player(telegram_id: int, username: Optional[str] = None) -> Player:
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM players WHERE telegram_id = ?', (telegram_id,))
    row = cursor.fetchone()
    
    if not row:
        # Create new player
        cursor.execute('''
            INSERT INTO players (telegram_id, username, last_login)
            VALUES (?, ?, ?)
        ''', (telegram_id, username, datetime.now().isoformat()))
        conn.commit()
        
        player = Player(telegram_id=telegram_id, username=username)
    else:
        player = Player(**dict(row))
        
        # Update username if changed
        if username and username != row['username']:
            cursor.execute('UPDATE players SET username = ? WHERE telegram_id = ?', (username, telegram_id))
            conn.commit()
    
    conn.close()
    return player

def calculate_passive_income(player: Player) -> int:
    # Calculate coins earned since last login
    if not player.last_login:
        return 0
    
    last_login = datetime.fromisoformat(player.last_login)
    hours_passed = (datetime.now() - last_login).total_seconds() / 3600
    
    return int(hours_passed * player.coins_per_second * 3600)

# --- Endpoints ---

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "IA Clicker Empire API", "status": "running"}

@app.post("/api/player/init")
async def init_player(
    telegram_id: int,
    username: Optional[str] = None,
    x_telegram_init_data: Optional[str] = Header(None)
):
    """Initialize or get player data"""
    player = get_or_create_player(telegram_id, username)
    
    # Calculate passive income
    passive_coins = calculate_passive_income(player)
    
    if passive_coins > 0:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE players 
            SET coins = coins + ?, last_login = ?
            WHERE telegram_id = ?
        ''', (passive_coins, datetime.now().isoformat(), telegram_id))
        conn.commit()
        conn.close()
    
    return {
        "player": get_or_create_player(telegram_id, username),
        "passive_coins": passive_coins
    }

@app.post("/api/player/tap")
async def player_tap(request: TapRequest):
    """Register taps from player"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get player energy
    cursor.execute('SELECT energy, max_energy, coins FROM players WHERE telegram_id = ?', 
                   (request.telegram_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Player not found")
    
    energy, max_energy, coins = row
    valid_taps = min(request.taps, energy)
    
    if valid_taps <= 0:
        raise HTTPException(status_code=400, detail="No energy")
    
    # Update player
    coins_earned = valid_taps  # 1 coin per tap base
    cursor.execute('''
        UPDATE players 
        SET coins = coins + ?, 
            energy = energy - ?,
            xp = xp + ?,
            last_login = ?
        WHERE telegram_id = ?
    ''', (coins_earned, valid_taps, valid_taps, datetime.now().isoformat(), request.telegram_id))
    
    conn.commit()
    conn.close()
    
    return {
        "coins_earned": coins_earned,
        "energy_used": valid_taps,
        "xp_gained": valid_taps
    }

@app.post("/api/player/upgrade")
async def buy_upgrade(request: UpgradeRequest):
    """Buy an upgrade"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get player and upgrades
    cursor.execute('SELECT coins, upgrades FROM players WHERE telegram_id = ?', 
                   (request.telegram_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Player not found")
    
    coins, upgrades_json = row
    upgrades = json.loads(upgrades_json) if upgrades_json else {}
    
    # Upgrade definitions
    UPGRADES = {
        'gpu': {'base_cost': 50, 'cps_bonus': 1},
        'model': {'base_cost': 100, 'cps_bonus': 2},
        'datacenter': {'base_cost': 500, 'cps_bonus': 10},
    }
    
    if request.upgrade_type not in UPGRADES:
        raise HTTPException(status_code=400, detail="Invalid upgrade")
    
    upgrade_info = UPGRADES[request.upgrade_type]
    level = upgrades.get(request.upgrade_type, {}).get('level', 0)
    cost = int(upgrade_info['base_cost'] * (1.5 ** level))
    
    if coins < cost:
        raise HTTPException(status_code=400, detail="Not enough coins")
    
    # Update player
    upgrades[request.upgrade_type] = {
        'level': level + 1,
        'cost': int(upgrade_info['base_cost'] * (1.5 ** (level + 1)))
    }
    
    cursor.execute('''
        UPDATE players 
        SET coins = coins - ?,
            coins_per_second = coins_per_second + ?,
            upgrades = ?
        WHERE telegram_id = ?
    ''', (cost, upgrade_info['cps_bonus'], json.dumps(upgrades), request.telegram_id))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "new_level": level + 1,
        "cps_bonus": upgrade_info['cps_bonus']
    }

@app.get("/api/trivia/daily")
async def get_daily_trivia():
    """Get daily trivia questions"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, question, options, difficulty, reward FROM trivia ORDER BY RANDOM() LIMIT 5')
    questions = []
    
    for row in cursor.fetchall():
        questions.append({
            'id': row['id'],
            'question': row['question'],
            'options': json.loads(row['options']),
            'difficulty': row['difficulty'],
            'reward': row['reward']
        })
    
    conn.close()
    
    return {"questions": questions}

@app.post("/api/trivia/answer")
async def submit_trivia_answer(request: TriviaAnswer):
    """Submit trivia answer"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get question
    cursor.execute('SELECT correct_answer, reward FROM trivia WHERE id = ?', 
                   (request.question_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Question not found")
    
    correct_answer, reward = row
    is_correct = request.answer == correct_answer
    
    if is_correct:
        # Update player coins
        cursor.execute('''
            UPDATE players 
            SET coins = coins + ?, xp = xp + ?
            WHERE telegram_id = ?
        ''', (reward, reward // 2, request.telegram_id))
        conn.commit()
    
    conn.close()
    
    return {
        "correct": is_correct,
        "reward": reward if is_correct else 0,
        "correct_answer": correct_answer if not is_correct else None
    }

@app.get("/api/leaderboard")
async def get_leaderboard():
    """Get global leaderboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT telegram_id, username, coins, level 
        FROM players 
        ORDER BY coins DESC 
        LIMIT 100
    ''')
    
    leaderboard = []
    for i, row in enumerate(cursor.fetchall(), 1):
        leaderboard.append({
            'rank': i,
            'telegram_id': row['telegram_id'],
            'username': row['username'],
            'coins': row['coins'],
            'level': row['level']
        })
    
    conn.close()
    
    return {"leaderboard": leaderboard}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
