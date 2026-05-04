import streamlit as st
import requests
import os

BASE_URL = os.getenv("BACKEND_URL") 
st.set_page_config(page_title="To-Do App", layout="centered")
st.title("📝 The Best To-Do List Manager")

# ---------------------------
# Helper functions
# ---------------------------
def get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        return response.json()
    return []

def add_task(task):
    return requests.post(f"{BASE_URL}/addTask", json=task)

def update_task(task_id, task):
    return requests.put(f"{BASE_URL}/updateTask/{task_id}", json=task)
def delete_task(task_id):
    return requests.delete(f"{BASE_URL}/deleteTask/{task_id}")

# ---------------------------
# View Tasks
# ---------------------------
st.subheader("📋 Current Tasks")

tasks = get_tasks()

if tasks:
    for t in tasks:
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            st.write(f"**{t['task']}**")
            st.caption(t["description"])
        with col2:
            st.write("✅ Completed" if t["completed"] else "⏳ Pending")
        with col3:
            if st.button("❌", key=f"delete_{t['id']}"):
                delete_task(t["id"])
                st.rerun()
else:
    st.info("No tasks available")

# ---------------------------
# Add Task
# ---------------------------
st.divider()
st.subheader("➕ Add New Task")

with st.form("add_task_form"):
    task_id = st.number_input("Task ID", min_value=1, step=1)
    task_name = st.text_input("Task Name")
    task_desc = st.text_area("Description")
    completed = st.checkbox("Completed")

    submitted = st.form_submit_button("Add Task")

    if submitted:
        payload = {
            "id": task_id,
            "task": task_name,
            "description": task_desc,
            "completed": completed
        }
        add_task(payload)
        st.success("Task added successfully")
        st.rerun()

# ---------------------------
# Update Task
# ---------------------------
st.divider()
st.subheader("✏️ Update Task")

with st.form("update_task_form"):
    update_id = st.number_input("Task ID to Update", min_value=1, step=1)
    new_task = st.text_input("Updated Task Name")
    new_desc = st.text_area("Updated Description")
    new_completed = st.checkbox("Completed (Updated)")

    updated = st.form_submit_button("Update Task")

    if updated:
        payload = {
            "id": update_id,
            "task": new_task,
            "description": new_desc,
            "completed": new_completed
        }
        res = update_task(update_id, payload)
        if res.status_code == 200:
            st.success("Task updated successfully")
            st.rerun()
        else:
            st.error("Task not found")


# ---------------------------
# Delete Task
# ---------------------------
st.divider()
st.subheader("🗑 Delete Task")

with st.form("delete_task_form"):
    delete_id = st.number_input("Task ID to Delete", min_value=1, step=1)
    delete_submitted = st.form_submit_button("Delete Task")

    if delete_submitted:
        res = delete_task(delete_id)
        if res.status_code == 200:
            st.success("Task deleted successfully")
            st.rerun()
        else:
            st.error("Task not found")
