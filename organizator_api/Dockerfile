FROM python:3.9
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
RUN pip install -r requirements/local/requirements.txt
CMD sh -c "gunicorn --reload --pythonpath . organizator_api.wsgi --bind 0.0.0.0:8000"
