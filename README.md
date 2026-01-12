# Inventory-Management-System-v0.2.0
Inventory Management System V0.2.0
Inventory Management (Tkinter + MySQL) v0.2.0

Quick setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure MySQL server is running locally and adjust credentials using environment variables if needed:

- `DB_HOST` (default: `localhost`)
- `DB_USER` (default: `root`)
- `DB_PASSWORD` (default: `root`)

4. Run the dashboard:

```bash
python dashboard.py
```

Notes

- The app will create a `invetory_system` database automatically if it does not exist.
- Logs are written to `app.log` in the project directory.
- For production use, secure DB credentials and use migrations instead of inline `CREATE TABLE` statements.
