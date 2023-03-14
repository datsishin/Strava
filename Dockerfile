FROM python:3.11-slim

WORKDIR /Strava

COPY requirements.txt requirements.txt

CMD [ "python3", "-m venv venv"]
CMD [ "source", "venv/bin/activate"]

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "telegram.py"]