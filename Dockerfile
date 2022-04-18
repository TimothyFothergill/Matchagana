FROM python:latest
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
RUN export FLASK_APP="app/Matchagana.py"
RUN export FLASK_ENV="development"
CMD ["flask", "run"]