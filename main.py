import streamlit as st
import mysql.connector
from mysql.connector import Error

DB_HOST = "localhost"
DB_USER = "YOUR_USERNAME"
DB_PASSWORD = "YOUR_PASSWORD"
DB_NAME = "skill_inventory_db" 
TABLE_NAME = "team_skills"
PROFICIENCY_LEVELS = ['Beginner', 'Intermediate', 'Expert']


@st.cache_resource
def create_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME 
        )
        return conn
    except Error as err:
        st.error(f"**Database Connection Failed!** Please check your MySQL server and login details.")
        st.caption(f"Error details: {err}")
        return None

def setup_database(conn):
    """Ensures the required table exists in the database."""
    if not conn or not conn.is_connected():
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                person_name VARCHAR(100) NOT NULL,
                skill_name VARCHAR(100) NOT NULL,
                skill_level VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        return True
    except Error as err:
        st.error(f"Issue during initial database setup: {err}")
        return False
    finally:
        cursor.close()

def add_skill_entry(conn, person_name, skill_name, skill_level):
    """Inserts a new skill record into the table."""
    if not conn or not conn.is_connected():
        st.error("Cannot add skill: Database link is broken.")
        return False

    sql = f"INSERT INTO {TABLE_NAME}(person_name, skill_name, skill_level) VALUES(%s, %s, %s)"
    values = (person_name, skill_name, skill_level)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Error as err:
        st.error(f"Error adding skill: {err}")
        return False
    finally:
        cursor.close()

def fetch_all_skills(conn):
    """Retrieves all skill records from the table and returns a list of dictionaries."""
    if not conn or not conn.is_connected():
        return []

    try:
        cursor = conn.cursor()
        # Fetching all required columns
        cursor.execute(f"SELECT id, person_name, skill_name, skill_level FROM {TABLE_NAME} ORDER BY id DESC")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        # Convert list of tuples to list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]
        return data
    except Error as err:
        st.error(f"Error fetching skills: {err}")
        return []
    finally:
        cursor.close()

def delete_skill_entry(conn, entry_id):
    """Deletes a skill record from the table based on its ID."""
    if not conn or not conn.is_connected():
        st.error("Cannot delete skill: Database link is broken.")
        return False

    sql = f"DELETE FROM {TABLE_NAME} WHERE id = %s"
    values = (entry_id,)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Error as err:
        st.error(f"Error deleting skill: {err}")
        return False
    finally:
        cursor.close()


def main_ui():
    st.set_page_config(
        page_title="Team Skill Inventory",
        layout="wide"
    )

    st.title("Team Skill Inventory")
    
    conn = create_connection()
    if conn is None:
        st.warning("Please resolve the database connection issue to continue.")
        st.stop()
        
    if not setup_database(conn):
        st.stop()
        
    col_form, col_table = st.columns([1, 2])
    
    with col_form:
        st.header("+ Add New Skill Entry")
        
        with st.form("add_skill_form", clear_on_submit=True):
            person_name = st.text_input("Person's Name:", key="ui_person_name")
            skill_name = st.text_input("Skill Name:", key="ui_skill_name")
            skill_level = st.selectbox(
                "Proficiency Level:", 
                PROFICIENCY_LEVELS, 
                index=1, 
                key="ui_skill_level"
            )

            submitted = st.form_submit_button("Save Skill Entry", type="primary")

            if submitted:
                if not person_name.strip() or not skill_name.strip():
                    st.warning("Name and Skill fields cannot be empty!")
                else:
                    if add_skill_entry(conn, person_name.strip(), skill_name.strip(), skill_level):
                        st.success(f"Skill '{skill_name}' saved for {person_name}!")
                        st.rerun()

    with col_table:
        st.header("All Skill Entries")
        
        all_skills = fetch_all_skills(conn)
        
        if all_skills:
            st.dataframe(
                all_skills, 
                use_container_width=True,
                column_order=("id", "person_name", "skill_name", "skill_level"),
                column_config={
                    "id": st.column_config.Column("ID", width="small"),
                    "person_name": "Person Name",
                    "skill_name": "Skill Name",
                    "skill_level": "Level"
                },
                hide_index=True
            )
            
            st.markdown("---")
            st.subheader("Delete Skill Entry")
            
            with st.form("delete_skill_form"):
                
                options = [
                    f"{s['person_name']} | {s['skill_name']} | {s['skill_level']}"
                    for s in all_skills
                ]
                
                id_map = {options[i]: all_skills[i]['id'] for i in range(len(all_skills))}
                
                skill_to_delete_display = st.selectbox(
                    "Select an entry to delete:", 
                    options=options,
                    index=None,
                    placeholder="Choose a skill entry to remove..."
                )
                
                delete_button = st.form_submit_button("Delete Selected Entry", type="secondary")

                if delete_button and skill_to_delete_display:
                    entry_id = id_map[skill_to_delete_display]
                    
                    if delete_skill_entry(conn, entry_id):
                        st.success(f"Entry for **{skill_to_delete_display.split(' | ')[0]}** deleted successfully!")
                        st.rerun()

        else:
            st.info("No skill entries found yet. Use the form to add one!")

if __name__ == "__main__":
    main_ui()
