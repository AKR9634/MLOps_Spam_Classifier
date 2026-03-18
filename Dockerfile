FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords

EXPOSE 5000

CMD ["python3", "app.py"]