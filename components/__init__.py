import os
import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "habit_auth")
_habit_auth_component = components.declare_component("habit_auth", path=build_dir)

def habit_auth(key=None, error=None, success=None):
    return _habit_auth_component(key=key, error=error, success=success, default=None)
