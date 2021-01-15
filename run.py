import os
from blog import app
if os.path.exists("env.py"):
    import env


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
