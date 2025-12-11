import click


@click.command()
@click.option("--student-id", required=True, type=str, help="Student ID")
@click.option("--calculation-type", required=True, type=str, help="Calculation type (average/total)")
def calculate_score(student_id: str, calculation_type: str):
    # 컨트롤러로 요청 전달 (6.2 섹션에서 구현)
    print(f"Received request: student_id={student_id}, calculation_type={calculation_type}")


if __name__ == "__main__":
    calculate_score()


# 실행
# 경로는 ch06/cli 들어와서
# python main.py --student-id test --calculation-type average
