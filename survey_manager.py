import json
import os

def save_survey_version(user, survey):
    folder = f"user_data/{user}"
    os.makedirs(folder, exist_ok=True)
    version = len(os.listdir(folder)) + 1
    with open(f"{folder}/survey_v{version}.json", "w") as f:
        json.dump(survey, f, indent=2)

def load_survey_versions(user):
    folder = f"user_data/{user}"
    if not os.path.exists(folder):
        return []
    files = sorted(os.listdir(folder))
    surveys = []
    for file in files:
        with open(os.path.join(folder, file), "r") as f:
            surveys.append(json.load(f))
    return surveys
