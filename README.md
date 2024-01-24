# TECHIN 510 Lab 3

Data storage and retrieval using Python. Demonstrated with a To-Do list app.

## Getting Started

Open the terminal and run the following commands:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## What's Included
- `app.py`: The main streamlit application. Functions listed as follows:
    - Create new tasks
    - List the tasks
    - Search within tasks using the search bar
    - Filter dropdown for categorial field (State)
    - Update the state field of tasks
    - Delete tasks
    - Edit tasks
- `todoapp.sqlite`: stores the detailed todo task data.

- `lecture.ipynb`: The notes taken during the class on the usage of sqlite3 and SQL.

## Lessons Learned
- Syntaxes of SQL and the usage of sqlite3 to perform SQL command in Python
- Reinforces the usage on streamlit, and learned several new features, e.g. `st.columns([3,2,4,2,2])` can be used to create 5 columns with different width ratios; `st.markdown("&nbsp;")` can be used to generate a new blank line to increase the vertical space; and many other basic elements' implementation via streamlit such as button, selectbox, and text_input.
  

## Questions / Uncertainties

- It seems to be tricky if I want to move the form of creating new tasks to the bottom of the page and have the "Todos" be on the top. Because `data = sp.pydantic_form(key="task_form", model=Task)` not only renders the form but also give the `data` with value that needs to be used in writing the "Todos".