# File: Flask_API.py
from __future__ import annotations

import os
import time
import requests
import pendulum

from flask import Flask, redirect, render_template
from airflow import DAG
from airflow.operators.python import PythonOperator  # ✅ Correction ici

# ---------- Config (Airflow REST API / Basic Auth) ----------
WEBSERVER = os.getenv("AIRFLOW_WEBSERVER", "http://localhost:8080")
AF_USER = os.getenv("AIRFLOW_USERNAME", os.getenv("_AIRFLOW_WWW_USER_USERNAME", "airflow"))
AF_PASS = os.getenv("AIRFLOW_PASSWORD", os.getenv("_AIRFLOW_WWW_USER_PASSWORD", "airflow"))
TARGET_DAG_ID = os.getenv("TARGET_DAG_ID", "Airflow_Lab2")

# ---------- Default args ----------
default_args = {
    "start_date": pendulum.datetime(2024, 1, 1, tz="UTC"),
    "retries": 0,
}

# ---------- Flask app ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")  # ✅ plus robuste
app = Flask(__name__, template_folder=TEMPLATE_DIR)


def get_latest_run_info():
    """
    Query Airflow REST API (/api/v1 ou /api/v2) using Basic Auth.
    Requires Airflow to be configured with:
      AIRFLOW__API__AUTH_BACKEND=airflow.api.auth.backend.basic_auth
    """
    url = f"{WEBSERVER}/api/v1/dags/{TARGET_DAG_ID}/dagRuns?order_by=-execution_date&limit=1"
    try:
        r = requests.get(url, auth=(AF_USER, AF_PASS), timeout=5)
    except Exception as e:
        return False, {"note": f"Exception calling Airflow API: {e}"}

    if r.status_code != 200:
        snippet = r.text[:200].replace("\n", " ")
        return False, {"note": f"API status {r.status_code}: {snippet}"}

    runs = r.json().get("dag_runs", [])
    if not runs:
        return False, {"note": "No DagRuns found yet."}

    run = runs[0]
    state = run.get("state")
    info = {
        "state": state,
        "run_id": run.get("dag_run_id"),
        "execution_date": run.get("execution_date"),
        "start_date": run.get("start_date"),
        "end_date": run.get("end_date"),
        "note": "",
    }
    return state == "success", info


# ---------- Flask Routes ----------
@app.route("/")
def index():
    ok, _ = get_latest_run_info()
    return redirect("/success" if ok else "/failure")


@app.route("/success")
def success():
    ok, info = get_latest_run_info()
    return render_template("success.html", **info)


@app.route("/failure")
def failure():
    ok, info = get_latest_run_info()
    return render_template("failure.html", **info)


@app.route("/health")
def health():
    return "ok", 200


def start_flask_app():
    """
    Run Flask dev server in-process; task intentionally blocks to keep API alive.
    Disable reloader to avoid forking inside Airflow worker.
    """
    print("Starting Flask on 0.0.0.0:5555 ...", flush=True)
    app.run(host="0.0.0.0", port=5555, use_reloader=False)
    while True:
        time.sleep(60)


# ---------- DAG ----------
flask_api_dag = DAG(
    dag_id="Airflow_Lab2_Flask",
    default_args=default_args,
    description="DAG to manage Flask API lifecycle",
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["Flask_API"],
    max_active_runs=1,
)

start_flask_API = PythonOperator(
    task_id="start_Flask_API",
    python_callable=start_flask_app,
    dag=flask_api_dag,
)

# ---------- DAG Entry ----------
# ---------- Standalone Flask ----------
if __name__ == "__main__":
    start_flask_app()  # lance directement le serveur Flask


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5555, debug=True)
    


# ---------- DAG Entry pour Airflow ----------
# start_flask_API  # Airflow lit cet objet, rien d'autre à faire ici

# ---------- # ---------- DAG Entry ----------


# if __name__ == "__main__":

#     app.run(host="0.0.0.0", port=5555, debug=True)

