import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QListWidget, QMessageBox, QGridLayout, QHBoxLayout, QListWidgetItem,
    QProgressDialog, QFrame
)
from PyQt5.QtGui import QFont, QIcon, QMovie
from PyQt5.QtCore import Qt, QSize

from src.utils import CITY_INDEX_MAP
from src.algorithms import brute_force_tsp, greedy_tsp
from src.cluster import cluster_tsp


class TSPGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TSP Route Planner')
        self.setGeometry(350, 200, 1080, 720)
        self.is_showing_optimal = False  # Track if showing optimal route

        # Main styling
        self.setStyleSheet("""
            background-color: #F7F8FA;
            border-radius: 11;
        """)

        # List of cities and selected route
        self.cities = CITY_INDEX_MAP
        self.selected_route = []

        # Standard font - using Arial
        self.standard_font = QFont("Arial", 15)

        # Set up the layout
        main_layout = QHBoxLayout()

        # Left section layout
        left_layout = QVBoxLayout()

        # Add a QLabel for the GIF
        self.gif_label = QLabel(self)
        self.gif_label.setFixedSize(450, 720)

        # Load and scale the GIF
        self.gif_movie = QMovie("pictures/background.gif")
        self.gif_movie.setScaledSize(QSize(450, 720))
        self.gif_movie.setSpeed(40)
        self.gif_label.setMovie(self.gif_movie)
        self.gif_movie.start()
        self.gif_movie.finished.connect(self.stop_on_last_frame)

        left_layout.addWidget(self.gif_label)

        # Right section layout
        right_layout = QVBoxLayout()
        top_layout = QGridLayout()

        # Start City
        self.start_city_label = QLabel("Starting City🛫:")
        self.start_city_label.setFont(self.standard_font)
        self.start_city_combo = QComboBox()
        self.start_city_combo.addItems(self.cities)
        self.start_city_combo.setFont(self.standard_font)
        self.start_city_combo.setMaxVisibleItems(6)
        self.start_city_combo.setStyleSheet("""
            border-radius: 9;
            padding: 5px;
            background-color: #FFFFFF;
        """)
        self.start_city_combo.currentTextChanged.connect(self.validate_route)

        # End City
        self.end_city_label = QLabel("Ending City🛬:")
        self.end_city_label.setFont(self.standard_font)
        self.end_city_combo = QComboBox()
        self.end_city_combo.addItems(self.cities)
        self.end_city_combo.setFont(self.standard_font)
        self.end_city_combo.setMaxVisibleItems(6)
        self.end_city_combo.setStyleSheet("""
            border-radius: 9;
            padding: 5px;
            background-color: #FFFFFF;
        """)
        self.end_city_combo.currentTextChanged.connect(self.validate_route)

        # Add City
        self.add_city_label = QLabel("Add City to Route➕:")
        self.add_city_label.setFont(self.standard_font)
        self.add_city_combo = QComboBox()
        self.add_city_combo.addItems(self.cities)
        self.add_city_combo.setFont(self.standard_font)
        self.add_city_combo.setMaxVisibleItems(6)
        self.add_city_combo.setStyleSheet("""
            border-radius: 9;
            padding: 5px;
            background-color: #FFFFFF;
        """)

        # Add City Button
        self.add_city_button = QPushButton()
        self.add_city_button.setIcon(QIcon('pictures/add_city.png'))
        self.add_city_button.setStyleSheet("""
            border-radius: 11;
            padding: 10px;
            background-color: #FFFFFF;
        """)
        self.add_city_button.clicked.connect(self.add_city_to_route)

        # Create a frame for the route view section
        self.route_view_frame = QFrame()
        self.route_view_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 11px;
                padding: 10px;
            }
        """)
        route_view_layout = QVBoxLayout(self.route_view_frame)

        # Route header layout
        route_header_layout = QHBoxLayout()
        self.route_header_label = QLabel("Current Route📌")
        self.route_header_label.setFont(self.standard_font)
        route_header_layout.addWidget(self.route_header_label)

        # Clear/Start Again button
        self.clear_route_button = QPushButton("Clear Route ×")
        self.clear_route_button.setFont(self.standard_font)
        self.clear_route_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #666666;
                padding: 5px;
                background: transparent;
            }
            QPushButton:hover {
                color: #FF6B6B;
            }
        """)
        self.clear_route_button.clicked.connect(self.handle_clear_or_restart)
        route_header_layout.addWidget(self.clear_route_button)
        route_header_layout.addStretch()

        # Selected Cities List
        self.selected_cities_list = QListWidget()
        self.selected_cities_list.setFont(self.standard_font)
        self.selected_cities_list.setStyleSheet("""
            border: none;
            background: transparent;
        """)
        self.selected_cities_list.setFrameShape(QFrame.NoFrame)

        # Add components to route view layout
        route_view_layout.addLayout(route_header_layout)
        route_view_layout.addWidget(self.selected_cities_list)

        # Find Route Button (taller)
        self.find_route_button = QPushButton(" Find Optimal Route")
        self.find_route_button.setIcon(QIcon('pictures/find_route.png'))
        self.find_route_button.setFont(self.standard_font)
        self.find_route_button.setStyleSheet("""
            border-radius: 11;
            padding: 15px;  /* Increased padding for height */
            background-color: #4D66F3;
            color: white;
            min-height: 50px;  /* Minimum height */
        """)
        self.find_route_button.clicked.connect(self.find_route)

        # Show Map Button
        self.show_map_button = QPushButton("Show Route Map🗺️")
        self.show_map_button.setFont(self.standard_font)
        self.show_map_button.setStyleSheet("""
            border-radius: 11;
            padding: 10px;
            background-color: #FFFFFF;
        """)
        self.show_map_button.clicked.connect(self.show_map_popup)

        # Layout assembly
        top_layout.addWidget(self.start_city_label, 0, 0)
        top_layout.addWidget(self.start_city_combo, 1, 0)
        top_layout.addWidget(self.end_city_label, 0, 1)
        top_layout.addWidget(self.end_city_combo, 1, 1)
        top_layout.addWidget(self.add_city_label, 2, 0)
        top_layout.addWidget(self.add_city_combo, 3, 0, 1, 2)

        right_layout.addLayout(top_layout)
        right_layout.addWidget(self.add_city_button)
        right_layout.addWidget(self.route_view_frame)
        right_layout.addWidget(self.find_route_button)
        right_layout.addWidget(self.show_map_button)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.update_route_view()

    def stop_on_last_frame(self):
        """Stop the GIF on the last frame."""
        self.gif_movie.stop()
        self.gif_movie.jumpToFrame(self.gif_movie.frameCount() - 1)

    def validate_route(self):
        """Validate the route when start or end cities change."""
        if self.is_showing_optimal:
            return  # Don't validate while showing optimal route

        start_city = self.start_city_combo.currentText()
        end_city = self.end_city_combo.currentText()

        # Remove start/end cities from selected route if they appear
        self.selected_route = [city for city in self.selected_route
                               if city != start_city and city != end_city]
        self.update_route_view()

    def handle_clear_or_restart(self):
        """Handle either clearing the route or starting again based on current state."""
        if self.is_showing_optimal:
            # Reset everything to initial state
            self.is_showing_optimal = False
            self.selected_route = []
            self.clear_route_button.setText("Clear Route ×")
            self.clear_route_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    color: #666666;
                    padding: 5px;
                    background: transparent;
                }
                QPushButton:hover {
                    color: #FF6B6B;
                }
            """)
            self.route_header_label.setText("Current Route📌")
            self.enable_input_controls(True)
        else:
            # Just clear the current route
            self.selected_route = []

        self.update_route_view()

    def enable_input_controls(self, enabled):
        """Enable or disable input controls."""
        self.start_city_combo.setEnabled(enabled)
        self.end_city_combo.setEnabled(enabled)
        self.add_city_combo.setEnabled(enabled)
        self.add_city_button.setEnabled(enabled)
        self.find_route_button.setEnabled(enabled)

    def add_city_to_route(self):
        """Add the selected city to the route list with validation."""
        if self.is_showing_optimal:
            return  # Don't allow adding cities while showing optimal route

        city = self.add_city_combo.currentText()
        start_city = self.start_city_combo.currentText()
        end_city = self.end_city_combo.currentText()

        if city == start_city or city == end_city:
            QMessageBox.warning(self, "Invalid Selection",
                                "Cannot add start or end city to the route.")
            return

        if city in self.selected_route:
            QMessageBox.warning(self, "Duplicate City",
                                f"{city} is already in the route.")
            return

        self.selected_route.append(city)
        self.update_route_view()

    def update_route_view(self):
        """Update the route display."""
        self.selected_cities_list.clear()

        if self.is_showing_optimal:
            self.route_header_label.setText("🌟 OPTIMAL ROUTE FOUND! 🌟")
            self.clear_route_button.setText("Start Again ↺")
            self.clear_route_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    color: #4D66F3;
                    padding: 5px;
                    background: transparent;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: #2D46D3;
                }
            """)

        # Add start city
        start_city = self.start_city_combo.currentText()
        item = QListWidgetItem(f"Start: {start_city}")
        item.setFont(self.standard_font)
        item.setForeground(Qt.blue)
        if self.is_showing_optimal:
            item.setBackground(Qt.yellow)
        self.selected_cities_list.addItem(item)

        # Add route cities
        for city in self.selected_route:
            route_item = QListWidgetItem(f"→ {city}")
            route_item.setFont(self.standard_font)
            if self.is_showing_optimal:
                route_item.setBackground(Qt.yellow)
            self.selected_cities_list.addItem(route_item)

        # Add end city
        end_city = self.end_city_combo.currentText()
        item = QListWidgetItem(f"End: {end_city}")
        item.setFont(self.standard_font)
        item.setForeground(Qt.red)
        if self.is_showing_optimal:
            item.setBackground(Qt.yellow)
        self.selected_cities_list.addItem(item)

        # Add total distance if showing optimal route
        if self.is_showing_optimal and hasattr(self, 'total_distance'):
            distance_item = QListWidgetItem(f"Total Distance: {self.total_distance:.2f} km")
            distance_item.setFont(self.standard_font)
            distance_item.setBackground(Qt.yellow)
            distance_item.setForeground(Qt.blue)
            self.selected_cities_list.addItem(distance_item)

    def find_route(self):
        """Find the optimal route with progress indication."""
        if len(self.selected_route) < 1:
            QMessageBox.warning(self, "Error", "You need to add at least one city.")
            return

        # Create progress dialog
        progress = QProgressDialog("Finding optimal route...", None, 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("Processing")
        progress.setValue(0)
        progress.show()

        # Simulate progress
        for i in range(100):
            progress.setValue(i)
            QApplication.processEvents()

        # Calculate route
        start_city = self.start_city_combo.currentText()
        end_city = self.end_city_combo.currentText()
        cities = [start_city] + self.selected_route + [end_city]

        # Decide which algorithm to use
        num_cities = len(cities)
        if num_cities <= 9:
            best_route, min_distance = brute_force_tsp(cities, start_city, end_city)
            algorithm_used = "Brute Force Algorithm"
        elif 10 <= num_cities <= 50:
            best_route, min_distance = cluster_tsp(cities, start_city, end_city)  # Cluster Algorithm
            algorithm_used = "Cluster Algorithm"
        else:
            best_route, min_distance = greedy_tsp(cities, start_city, end_city)
            algorithm_used = "Greedy Algorithm"
        progress.setValue(100)

        # Update route and display with highlighting
        self.selected_route = best_route[1:-1]
        self.total_distance = min_distance
        self.is_showing_optimal = True
        self.enable_input_controls(False)
        self.update_route_view()

    def show_map_popup(self):
        """Show a popup with the route map."""
        QMessageBox.information(self, "Map", "Map display is under development.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TSPGui()
    window.show()
    sys.exit(app.exec_())
