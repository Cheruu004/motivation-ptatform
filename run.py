# run.py

import os
from dotenv import load_dotenv
from app import create_app
from flask_migrate import Migrate
from flask.cli import AppGroup

# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = create_app()

# Initialize Flask-Migrate
from models import db  # Ensure `db` is imported from `models.py`
migrate = Migrate(app, db)

# Create a custom CLI group for migrations
cli = AppGroup('db')

@cli.command('init')
def init_db():
    """Initialize the database."""
    from flask_migrate import init
    init()

@cli.command('migrate')
def migrate_db():
    """Run the migration scripts."""
    from flask_migrate import migrate
    migrate()

@cli.command('upgrade')
def upgrade_db():
    """Apply the latest migrations."""
    from flask_migrate import upgrade
    upgrade()

@cli.command('downgrade')
def downgrade_db():
    """Revert to a previous migration."""
    from flask_migrate import downgrade
    downgrade()

@cli.command('status')
def status_db():
    """Show the status of migrations."""
    from flask_migrate import status
    status()

# Register the CLI group with the Flask app
app.cli.add_command(cli)

if __name__ == "__main__":
    app.run(debug=True)
