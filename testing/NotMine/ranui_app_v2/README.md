# Ranui Family Clothing Allowance App

A Python Tkinter GUI application using **OOP** and **SQLite** to manage annual clothing allowances for Nikau, Hana, and Tia.

---

## How to Run

```bash
python main.py
```

Or double-click `run.bat` (Windows) / `run.sh` (Mac/Linux).

---

## Requirements

- Python 3.10+
- Tkinter (included with standard Python)
- sqlite3 (included with standard Python)
- **No extra pip installs needed**

---

## Project Structure

```
ranui_app_v2/
├── main.py         ← GUI + App controller
├── models.py       ← OOP: Child and Family classes
├── database.py     ← SQLite persistence layer
├── data/
│   └── ranui.db    ← Auto-created SQLite database
├── run.bat         ← Windows launcher
├── run.sh          ← Mac/Linux launcher
└── README.md       ← This file
```

---

## OOP Design

| Class    | Attributes                           | Key Methods                    |
|----------|--------------------------------------|--------------------------------|
| `Child`  | `name`, `balance`, `on_target_for_bonus` | `spend(amount)`, `reset()`  |
| `Family` | `name`, `children[]`                 | `add_child()`, `get_child()`, `bonus_eligible()`, `reset_all()` |

---

## Database Schema

### `children` table
| Column  | Type | Description            |
|---------|------|------------------------|
| id      | INT  | Primary key            |
| name    | TEXT | Child's name           |
| balance | REAL | Current balance ($)    |

### `transactions` table
| Column      | Type | Description               |
|-------------|------|---------------------------|
| id          | INT  | Primary key               |
| child_name  | TEXT | Who spent the money       |
| amount      | REAL | Amount spent ($)          |
| description | TEXT | Optional item description |
| timestamp   | TEXT | Date and time of purchase |

---

## Business Rules

| Rule | Detail |
|------|--------|
| Annual allowance | $300 per child |
| Overspending | Blocked — purchase declined |
| Bonus threshold | More than $50 remaining at year end |
| Bonus | Child chooses an activity of their choice |
