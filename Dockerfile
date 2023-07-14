FROM python:latest

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python database.py

CMD [ "python", "main.py" ]