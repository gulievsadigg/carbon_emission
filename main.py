# Carbon Footprint Monitoring Tool
# This tool calculates the carbon footprint based on user input of their energy usage, waste production, and business travel.

import json
from fpdf import FPDF

class CarbonCalculator:
    """A class to encapsulate the carbon footprint calculations and report generation."""
    
    def __init__(self):
        """Initialize the calculator with conversion factors."""
        # These factors could be more accurately determined in future research
        self.electricity_factor = 0.0005  # kgCO2 per euro spent on electricity
        self.gas_factor = 0.0053          # kgCO2 per euro spent on gas
        self.fuel_factor = 2.32           # kgCO2 per euro spent on transportation fuel
        self.waste_factor = 0.57          # kgCO2 per kg of waste
        self.travel_factor = 2.31         # kgCO2 per liter of fuel

    def get_input(self, prompt, input_type=float):
        """Safely get user input and convert to the specified type."""
        while True:
            try:
                value = input(prompt)
                if input_type == float and float(value) < 0:
                    raise ValueError("Value cannot be negative.")
                return input_type(value)
            except ValueError as e:
                print(f"Invalid input. {e} Please enter a valid {input_type.__name__} value.")
    
    def calculate_footprint(self):
        """Gather user input and calculate the carbon footprint."""
        # Gather energy usage
        electricity_bill = self.get_input("Enter your average monthly electricity bill in euros: ")
        gas_bill = self.get_input("Enter your average monthly natural gas bill in euros: ")
        fuel_bill = self.get_input("Enter your average monthly fuel bill for transportation in euros: ")
        
        # Gather waste information
        waste_kg = self.get_input("Enter how much waste you generate per month in kilograms: ")
        recycle_percent = self.get_input("Enter how much of that waste is recycled or composted (in percentage): ")
        
        # Gather business travel information
        km_year = self.get_input("Enter how many kilometers your employees travel per year for business purposes: ")
        fuel_efficiency = self.get_input("Enter the average fuel efficiency of the vehicles used for business travel in liters per 100 kilometers: ")

        # Perform calculations
        energy_co2 = (electricity_bill * self.electricity_factor + gas_bill * self.gas_factor + fuel_bill * self.fuel_factor) * 12
        waste_co2 = waste_kg * (self.waste_factor - (recycle_percent / 100)) * 12
        travel_co2 = km_year / 100 * fuel_efficiency * self.travel_factor

        # Sum and return the results
        total_co2 = energy_co2 + waste_co2 + travel_co2
        return {
            "energy_co2": energy_co2,
            "waste_co2": waste_co2,
            "travel_co2": travel_co2,
            "total_co2": total_co2
        }


# Report Generation using FPDF
class PDFReport(FPDF):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(10)  # Line break

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)  # Line break

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()  # Line break

    def add_report_section(self, title, content):
        self.chapter_title(title)
        self.chapter_body(content)

    def add_table(self, headers, data):
        """Add a table to the PDF."""
        col_width = self.w / len(headers)
        for header in headers:
            self.cell(col_width, 10, header, border=1)
        self.ln()
        for row in data:
            for item in row:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()

def generate_report(data, organization_name):
    """Generate a PDF report from the calculated data."""
    title = f"{organization_name} Carbon Footprint Report"
    pdf = PDFReport(title)
    
    # Add the problem statement and importance of the issue
    problem_statement = f"The carbon footprint of {organization_name} directly impacts climate change. Reducing it is vital for environmental sustainability. This report analyzes the carbon footprint based on energy usage, waste production, and business travel."
    pdf.add_report_section('Problem Statement', problem_statement)
    
    # Add summaries of the analysis (e.g., tables/visualizations)
    headers = ["Category", "CO2 Emission (kg)"]
    table_data = [
        ["Energy Usage", f"{data['energy_co2']:.2f}"],
        ["Waste Production", f"{data['waste_co2']:.2f}"],
        ["Business Travel", f"{data['travel_co2']:.2f}"],
        ["Total", f"{data['total_co2']:.2f}"]
    ]
    pdf.add_report_section('Summaries of the Analysis', "")
    pdf.add_table(headers, table_data)
    
    # Add conclusions and suggestions with specific advice
    conclusions = (
        "Conclusions and suggestions for future work will involve "
        "optimization of resource usage, investment in renewable energy, "
        "and promoting recycling and waste management programs to reduce "
        "the overall carbon footprint.\n\n"
        "Specific Advice to Reduce CO2 Emissions:\n"
    )
    advice = generate_advice(data)
    pdf.add_report_section('Conclusions and Suggestions', conclusions + advice)
    
    # Save the PDF to a file
    pdf.output(f'reports/{organization_name}_carbon_footprint_report.pdf')

def generate_advice(data):
    """Generate specific advice to reduce CO2 emissions based on the footprint data."""
    advice = []
    
    if data['energy_co2'] > data['waste_co2'] and data['energy_co2'] > data['travel_co2']:
        advice.append("1. Reduce energy consumption by implementing energy-efficient practices and using renewable energy sources.")
        advice.append("2. Encourage the use of energy-saving devices and appliances.")
        advice.append("3. Conduct energy audits to identify areas for improvement.")
    
    if data['waste_co2'] > data['energy_co2'] and data['waste_co2'] > data['travel_co2']:
        advice.append("1. Implement a comprehensive recycling program to reduce waste production.")
        advice.append("2. Educate employees about waste reduction and proper recycling techniques.")
        advice.append("3. Explore opportunities to compost organic waste.")
    
    if data['travel_co2'] > data['energy_co2'] and data['travel_co2'] > data['waste_co2']:
        advice.append("1. Promote remote work and virtual meetings to reduce business travel.")
        advice.append("2. Encourage the use of public transportation, carpooling, and biking.")
        advice.append("3. Invest in fuel-efficient or electric vehicles for business travel.")
    
    if not advice:
        advice.append("1. Continue to monitor and optimize energy usage, waste production, and business travel.")
        advice.append("2. Engage employees in sustainability initiatives and create a culture of environmental responsibility.")
    
    return "\n".join(advice)
def main():
    calculator = CarbonCalculator()
    organization_name = input("Enter the name of your organization: ")
    footprint_data = calculator.calculate_footprint()
    
    # Generate report with the footprint data
    generate_report(footprint_data, organization_name)

    print("The carbon footprint has been calculated and the report has been generated.")

if __name__ == "__main__":
    main()
