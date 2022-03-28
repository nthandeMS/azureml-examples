import os, json
from pathlib import Path


from azure.ml import dsl
from azure.ml.entities import Environment
from azure.ml.dsl._types import DataInput, DataOutput

conda_env = Environment(
    conda_file=Path(__file__).parent / "conda.yaml",
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04"
)

@dsl.command_component(
    name="TF_mnist",
    version="1",
    display_name="TF_mnist",
    description="Train a basic neural network with TensorFlow on the MNIST dataset, distributed via TensorFlow.",
    environment=conda_env,
    distribution={
        "type": "tensorflow",
        "worker_count": 2
    },
)
def tf_func(
    trained_model_output: DataOutput, 
    epochs=3,
    steps_per_epoch=70,
    per_worker_batch_size=64,
):
    # avoid dependency issue
    from train import train_and_save_model
    train_and_save_model(per_worker_batch_size, epochs, steps_per_epoch, trained_model_output)