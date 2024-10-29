from threading import Thread
from app import create_app

app = create_app()

# ChatGPT was used to guide me through how to start the application and open browser after server has started
if __name__ == "__main__":
    # Start Flask server in a separate thread
    Thread(target=lambda: app.run(debug=False)).start()