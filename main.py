from models.db_init import create_tables, insert_books
import subprocess
import signal
import sys

node_process = None

def start_node_server():
    global node_process
    try:
        print("Starting Node.js server...")
        node_process = subprocess.Popen(["node", "server.js"])  
    except FileNotFoundError:
        print("Node.js is not installed or 'node' is not in your PATH.")
        sys.exit(1)

def stop_node_server():
    global node_process
    if node_process:
        print("Stopping Node.js server...")
        node_process.terminate() 
        node_process.wait() 
        print("Node.js server stopped.")

def main():

    create_tables()
    insert_books()
    print("Database initialized and tables created.")

    start_node_server()

    def signal_handler(sig, frame):
        print("\nShutting down...")
        stop_node_server()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


    print("Press Ctrl+C to stop the server.")
    while True:
        pass  

if __name__ == "__main__":
    main()