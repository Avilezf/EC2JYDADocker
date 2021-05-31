FROM python:3.6-slim
RUN pip install dash numpy matplotlib pandas flask_sqlalchemy flask plotly psycopg2
COPY . .
WORKDIR /slides/

ENTRYPOINT ["python", "app.py"]