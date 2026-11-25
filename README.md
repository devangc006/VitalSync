# VitalSync

VitalSync is a Flask-based personal health and environmental wellness dashboard. It combines profile and BMI data with weather conditions to provide hydration, UV protection, skincare, attire, and exercise recommendations.

## Features

- User registration, login, logout, and session-based authentication
- Personal profile management with BMI calculation
- City-based weather details and seven-day forecast
- Health recommendations for hydration, UV exposure, skincare, clothing, and exercise
- Weather and recommendation history
- User settings, including notification and appearance preferences
- SQLite development database with PostgreSQL/ShaktiDB support
- OpenWeatherMap integration with built-in mock weather fallback

## Tech Stack

- Python 3 and Flask
- SQLite 3 (default) or PostgreSQL
- Jinja2 templates
- HTML, CSS, and JavaScript
- pytest
- OpenWeatherMap API

## Getting Started

### Prerequisites

- Python 3.10 or newer
- `pip`
- Optional: PostgreSQL and an OpenWeatherMap API key

### Installation

```bash
git clone https://github.com/devangc006/VitalSync.git
cd VitalSync

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open `http://localhost:5000`.

VitalSync uses mock weather data when `OPENWEATHERMAP_API_KEY` is not set or when an API request fails.

## Configuration

Configuration is read from environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `FLASK_ENV` | `development` | Selects the Flask environment |
| `SECRET_KEY` | Development key | Flask session signing key |
| `OPENWEATHERMAP_API_KEY` | Empty | Enables live OpenWeatherMap data |
| `USE_POSTGRES` | `false` | Enables PostgreSQL instead of SQLite |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `vitalsync` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL username |
| `DB_PASS` | `postgres` | PostgreSQL password |

Example:

```bash
export FLASK_ENV=development
export SECRET_KEY='replace-with-a-long-random-value'
export OPENWEATHERMAP_API_KEY='your-api-key'
python app.py
```

For PostgreSQL/ShaktiDB:

```bash
export USE_POSTGRES=true
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=vitalsync
export DB_USER=postgres
export DB_PASS='your-password'
python app.py
```

## Database

By default, the application stores data in `database/vitalsync.db`. The schema is defined in `database/schema.sql` and is initialized when the app starts.

When PostgreSQL is disabled, `init_db()` recreates the SQLite database file and applies `schema.sql` on startup. PostgreSQL mode executes the schema statements against the configured database.

`database/sample_data.sql` contains example users, settings, weather records, recommendations, and audit records. It is not loaded automatically.

## Tests

Run the test suite from the project root:

```bash
pytest
```

The tests cover authentication, database initialization and CRUD operations, weather fallback behavior, routes, and recommendations.

## Project Structure

```text
VitalSync/
├── app.py                 # Application factory and entry point
├── config.py              # Environment-based configuration
├── database/              # Schema, SQLite database, and queries
├── routes/                # Flask blueprints
├── services/              # Weather and health recommendation logic
├── static/                # CSS and JavaScript assets
├── templates/             # Jinja2 HTML templates
├── tests/                 # pytest test suite
└── requirements.txt       # Python dependencies
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
