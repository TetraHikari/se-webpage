from pydantic import BaseModel

class GradeForm(BaseModel):
    student_id: str
    score: int