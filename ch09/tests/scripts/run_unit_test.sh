#!/bin/bash

echo "Running pre-commit tests (UseCase and Controller, Entity)..."

if command -v pipenv >/dev/null 2>&1; then
    pipenv run python -m unittest \
        tests/unit/usecase/test_create_order_usecase.py \
        tests/unit/controller/test_create_order_controller.py \
        tests/unit/entity/test_order.py -v
else
    # pipenv가 없으면 python3 시도
    python3 -m unittest \
        tests/unit/usecase/test_create_order_usecase.py \
        tests/unit/controller/test_create_order_controller.py \
        tests/unit/entity/test_order.py -v
fi

# 테스트 결과 확인
if [ $? -eq 0 ]; then
    echo "Pre-commit tests passed!"
    exit 0
else
    echo "Pre-commit tests failed!"
    exit 1
fi