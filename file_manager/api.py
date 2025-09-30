import os
from flask import Flask, jsonify, render_template
from sqlalchemy.orm import sessionmaker
from .database import FileLog

# Function to create and configure the Flask application
def create_app(db_session: sessionmaker):
    # Define the path to the templates directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    app = Flask(__name__, template_folder=template_dir)

    # Route for the main dashboard (renders dashboard.html)
    @app.route("/")
    def index():
        # Open a new database session
        session = db_session()
        # Query the 10 most recent file logs
        recent_logs = session.query(FileLog).order_by(FileLog.moved_at.desc()).limit(10).all()
        
        # Add a human-readable timestamp property to each log
        for log in recent_logs:
            log.pretty_time = log.moved_at.strftime("%d/%m/%Y %H:%M")

        # Count number of files moved per category
        stats_counts = {}
        for (cat,) in session.query(FileLog.category).all():
            stats_counts[cat] = stats_counts.get(cat, 0) + 1

        # Render the dashboard template with logs and stats
        return render_template("dashboard.html", recent_logs=recent_logs, stats_counts=stats_counts)

    # Route for health check (returns JSON with status)
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # Route to fetch the 10 most recent moved files (JSON response)
    @app.route("/recent")
    def recent():
        # Open a new database session
        session = db_session()
        # Query the 10 most recent file logs
        logs = session.query(FileLog).order_by(FileLog.moved_at.desc()).limit(10).all()
        # Return logs in JSON format
        return jsonify([
            {
                "filename": l.filename,
                "category": l.category,
                "src": l.src,
                "dest": l.dest,
                "moved_at": l.moved_at.isoformat()
            }
            for l in logs
        ])

    # Route to fetch statistics of files moved per category (JSON response)
    @app.route("/stats")
    def stats():
        # Open a new database session
        session = db_session()
        # Query all categories
        counts = session.query(FileLog.category).all()
        stats = {}
        # Count number of files per category
        for (cat,) in counts:
            stats[cat] = stats.get(cat, 0) + 1
        return jsonify(stats)

    # Return the configured Flask app
    return app
