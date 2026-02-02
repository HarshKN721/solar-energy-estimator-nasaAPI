import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QDateEdit,
    QFileDialog, QFrame
)
from PyQt6.QtCore import QDate

from nasa_api import fetch_irradiance
from calculator import calculate_energy
from exporter import export_csv


class SolarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar Energy Estimator")
        self.setFixedWidth(460)

        self.last_result = None

        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(14)

        title = QLabel("☀ Solar Energy Estimator")
        title.setObjectName("title")

        self.lat = QLineEdit()
        self.lat.setPlaceholderText("Latitude (e.g. 28.61)")

        self.lon = QLineEdit()
        self.lon.setPlaceholderText("Longitude (e.g. 77.20)")

        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)

        self.area = QLineEdit("2.5")
        self.area.setToolTip(
        "Total surface area of the solar panel in square meters.\n"
        "Typical residential panels are ~2–3 m²."
        )

        self.eff = QLineEdit("0.18")
        self.eff.setToolTip(
            "Panel efficiency (fraction).\n"
            "18% is typical for standard silicon panels."
        )


        self.calc_btn = QPushButton("Estimate Energy")
        self.calc_btn.clicked.connect(self.run_calculation)

        self.export_btn = QPushButton("Export CSV")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_csv_file)

        # Result card
        self.result_card = QFrame()
        self.result_card.setToolTip(
            "Formula Used:\n"
            "Energy (kWh/day) =\n"
            "Irradiance × Panel Area × Efficiency × Loss Factor (0.75)\n\n"
            "Data Source: NASA POWER API\n"
            "Values are near-accurate approximations."
        )
        self.result_card.setObjectName("resultCard")
        self.result_label = QLabel("Enter details and click Estimate")
        self.result_label.setWordWrap(True)

        card_layout = QVBoxLayout()
        card_layout.addWidget(self.result_label)
        self.result_card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(QLabel("Latitude"))
        layout.addWidget(self.lat)
        layout.addWidget(QLabel("Longitude"))
        layout.addWidget(self.lon)
        layout.addWidget(QLabel("Date"))
        layout.addWidget(self.date)
        layout.addWidget(QLabel("Panel Area (m²)"))
        layout.addWidget(self.area)
        layout.addWidget(QLabel("Efficiency"))
        layout.addWidget(self.eff)
        layout.addWidget(self.calc_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.result_card)

        self.setLayout(layout)

    def run_calculation(self):
        if not all([
            self.lat.text(),
            self.lon.text(),
            self.area.text(),
            self.eff.text()
        ]):
            self.show_error("❌ No value entered in one or more fields.")
            return

        try:
            lat = float(self.lat.text())
            lon = float(self.lon.text())
            area = float(self.area.text())
            eff = float(self.eff.text())
        except ValueError:
            self.show_error("❌ Invalid numeric input.")
            return

        date_str = self.date.date().toString("yyyyMMdd")

        try:
            irradiance = fetch_irradiance(lat, lon, date_str)
            energy = calculate_energy(irradiance, area, eff)
        except Exception as e:
            self.show_error("❌ Failed to fetch NASA data.")
            return

        self.last_result = {
            "Latitude": lat,
            "Longitude": lon,
            "Date": date_str,
            "Irradiance (kWh/m²/day)": round(irradiance, 2),
            "Estimated Energy (kWh/day)": round(energy, 2),
            "Source": "NASA POWER API",
            "Note": "Values are approximations"
        }

        self.result_label.setStyleSheet("color: #e6e6e6;")
        self.result_label.setText(
            f"🌞 Irradiance: {irradiance:.2f} kWh/m²/day\n"
            f"⚡ Estimated Energy: {energy:.2f} kWh/day\n\n"
            "Source: NASA POWER API\n"
            "⚠ Values are approximations"
        )

        self.export_btn.setEnabled(True)

    def show_error(self, message):
        self.result_label.setStyleSheet("color: #ff6b6b;")
        self.result_label.setText(message)
        self.export_btn.setEnabled(False)

    def export_csv_file(self):
        if not self.last_result:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV Files (*.csv)"
        )

        if path:
            export_csv(self.last_result, path)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e6e6e6;
                font-size: 13px;
            }
            QLabel {
                font-weight: 600;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 10px;
            }
            QLineEdit, QDateEdit {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
            QPushButton {
                background-color: #3b82f6;
                border: none;
                padding: 8px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:disabled {
                background-color: #555;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QFrame#resultCard {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SolarApp()
    window.show()
    sys.exit(app.exec())
