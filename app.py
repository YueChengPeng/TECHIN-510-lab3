import sqlite3
from enum import Enum, IntEnum
import streamlit as st
from pydantic import BaseModel, Field
import streamlit_pydantic as sp
from datetime import datetime

con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            description TEXT, 
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
            created_by TEXT, 
            category TEXT, 
            state TEXT
        )
    """
)

# Enum for Task State
class TaskState(str, Enum):
    PLANNED = '⏰ planned'
    IN_PROGRESS = '⭕️ in-progress'
    DONE = '✅ done'

# Enum for Task Category
class TaskCategory(str, Enum):
    SCHOOL = '🏫 school'
    WORK = '👨‍💻 work'
    PERSONAL = '🌙 personal'

class Task(BaseModel):
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str
    category: TaskCategory = TaskCategory.PERSONAL
    state: TaskState = TaskState.PLANNED

# Function to update the task state
def update_task_state(state, row_id):
    cur.execute(
        """
        UPDATE tasks SET state = ? WHERE id = ?
        """,
        (state, row_id),
    )

def main():
    st.title("Leo's Todo App")    
    data = sp.pydantic_form(key="task_form", model=Task)
    st.markdown("&nbsp;") # add vertical space
    if data:
        cur.execute(
             """
            INSERT INTO tasks (name, description, created_at, created_by, category, state) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (data.name, data.description, data.created_at, data.created_by, data.category, data.state),
        )
    
    st.header("Search & Filter")    

    search_filter_col = st.columns([1,1])
        
    # Search bar without a separate search button
    search_term = search_filter_col[0].text_input("Search in Name or Description, press Enter to search")

    query_search = ""
    params_search = ()

    # Fetch tasks based on search term or fetch all tasks
    if search_term: # if search term is not empty
        query_search = "SELECT * FROM tasks WHERE (name LIKE ? OR description LIKE ?)"
        params_search = ('%' + search_term + '%', '%' + search_term + '%')
    else: # if search term is empty
        query_search = "SELECT * FROM tasks"
        params_search = ()
    
    query_filter = ""
    params_filter = ()

    # State filter dropdown
    filter_state = search_filter_col[1].selectbox("Filter by State", ['Show all', '⏰ planned', '⭕️ in-progress', '✅ done'])
    if filter_state:  # if a state is selected for filtering
        if filter_state == 'Show all':
            query_filter = ""
            params_filter = ()
        else:
            if query_search == "SELECT * FROM tasks":
                query_filter = " WHERE state = ?"
                params_filter = (filter_state,)
            else:
                query_filter = " AND state = ?"
                params_filter = (filter_state,)

    # print(query_search + query_filter)
    # print(params_search+params_filter)
    data = cur.execute(query_search + query_filter, params_search+params_filter).fetchall() # after adding the search and filter query, fetch data from database

    # add vertical space
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")

    st.header("Todos")    

    # Display table headers
    cols = st.columns([3,2,4,2,2])
    cols[0].write("State")
    # cols[1].write("Category")
    cols[1].write("Name")
    cols[2].write("Description")
    cols[3].write("Options")
    # cols[4].write("Created At")
    # cols[5].write("Created By")

    # Function to delete a task
    def delete_task(task_id):
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    # Check if a task is being edited
    if 'editing_task_id' in st.session_state and st.session_state['editing_task_id'] is not None:
        edit_task_id = st.session_state['editing_task_id']
        # Fetch task details
        task_to_edit = cur.execute("SELECT * FROM tasks WHERE id = ?", (edit_task_id,)).fetchone()

        # Display form with task details for editing
        with st.form(key='edit_task'):
            edited_name = st.text_input("Name", value=task_to_edit[1])
            edited_description = st.text_area("Description", value=task_to_edit[2])
            submit_edit = st.form_submit_button("Update Task")

            if submit_edit:
                # Update task in database
                cur.execute("UPDATE tasks SET name = ?, description = ? WHERE id = ?", (edited_name, edited_description, edit_task_id))
                # Clear editing state
                st.session_state['editing_task_id'] = None
                st.experimental_rerun()

    for row in data:
        cols = st.columns([3,2,4,2,2])
        new_state = cols[0].selectbox('State', [state.value for state in TaskState], index=[state.value for state in TaskState].index(row[6]), key=f'state_{row[0]}', label_visibility="collapsed")
        if new_state != row[6]:
                cur.execute("UPDATE tasks SET state = ? WHERE id = ?", (new_state, row[0]))

        cols[1].write(row[1])
        cols[2].write(row[2])

        # Delete button
        if cols[3].button('Delete', key=f'delete_{row[0]}'):
            delete_task(row[0])
            st.experimental_rerun()

        # Edit button
        if cols[4].button('Edit', key=f'edit_{row[0]}'):
            # Store the id of the task to be edited
            st.session_state['editing_task_id'] = row[0]
            st.experimental_rerun()


    #  Display tasks and allow state update through a selectbox


main()