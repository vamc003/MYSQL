# MySQL Database Source Repository

## Overview

This repository is used to extract, organize, document, and version-control MySQL database objects using Python and GitHub.

The project connects to a MySQL database, extracts database object definitions and metadata, stores them as source files in a structured repository, and uses Git/GitHub to maintain the history of database changes.

### Main Goal

```text
MySQL Database
       ↓
Python Extraction
       ↓
Database Source Files
       ↓
Git
       ↓
GitHub Repository
```

---

## Project Objectives

The project is designed to:

* Connect to MySQL databases using Python.
* Extract database objects automatically.
* Store database object definitions as `.sql` files.
* Extract technical metadata such as columns, data types, keys, and comments.
* Maintain database source code in Git.
* Track database changes over time.
* Store the extracted database source in GitHub.
* Provide a structured and repeatable database source-control process.

---

## Database Objects

The extraction process is planned to support the following MySQL objects:

| Object            | Extraction |
| ----------------- | ---------- |
| Tables            | Planned    |
| Columns           | Planned    |
| Primary Keys      | Planned    |
| Foreign Keys      | Planned    |
| Indexes           | Planned    |
| Views             | Planned    |
| Stored Procedures | Planned    |
| Functions         | Planned    |
| Triggers          | Planned    |
| Events            | Planned    |

Additional object types can be added as the project evolves.

---

## Repository Structure

```text
MYSQL/
│
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── database/
│   └── EMPLOYEE/
│       ├── tables/
│       ├── views/
│       ├── procedures/
│       ├── functions/
│       ├── triggers/
│       └── events/
│
└── scripts/
    └── extract.py
```

---

## Directory Description

### `database/`

Contains the extracted MySQL database source.

```text
database/
└── EMPLOYEE/
```

`EMPLOYEE` represents the MySQL database being extracted.

---

### `database/EMPLOYEE/tables/`

Contains extracted table definitions.

Example:

```text
tables/
├── employees.sql
├── departments.sql
├── salaries.sql
└── titles.sql
```

The files contain the SQL definition of the corresponding tables.

---

### `database/EMPLOYEE/views/`

Contains extracted MySQL views.

Example:

```text
views/
└── employee_details.sql
```

---

### `database/EMPLOYEE/procedures/`

Contains extracted stored procedures.

Example:

```text
procedures/
└── get_employee.sql
```

---

### `database/EMPLOYEE/functions/`

Contains extracted MySQL functions.

Example:

```text
functions/
└── employee_count.sql
```

---

### `database/EMPLOYEE/triggers/`

Contains extracted MySQL triggers.

Example:

```text
triggers/
└── employee_audit.sql
```

---

### `database/EMPLOYEE/events/`

Contains extracted MySQL events.

Example:

```text
events/
└── salary_update.sql
```

---

### `scripts/`

Contains the Python extraction program.

```text
scripts/
└── extract.py
```

The extraction program will:

1. Connect to MySQL.
2. Identify database objects.
3. Extract object definitions.
4. Extract metadata.
5. Create the required directories.
6. Write the extracted source files.
7. Update existing source files when database objects change.

---

## Python Environment

The project uses a Python virtual environment.

Recommended environment:

```text
Python
    ↓
Virtual Environment (.venv)
    ↓
Project Dependencies
    ↓
MySQL Connection
```

The `.venv` directory is local to the development environment and must not be committed to GitHub.

---

## Prerequisites

Before running the project, install:

* Python 3.x
* MySQL Server
* Git
* Visual Studio Code
* GitHub account
* Access to the target MySQL database

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

---

## Project Setup

### 1. Clone the repository

```powershell
git clone https://github.com/vamc003/MYSQL.git
```

Move into the repository:

```powershell
cd MYSQL
```

---

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

---

### 3. Activate the virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should display:

```text
(.venv)
```

Example:

```text
(.venv) PS C:\...\MYSQL>
```

---

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## Database Configuration

Database credentials should not be stored directly in Python source code or committed to GitHub.

Create a local `.env` file:

```text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=employee
```

The `.env` file is excluded from Git using `.gitignore`.

For reference, the repository contains:

```text
.env.example
```

Developers can copy the example configuration and provide their local credentials.

---

## Extraction Process

The main extraction program will be:

```powershell
python scripts/extract.py
```

The expected process is:

