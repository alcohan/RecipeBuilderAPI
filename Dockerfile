FROM tadeorubio/pyodbc-msodbcsql17

# Flask config
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

# Environment variables for server
ENV SERVER 192.168.7.122:1433
ENV DATABASE SaladBuilder

# Install ODBC Driver and pyodbc
RUN pip install pyodbc

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--no-reload"]