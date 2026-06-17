from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "datasets" / "processed" / "indore_restaurants_features.csv"

APP_NAME = "Menulytics AI Backend"
APP_VERSION = "1.0.0"