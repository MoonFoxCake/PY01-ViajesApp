FROM python:3.12

WORKDIR /app

RUN pip install poetry
COPY . .

RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app:app", "--host=0.0.0.0"]