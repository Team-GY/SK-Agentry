# python3.11 이미지 다운로드 FROM 
FROM python:3.11-buster

ENV PYTHONUNBUFFERED=1

# 파이썬의 출력 표시를 Docker용으로 조정
WORKDIR /src

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# poetry정의 파일 복사 (존재하는 경우)
COPY pyproject.toml* poetry.lock* ./

# poetry로 라이브러리 설치(pyproject.toml이 이미 존재하는 경우)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicorn 서버 실행
ENTRYPOINT ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--reload"]
