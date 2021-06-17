FROM python:3.9

LABEL Valerio "vinciarelli.1193280@studenti.uniroma1.it"

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1 

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
