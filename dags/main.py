# File: ~/airflow/dags/main.py
from __future__ import annotations
import sys
import os
import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule  # <- Correction ici (import correct)

# ✅ Ajouter le dossier src dans le PYTHONPATH pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from model_development import (
    load_data,
    data_preprocessing,
    separate_data_outputs,
    build_model,
    load_model,
)

# ---------- Default args ----------
default_args = {
    "start_date": pendulum.datetime(2024, 1, 1, tz="UTC"),
    "retries": 0,
}

# ---------- DAG ----------
with DAG(
    dag_id="Airflow_Lab2",
    default_args=default_args,
    description="Airflow-Lab2 DAG Description",
    schedule="@daily",
    catchup=False,
    tags=["example"],
    max_active_runs=1,
) as dag:

    # ---------- Tasks ----------
    owner_task = BashOperator(
        task_id="task_using_linked_owner",
        bash_command="echo 1",
    )

    send_email = EmailOperator(
        task_id="send_email",
        to="djamila.taki3@gmail.com",
        subject="Notification from Airflow",
        html_content="<p>This is a notification email sent from Airflow.</p>",
    )

    load_data_task = PythonOperator(
        task_id="load_data_task",
        python_callable=load_data,
    )

    data_preprocessing_task = PythonOperator(
        task_id="data_preprocessing_task",
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    separate_data_outputs_task = PythonOperator(
        task_id="separate_data_outputs_task",
        python_callable=separate_data_outputs,
        op_args=[data_preprocessing_task.output],
    )

    build_save_model_task = PythonOperator(
        task_id="build_save_model_task",
        python_callable=build_model,
        op_args=[separate_data_outputs_task.output, "model.sav"],
    )

    load_model_task = PythonOperator(
        task_id="load_model_task",
        python_callable=load_model,
        op_args=[separate_data_outputs_task.output, "model.sav"],
    )

    trigger_dag_task = TriggerDagRunOperator(
        task_id="my_trigger_task",
        trigger_dag_id="Airflow_Lab2_Flask",
        conf={"message": "Data from upstream DAG"},
        reset_dag_run=False,
        wait_for_completion=False,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    # ---------- Dependencies ----------
    owner_task >> load_data_task >> data_preprocessing_task >> \
        separate_data_outputs_task >> build_save_model_task >> \
        load_model_task >> trigger_dag_task

    load_model_task >> send_email
