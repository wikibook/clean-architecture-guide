# ViewModels Layer
from dataclasses import dataclass


@dataclass
class ScoreViewModel:
    student_id: str
    average: str
    status: str
    grade: str
