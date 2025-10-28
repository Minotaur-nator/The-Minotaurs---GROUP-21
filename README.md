# Team Skill Inventory App
A simple, effective, and real-time skill tracking dashboard built using Streamlit for the frontend and MySQL for persistent backend storage. This application allows teams to quickly input, view, and manage individual skills and proficiency levels.

## Features
CRUD Operations:
Easily Create, Read, and Delete skill entries via the web interface.
Real-time Data: Data is stored in a MySQL database, providing persistence and real-time updates across sessions.
Responsive UI: Built with Streamlit for a clean, mobile-friendly interface.
Proficiency Levels: Tracks skills using predefined levels: Beginner, Intermediate, and Expert.🛠️ PrerequisitesBefore running the application, you need the following software installed and configured;
1. Python 3ySQL Server
2. A running MySQL instance.
3. Database Credentials: User with rights to create databases and tables.
   
## Setup and Installation
1. Clone the Repositorygit clone <repository-url>
cd team-skill-inventory
6. Python Environment Setup and Install the required Python libraries (streamlit and mysql-connector-python): pip install streamlit mysql-connector-python
7. Database ConfigurationYou need to match the credentials used in the Python script (main.py). Open the application file and update the following global constants to match your local MySQL configuration:
  DB_HOST = "localhost"
  DB_USER = "root"
  DB_PASSWORD = "YOUR_MYSQL_PASSWORD" # <--- IMPORTANT: Update this
  DB_NAME = "skill_inventory_db" 
The application will automatically attempt to create the skill_inventory_db database and the team_skills table if they do not already exist on the first run.

## Run the Streamlit Application
Start the application from your terminal:
streamlit run <your-script-name>.py 
(Assuming your file is named something like main.py)
The application will launch in your browser, typically at http://localhost:8501.

## Usage
The application is split into two main sections:
1. Add New Skill Entry Use the form in the left column to add new data:
   Person's Name: The team member's name.Skill Name: The specific skill (e.g., Python, SQL, Cloud Architecture).
   Proficiency Level: Select from Beginner, Intermediate, or Expert. Click "Save Skill Entry" to commit the data to MySQL.
2. View All Skill Entries. The right column displays a sortable and searchable st.dataframe showing all entries currently stored in the MySQL table.
3. Delete Skill EntryBelow the main table, you can remove data:Select the specific entry you want to delete from the dropdown menu (e.g., Alice | Python | Expert).
      Click "Delete Selected Entry".

## Contributors:
Gloria Kayasa - Project Manager
Clinton Nwachukwu - Error Handler
Phils Blay - Ui designer
John Antwi - Consultant
Joseph Artur - Overviewer
