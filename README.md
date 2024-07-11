# carbon_emission
his tool calculates the carbon footprint based on user input of their energy usage, waste production, and business travel. It generates a detailed PDF report with an analysis summary and suggestions for reducing CO2 emissions.

## Features

- **Energy Usage Calculation**: Calculate CO2 emissions from electricity, gas, and fuel bills.
- **Waste Production Calculation**: Calculate CO2 emissions from monthly waste generation and recycling percentage.
- **Business Travel Calculation**: Calculate CO2 emissions from annual business travel based on kilometers traveled and vehicle fuel efficiency.
- **PDF Report Generation**: Generate a comprehensive PDF report including problem statement, analysis summary, and specific advice for reducing CO2 emissions.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/gulievsadigg/carbon_emission.git
    cd carbon-footprint-monitor
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the `main.py` script to start the carbon footprint calculation and generate the PDF report.

```sh
python main.py