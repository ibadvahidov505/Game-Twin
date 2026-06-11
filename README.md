# Gaming Digital Twin

## How to Run

### 1. Start Backend (Flask)

```bash
cd backend
pip install flask flask-cors
python app.py
```

Server runs on http://127.0.0.1:5000

### 2. Start Frontend

**DO NOT open `frontend/index.html` by double-clicking** (`file://`). Browsers block fetch from `file://` to `http://`.

Instead, serve it with any HTTP server:

**Option A — Python (no install needed):**
```bash
cd frontend
python -m http.server 5500
```
Then open http://localhost:5500

**Option B — VS Code Live Server:**
Right-click `index.html` → Open with Live Server

**Option C — Node.js http-server:**
```bash
npx http-server frontend -p 5500
```

### 3. Use the App

- Enter a Steam username: `player1`, `player2`, or `player3`
- Click "Analyze Player"
- Backend returns mock Steam profile + archetype analysis

### Mock Users

| Username   | Hours | Games | Favorite Game    |
|------------|-------|-------|------------------|
| player1    | 620   | 45    | The Witcher 3    |
| player2    | 180   | 12    | Counter-Strike 2 |
| player3    | 1500  | 89    | Dota 2           |
