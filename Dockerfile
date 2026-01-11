FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
COPY scripts/wait_for_db.sh /code/scripts/wait_for_db.sh
COPY scripts/entrypoint.sh /code/scripts/entrypoint.sh
RUN chmod +x /code/scripts/wait_for_db.sh /code/scripts/entrypoint.sh
ENTRYPOINT ["/code/scripts/entrypoint.sh"]
