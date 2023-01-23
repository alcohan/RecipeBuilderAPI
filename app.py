from flask import Flask
from flask_cors import CORS

# Import modules
from routes import routes
from demo import demo
# import debugpy

# debugpy.listen(("0.0.0.0",5678))

app = Flask(__name__)
app.register_blueprint(routes)
app.register_blueprint(demo)
CORS(app)

if __name__ == "__main__":
    app.run()