##########################################################
### Special Things
# Add setup_demo.sh
# Add changes to /usr/local/lib/python3.8/dist-packages/airflow/executors
#   in app = Celery(...)
##########################################################

import logging
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 2: ERROR & FATAL; 3: FATAL only
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import datetime
from datetime import datetime, timedelta

from typing import List, Text

from tfx.orchestration import metadata, pipeline
from tfx.orchestration.airflow.airflow_dag_runner import AirflowDagRunner
from tfx.orchestration.airflow.airflow_dag_runner import AirflowPipelineConfig
from tfx.components import ImportExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Trainer, ResolverNode, Evaluator, Pusher
from tfx.components.trainer.executor import GenericExecutor
from tfx.components.base import executor_spec
from tfx.proto import example_gen_pb2, trainer_pb2, pusher_pb2
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.types.standard_artifacts import Model, ModelBlessing
from tfx.types import Channel

from segmentation_pipeline import base_pipeline

# Pipeline arguments for Beam powered Components.
beam_pipeline_args = [
    '--direct_running_mode=multi_processing',
    # 0 means auto-detect based on on the number of CPUs available
    # during execution time.
    '--direct_num_workers=0',
]

airflow_config = {
    "schedule_interval": None,
    "start_date": datetime(2020, 10, 17),
}

pipeline_name = "segmentation_dag"
dags_dir = "/mnt/c/dags/"
project_dir = os.path.join(dags_dir, "segmentation_pipeline")
# airflow_dir = os.path.join(os.environ["HOME"], "airflow") # ok
data_dir = os.path.join(project_dir, "data/tfrecords/")
module_file = os.path.join(project_dir, "module.py") ### write module file
serving_model_dir = os.path.join(project_dir, "serving_model", pipeline_name)


pipeline_root = os.path.join(project_dir, "pipelines", pipeline_name)
metadata_path = os.path.join(pipeline_root, "metadata", pipeline_name, "metadata.sqlite")

p = base_pipeline.init_beam_pipeline(
    pipeline_name=pipeline_name,
    pipeline_root=pipeline_root,
    data_root=data_dir,
    module_file=module_file,
    serving_model_dir=serving_model_dir,
    metadata_path=metadata_path,
    beam_pipeline_args=beam_pipeline_args
    )


DAG = AirflowDagRunner(AirflowPipelineConfig(airflow_config)).run(p)
