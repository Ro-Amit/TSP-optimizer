import sys
from PyQt5.QtWidgets import QApplication
from gui.gui import TSPGui  # Adjust the import according to your project structure

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TSPGui()  # Initialize the TSP GUI
    window.show()      # Show the GUI window
    sys.exit(app.exec_())  # Start the application event loop