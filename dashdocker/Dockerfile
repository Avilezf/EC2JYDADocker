FROM python:3.6-slim
RUN pip install dash numpy matplotlib pandas flask_sqlalchemy flask plotly
COPY . .
WORKDIR /slides/

EXPOSE 8000
ENTRYPOINT ["python", "app.py"]