import os
import glob
from tensorflow import keras

def load_model():
    LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "risk_icu", "training_outputs")
    local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
    local_model_paths = glob.glob(f"{local_model_directory}/*")

    most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

    latest_model = keras.models.load_model(most_recent_model_path_on_disk)
    return latest_model
