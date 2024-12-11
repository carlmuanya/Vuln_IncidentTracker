from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import incident

# Constants
DB_FILE = "cyber_DBfile.db"
LOG_FILE = "logfile.txt"
CSV_FILE = "incident_data.csv"
API_URL = "https://api.abuseip  db.com/api/v2/check"
API_KEY = "8f7bb5c5bf19a29cfed4a814915d3165ea2e4c79795ef62a66e95cc06527d4b2df10236972c578cd"

class CyberApplication(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Input fields
        self.type_input = TextInput(hint_text="Incident Type (e.g., Malware, Ransomware, Virus, Botnet, etc.)", multiline=False)
        self.severity_input = TextInput(hint_text="Severity (1-10)", multiline=False)
        self.description_input = TextInput(hint_text="Description", multiline=False)

        # Buttons
        self.add_button = Button(text="Add Incident")
        self.add_button.bind(on_press=self.add_incident)

        self.view_button = Button(text="View Incidents")
        self.view_button.bind(on_press=self.view_incidents)

        self.stats_button = Button(text="View Statistics")
        self.stats_button.bind(on_press=self.view_statistics)

        self.layout.add_widget(Label(text="Cybersecurity Incident Tracker"))
        self.layout.add_widget(self.type_input)
        self.layout.add_widget(self.severity_input)
        self.layout.add_widget(self.description_input)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.view_button)
        self.layout.add_widget(self.stats_button)

        # Initialize database
        incident.initialize_db(DB_FILE)

        return self.layout

    def add_incident(self, instance):
        incident_type = self.type_input.text.strip()
        severity = self.severity_input.text.strip()
        description = self.description_input.text.strip()

        if not incident.validate_input(incident_type, severity, description):
            return

        # Insert into database
        incident.insert_incident(DB_FILE, incident_type, int(severity), description)

        # Log action
        incident.log_action(LOG_FILE, f"Incident added: {incident_type}, Severity: {severity}")
        self.type_input.text = self.severity_input.text = self.description_input.text = ""

    def view_incidents(self, instance):
        incidents = incident.fetch_all_incidents(DB_FILE)
        incident.export_to_csv(incidents, CSV_FILE)

        self.layout.add_widget(Label(text="Incidents exported to CSV. Check incident_data.csv."))

    def view_statistics(self, instance):
        stats = incident.calculate_statistics(DB_FILE)
        self.layout.add_widget(Label(text=f"Average Severity: {stats['average_severity']}"))

# Run main
if __name__ == "__main__":
    CyberApplication().run()
