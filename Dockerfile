FROM python
COPY . .
RUN pip install flask
RUN pip install pymongo
CMD ["python3", "Matchagana.py"]