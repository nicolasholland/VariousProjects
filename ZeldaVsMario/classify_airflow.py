from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'zelda',
    'start_date': datetime(2015, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('classify', default_args=default_args)

img_command = ("python $PYTHONPATH/classifiy_luigi.py GetImage "
               "$PYTHONPATH/raw_input $PYTHONPATH/tmp")

cluster_command = ("python $PYTHONPATH/classifiy_luigi.py ClusterImage "
                   "$PYTHONPATH/tmp/img.png $PYTHONPATH/tmp")

train_command = ("python $PYTHONPATH/classifiy_luigi.py TrainClassifier "
                 "$PYTHONPATH/training/ $PYTHONPATH/tmp")

predict_command = ("python $PYTHONPATH/classifiy_luigi.py "
                   "PredictLabel $PYTHONPATH/tmp")

rm_command = """
    rm $PYTHONPATH/tmp/img.png
    rm $PYTHONPATH/tmp/cluster.txt
    rm $PYTHONPATH/tmp/clf.pkl
    rm $PYTHONPATH/tmp/label.txt
"""

t1 = BashOperator(
    task_id='GetImage',
    bash_command=img_command,
    dag=dag)

t2 = BashOperator(
    task_id='ClusterImage',
    bash_command=cluster_command,
    dag=dag)

t3 = BashOperator(
    task_id='TrainClassifier',
    bash_command=train_command,
    dag=dag)

t4 = BashOperator(
    task_id='PredictLabel',
    bash_command=predict_command,
    dag=dag)

t5 = BashOperator(
    task_id='CleanAll',
    bash_command=rm_command,
    dag=dag)

t2.set_upstream(t1)

t4.set_upstream(t3)
t4.set_upstream(t2)

t5.set_upstream(t1)
t5.set_upstream(t2)
t5.set_upstream(t3)
t5.set_upstream(t4)
