import logging
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 2: ERROR & FATAL; 3: FATAL only
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import absl
import tensorflow_model_analysis as tfma
from typing import Any, Dict, Iterable, List, Text
from tfx.components import Evaluator, Pusher, ResolverNode, StatisticsGen, Trainer
from tfx.components.base import executor_spec
from tfx.components import ImportExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Trainer, ResolverNode, Evaluator, Pusher
from tfx.components.trainer.executor import GenericExecutor
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import metadata, pipeline
from tfx.proto import example_gen_pb2, trainer_pb2, pusher_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model, ModelBlessing
from classification_pipeline import constants


def init_beam_pipeline(
    pipeline_name: Text,
    pipeline_root: Text,
    data_root: Text,
    module_file: Text,
    serving_model_dir: Text,
    metadata_path: Text,
    beam_pipeline_args: List[Text]) -> pipeline.Pipeline:

    absl.logging.info(f"Pipeline root set to: {pipeline_root}")

    input_config = example_gen_pb2.Input(
        splits=[
        example_gen_pb2.Input.Split(name='train', pattern='train/*'),
        example_gen_pb2.Input.Split(name="eval", pattern="test/*")
        ]
        )

    example_gen = ImportExampleGen(
        input_base=data_root,
        input_config=input_config,
        # output_config=output,
        # custom_executor_spec=executor_spec.ExecutorClassSpec(ImageExampleGenExecutor)
        )

    statistics_gen = StatisticsGen(
        examples=example_gen.outputs['examples']
        )

    schema_gen = SchemaGen(
        statistics=statistics_gen.outputs['statistics'],
        infer_feature_shape=True
        )

    example_validator = ExampleValidator(
        statistics=statistics_gen.outputs['statistics'],
        schema=schema_gen.outputs['schema']
        )

    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=schema_gen.outputs['schema'],
        module_file=module_file
        )

    trainer = Trainer(
        module_file=module_file,
        custom_executor_spec=executor_spec.ExecutorClassSpec(GenericExecutor),
        examples=transform.outputs['transformed_examples'],
        transform_graph=transform.outputs['transform_graph'],
        schema=schema_gen.outputs['schema'],
        train_args=trainer_pb2.TrainArgs(splits=["train"]),
        eval_args=trainer_pb2.EvalArgs(splits=["eval"]),
        )

    # model_resolver = ResolverNode(
    #     instance_name='latest_blessed_model_resolver',
    #     resolver_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
    #     model=Channel(type=Model),
    #     model_blessing=Channel(type=ModelBlessing)
    #     )

    # eval_config = tfma.EvalConfig(
    #     model_specs=[
    #         tfma.ModelSpec(label_key=constants.LABEL_KEY)
    #     ],
    #     metrics_specs=[
    #         tfma.MetricsSpec(
    #             metrics=[
    #                 tfma.MetricConfig(class_name='ExampleCount'),
    #                 tfma.MetricConfig(class_name='AUC'),
    #                 tfma.MetricConfig(class_name='Accuracy',
    #                   threshold=tfma.MetricThreshold(
    #                       value_threshold=tfma.GenericValueThreshold(
    #                           lower_bound={'value': 0.65}),
    #                       change_threshold=tfma.GenericChangeThreshold(
    #                           direction=tfma.MetricDirection.HIGHER_IS_BETTER,
    #                           absolute={'value': 0.01})))
    #             ]
    #         )
    #     ],
    #     slicing_specs=[
    #         tfma.SlicingSpec()
    #     ])

    # evaluator = Evaluator(
    #     examples=example_gen.outputs['examples'],
    #     model=trainer.outputs['model'],
    #     baseline_model=model_resolver.outputs['model'],
    #     eval_config=eval_config
    #     )

    pusher = Pusher(
        model=trainer.outputs['model'],
        # model_blessing=evaluator.outputs['blessing'],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=serving_model_dir
                )
            )
        )

    p = pipeline.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        components=[
            example_gen,
            statistics_gen,
            schema_gen,
            example_validator,
            transform,
            trainer,
            # model_resolver,
            # evaluator,
            pusher
        ],
        enable_cache=True,
        metadata_connection_config=metadata.sqlite_metadata_connection_config(
            metadata_path
        ),
        beam_pipeline_args=beam_pipeline_args,
    )

    return p