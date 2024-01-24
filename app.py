import sqlite3
from enum import Enum, IntEnum
import streamlit as st
from pydantic import BaseModel, Field, ValidationError
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

def toggle_is_done(is_done, row):
    cur.execute(
        """
        UPDATE tasks SET is_done = ? WHERE id = ?
        """,
        (is_done, row[0]),
    )

# Function to update the task state
def update_task_state(state, row_id):
    cur.execute(
        """
        UPDATE tasks SET state = ? WHERE id = ?
        """,
        (state, row_id),
    )

def main():
    st.title("Todo App")
    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        cur.execute(
             """
            INSERT INTO tasks (name, description, created_at, created_by, category, state) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (data.name, data.description, data.created_at, data.created_by, data.category, data.state),
        )

    data = cur.execute(
        """
        SELECT * FROM tasks
        """
    ).fetchall()

    # HINT: how to implement a Edit button?
    # if st.query_params.get('id') == "123":
    #     st.write("Hello 123")
    #     st.markdown(
    #         f'<a target="_self" href="/" style="display: inline-block; padding: 6px 10px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 12px; border-radius: 4px;">Back</a>',
    #         unsafe_allow_html=True,
    #     )
    #     return

    cols = st.columns(3)
    cols[0].write("Done?")
    cols[1].write("Name")
    cols[2].write("Description")
    for row in data:
        cols = st.columns(3)
        # cols[0].checkbox('state', row[3], label_visibility='hidden', key=row[0], on_change=update_task_state, args=(not row[3], row))
        cols[0].radio('State', ['planned', 'in-progress', 'done'], index=['planned', 'in-progress', 'done'].index(task[3]), key=task[0])
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[2].markdown(
            f'<a target="_self" href="/?id=123" style="display: inline-block; padding: 6px 10px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 12px; border-radius: 4px;">Action Text on Button</a>',
            unsafe_allow_html=True,
        )
    #  Display tasks and allow state update through a selectbox


main()