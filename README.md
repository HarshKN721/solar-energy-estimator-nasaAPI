# ☀️ Solar Energy Estimator (NASA POWER API)

A cross-platform desktop application that estimates daily electricity generation from solar panels using real NASA satellite data.

Built using Python and PyQt6, this app allows users to input a geographic location and receive near-accurate solar energy estimates.

---

## 🚀 Features

- 🌍 Location-based solar estimation (Latitude & Longitude)
- 📅 Date-based solar irradiance data
- ☀️ Uses NASA POWER API (satellite-based data)
- ⚡ Estimates electricity generation (kWh/day)
- 📊 Shows raw solar irradiance values
- 📤 Export results as CSV
- 🌙 Modern dark-mode UI
- 🖥️ Works on Windows, macOS, and Linux

---

## 🧮 Formula Used

Energy (kWh/day) =
Solar Irradiance (kWh/m²/day)
× Panel Area (m²)
× Panel Efficiency
× System Loss Factor (0.75)

> ⚠️ Values are near-accurate approximations suitable for academic and research purposes.

---

## 📡 Data Source

- **NASA POWER API**
- Parameter used: `ALLSKY_SFC_SW_DWN`
- Unit: kWh/m²/day

---

## 🛠️ Tech Stack

- Python 3.x
- PyQt6 (GUI)
- Requests (API calls)
- Pandas (CSV export)
- ReportLab (PDF-ready support)
- PyInstaller (Windows executable)

---

## 🧪 Installation (From Source)

```bash
git clone https://github.com/<your-username>/solar-energy-estimator-nasa.git
cd solar-energy-estimator-nasa
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py


🪟 Windows Executable
A standalone Windows executable (app.exe) can be generated using:

pyinstaller --onefile --windowed app.py


📜 Disclaimer

This application provides estimated values based on satellite data and standard assumptions.
It is not intended for commercial-grade system design.

👨‍💻 Author

Harsh
B.Tech CSE (Cloud Computing & Automation)



