FROM python:3.7

WORKDIR /bot/

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/bot"

CMD python bot.py
