from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DB_CONNECTION_STRING")
if not DB_URL:
    raise RuntimeError("DB_CONNECTION_STRING is required")


def get_db_conn():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)


def init_db():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                  id SERIAL PRIMARY KEY,
                  title TEXT NOT NULL,
                  done BOOLEAN NOT NULL DEFAULT FALSE,
                  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
                );
                """
            )
        conn.commit()


init_db()


@app.route("/")
def home():
    return "Flask + Docker + GHCR + Terraform + Render + Todo API"


@app.route("/health")
def health():
    return jsonify({"status": "up"})


@app.route("/todos", methods=["GET"])
def list_todos():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done, created_at FROM todos ORDER BY id")
            rows = cur.fetchall()
    return jsonify(rows)


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json(force=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO todos (title) VALUES (%s) RETURNING id, title, done, created_at",
                (title,),
            )
            todo = cur.fetchone()
            conn.commit()

    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    data = request.get_json(force=True) or {}
    done = data.get("done")
    title = data.get("title")

    if done is None and title is None:
        return jsonify({"error": "nothing to update"}), 400

    set_fragments = []
    values = []
    if done is not None:
        set_fragments.append("done = %s")
        values.append(bool(done))
    if title is not None:
        set_fragments.append("title = %s")
        values.append(str(title).strip())

    values.append(todo_id)

    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE todos SET {', '.join(set_fragments)} WHERE id = %s RETURNING id, title, done, created_at",
                tuple(values),
            )
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "not found"}), 404
            conn.commit()

    return jsonify(row)


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s RETURNING id", (todo_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "not found"}), 404
            conn.commit()

    return jsonify({"deleted": todo_id})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

