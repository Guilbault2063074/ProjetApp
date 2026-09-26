## Nom et code permanent
William Guilbault
GUIW19080300

# ☕ Coffee Loyalty Management System - Setup Guide

This repository contains a lightweight Point of Sale (POS) barista dashboard and client registry built using **Django 6.x** and **SQLite**. 

---

## 💻 System Prerequisites

* **Operating System:** Windows 10 / 11, macOS, or Linux
* **Python Engine:** Version 3.12 or higher
* **Package Architecture Tool:** `astral-uv`

---

## 🚀 How to Run the Project (Quick Start)

To compile your environment variables, apply database migrations, and boot the testing server without triggering platform-specific activation flags, open your terminal in the project root directory and execute:

```powershell
# 1. Generate internal database schemas and structural tables
uv run --directory src python manage.py migrate

# 2. Boot the application engine development port
uv run --directory src python manage.py runserver
```

## If the above does not work try this:

go directly into src and type: 

uv run python manage.py migrate
uv run python manage.py runserver


### 🔑 Local Access & Grading Credentials

* **☕ Barista Station Dashboard:** [http://127.0.0.1:8000/]
* **⚙️ Management Console Access:** [http://127.0.0.1:8000/admin/]
* **Administrator Username:** `admin`
* **Administrator Password:** `1234`

---

## 📂 Project Directory Structure Mapping

As per assignment submission blueprints, our directory trees align as follows:
* `README.md` → Environment boot operations (This file).
* `AI-USAGE.md` → Academic AI disclosure statement layout.
* `docs/` → Project documentation.
* `src/` → Application codebase assets (`manage.py`, project configuration, apps).
