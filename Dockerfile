FROM python 

WORKDIR /app

COPY ./app /app 

RUN pip install flask Flask-SQLAlchemy jwt flask_mysqldb wtforms passlib

ENTRYPOINT [ "python", "/app/app.py" ]