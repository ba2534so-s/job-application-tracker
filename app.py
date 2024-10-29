import time
import webbrowser
from threading import Thread
from app import create_app

app = create_app()

# ChatGPT was used to guide me through how to start the application and open browser after server has started
if __name__ == "__main__":
    # Start Flask server in a separate thread
    server_thread = Thread(target=lambda: app.run(debug=False))
    # Daemonize thread to close it with the main program
    server_thread.daemon = True 

    # Wait a short time to ensure the server is up
    time.sleep(1)  # Adjust if necessary

    # Open the login page
    webbrowser.open("http://127.0.0.1:5000/auth/login")