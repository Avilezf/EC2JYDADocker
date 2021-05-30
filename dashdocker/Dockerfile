FROM python:3.6-slim
RUN pip install dash numpy matplotlib pandas flask_sqlalchemy plotly
COPY . .
WORKDIR /slides/

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
EXPOSE 8000
ENTRYPOINT ["python", "app.py"]