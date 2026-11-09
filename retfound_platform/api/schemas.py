from typing import Literal

from pydantic import BaseModel, Field


class InputValidation(BaseModel):
    status: Literal['accepted']
    decision: Literal[1]
    image_sha256: str
    basis: str | None = None
    policy_version: str
    limitation: str


class ModelIdentity(BaseModel):
    name: str = 'RETFound MAE'
    architecture: str = 'ViT-Large'
    task: str = 'APTOS2019 · five-grade diabetic retinopathy classification'
    checkpoint_sha256: str
    preprocessing_version: str
    device: str
    dtype: str
    grades: list[str]
    input_policy: str = 'jev-fundus-choice-v1'
    automatic_retina_detection: bool = True


class PredictionResponse(BaseModel):
    schema_version: Literal['retfound-prediction/1'] = 'retfound-prediction/1'
    request_id: str
    created_utc: str
    predicted_grade: int = Field(ge=0, le=4)
    predicted_label: str
    scores: list[float] = Field(min_length=5, max_length=5)
    top_score: float
    image_sha256: str
    elapsed_ms: float
    timing_ms: dict[str, float] | None = None
    model: ModelIdentity
    input_validation: InputValidation
    interpretation: str = 'Uncalibrated model scores. Research use; not a clinical diagnosis.'
