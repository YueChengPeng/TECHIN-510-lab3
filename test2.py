from enum import Enum
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from pydantic import BaseModel, Field
from streamlit_pydantic import pydantic_form
from typing import Optional

# Database setup
conn = sqlite3.connect('tasks.db', check_same_thread=False)
c = conn.cursor()

# Enum for Task State
class TaskState(str, Enum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'

# Enum for Task Category
class TaskCategory(str, Enum):
    SCHOOL = 'school'
    WORK = 'work'
    PERSONAL = 'personal'

# Create table
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            description TEXT, 
            created_at DATETIME, 
            created_by TEXT, 
            category TEXT, 
            state TEXT
        )
    ''')

create_table()

# Pydantic model
class Task(BaseModel):
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str
    category: str
    state: str

# # Add a task to the database
# def add_task(task_data):
#     with conn:
#         c.execute('''
#             INSERT INTO tasks (name, description, created_at, created_by, category, state) 
#             VALUES (:name, :description, :created_at, :created_by, :category, :state)
#         ''', task_data.dict())

# # Update task state
# def update_task_state(task_id, new_state):
#     with conn:
#         c.execute('UPDATE tasks SET state = ? WHERE id = ?', (new_state, task_id))

# # Delete task
# def delete_task(task_id):
#     with conn:
#         c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

# # Streamlit UI
# st.title("Todo Task Manager")

# with pydantic_form(key='form', model=Task):
#     task_data = st.form_submit_button("Submit")

# if task_data:
#     add_task(task_data)
#     st.success("Task added successfully!")

# # Display tasks
# st.subheader("Tasks")
# for row in c.execute('SELECT id, name, description, state FROM tasks'):
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.text(f"Name: {row[1]}\nDescription: {row[2]}\nState: {row[3]}")
#     with col2:
#         if st.button("Done", key=row[0]):
#             update_task_state(row[0], "done")
#         if st.button("Delete", key=f"del{row[0]}"):
#             delete_task(row[0])

# # Optional: Add search and filter functionality here

# # Keep the connection open
# st.experimental_rerun()