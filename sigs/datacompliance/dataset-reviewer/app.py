from main import *

# from flask_cors import CORS

# Models in models are not initialized if they are not imported, because they are not imported into the main program
from main.model.db_models import *

from main.api import blueprint

# Get app via singleton to ensure this app is unique in this project.
app = SingletonApp()
app.register_blueprint(blueprint)

# CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
