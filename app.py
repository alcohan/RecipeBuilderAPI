from flask import Flask
from flask_cors import CORS
import os

# Import modules
from routes import routes
from demo import demo
import debugpy

# if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'): 
# try:
# debugpy.listen(("0.0.0.0",5678))
# except RuntimeError:
#     print("Runtime error... skipping this attach")
#     pass

app = Flask(__name__)
app.register_blueprint(routes)
app.register_blueprint(demo)
CORS(app)

if __name__ == "__main__":
    app.run()