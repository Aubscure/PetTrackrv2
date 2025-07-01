from backend.services import db_service
from frontend.gui import launch_gui

def main():
    """
    Entry point for the PetTrackr application.
    Initializes the database connection and launches the GUI.
    """
    print("🐾 Starting PetTrackr...")

    # Optional: Test all DB connections
    db_service.test_all_connections()

    # Launch the main GUI loop
    launch_gui()

if __name__ == "__main__":
    main()