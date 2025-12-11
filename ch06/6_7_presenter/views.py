# Views Layer
from .viewmodels import ScoreViewModel


class WebScoreView:
    def display(self, view_model: ScoreViewModel) -> str:
        styled_grade = f"<em>{view_model.grade}</em>"
        return f"""
        <div class="score-card">
            <h2>성적 결과: {view_model.student_id}</h2>
            <div class="score-details">
                <p>평균: <strong style="color: blue">{view_model.average}</strong></p>
                <p>등급: {styled_grade}</p>
                <p>상태: <span style="color: {'#28a745' if view_model.status == '성공' else '#dc3545'}">{view_model.status}</span></p>
            </div>
        </div>
        """


class ApiScoreView:
    def display(self, view_model: ScoreViewModel) -> dict:
        return {
            "student_id": view_model.student_id,
            "average": view_model.average,
            "grade": view_model.grade,
            "status": view_model.status,
        }