```text
                  MySQL
                    │
                    ▼
             scripts/extract.py
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
       Tables     Views    Procedures
          │         │         │
          ├─────────┼─────────┤
          │         │         │
          ▼         ▼         ▼
      Functions  Triggers   Events
                    │
                    ▼
          database/EMPLOYEE/
                    │
                    ▼
               Git Changes
                    │
                    ▼
                 GitHub
```

---

## Example Generated Output

After extraction, the repository may contain:

```text
database/
└── EMPLOYEE/
    │
    ├── tables/
    │   ├── employees.sql
    │   ├── departments.sql
    │   ├── dept_emp.sql
    │   ├── dept_manager.sql
    │   ├── salaries.sql
    │   └── titles.sql
    │
    ├── views/
    │   └── employee_details.sql
    │
    ├── procedures/
    │   └── get_employee.sql
    │
    ├── functions/
    │   └── employee_count.sql
    │
    ├── triggers/
    │   └── employee_audit.sql
    │
    └── events/
        └── salary_update.sql
```

The actual files depend on the objects present in the MySQL database.

---

## Metadata

The project will also capture technical metadata where available.

For tables and columns, metadata may include:

* Table name
* Table description
* Column name
* Data type
* Column type
* Nullable
* Default value
* Primary key
* Foreign key
* Index information
* Auto-increment
* Column comments

Example:

```text
employees
│
├── emp_no
│   ├── INT
│   ├── NOT NULL
│   └── PRIMARY KEY
│
├── first_name
│   └── VARCHAR(14)
│
└── hire_date
    └── DATE
```

Business descriptions can be added separately when the technical database metadata does not provide the business purpose of a table or column.

---

## Git Workflow

After extracting database objects, review the changes before committing them.

Check the status:

```powershell
git status
```

Review changes:

```powershell
git diff
```

Stage the changes:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Update MySQL database source"
```

Push to GitHub:

```powershell
git push
```

---

## Example Change Workflow

Suppose a new column is added to the MySQL database:

```sql
ALTER TABLE employees
ADD COLUMN salary DECIMAL(10,2);
```

Run:

```powershell
python scripts/extract.py
```

Git can then identify the changed source file:

```text
database/EMPLOYEE/tables/employees.sql
```

Review:

```powershell
git diff
```

Then commit:

```powershell
git add .
git commit -m "Add salary column to employees"
git push
```

This provides a historical record of database changes.

---

## Security

Database credentials must never be committed to this repository.

Do not commit:

```text
.env
```

Do not place passwords directly inside:

```text
scripts/*.py
```

Use environment variables instead.

The `.gitignore` file excludes sensitive and local development files.

---

## Development Roadmap

### Phase 1 — Project Setup

* [x] Create GitHub repository
* [ ] Create project structure
* [ ] Configure Python virtual environment
* [ ] Install MySQL Python connector
* [ ] Configure `.env`

### Phase 2 — MySQL Connection

* [ ] Create MySQL connection
* [ ] Test database connectivity
* [ ] Validate database credentials

### Phase 3 — Table Extraction

* [ ] Discover tables
* [ ] Extract table definitions
* [ ] Extract columns
* [ ] Extract primary keys
* [ ] Extract foreign keys
* [ ] Extract indexes
* [ ] Extract comments

### Phase 4 — Database Objects

* [ ] Extract views
* [ ] Extract procedures
* [ ] Extract functions
* [ ] Extract triggers
* [ ] Extract events

### Phase 5 — Git Integration

* [ ] Review generated changes
* [ ] Commit database source
* [ ] Push changes to GitHub
* [ ] Maintain database source history

### Phase 6 — Future Enhancements

* [ ] Automated metadata generation
* [ ] Object dependency analysis
* [ ] Validation
* [ ] Automated extraction
* [ ] GitHub Actions
* [ ] Change reporting
* [ ] Multiple database/environment support

---

## Project Workflow

The intended long-term workflow is:

```text
             ┌─────────────────┐
             │   MySQL Server  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Python Extractor│
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Database Source │
             │     Files       │
             └────────┬────────┘
                      │
                      ▼
                  Git Diff
                      │
                      ▼
                 Git Commit
                      │
                      ▼
             ┌─────────────────┐
             │     GitHub      │
             └─────────────────┘
```

---

## Repository

GitHub repository:

`https://github.com/vamc003/MYSQL`

---

## Status

**Current Status:** Initial project setup

The project is currently being developed incrementally, starting with MySQL connectivity and table extraction before adding support for additional database objects.

