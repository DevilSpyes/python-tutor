import json
import os
from dataclasses import dataclass

STATE_FILE = "user_progress.json"

@dataclass
class UserState:
    current_lesson_id: int
    completed_lessons: list[int]

def load_state() -> UserState:
    if not os.path.exists(STATE_FILE):
        return UserState(current_lesson_id=1, completed_lessons=[])
    
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            return UserState(
                current_lesson_id=data.get("current_lesson_id", 1),
                completed_lessons=data.get("completed_lessons", [])
            )
    except json.JSONDecodeError:
        return UserState(current_lesson_id=1, completed_lessons=[])

def save_state(state: UserState):
    data = {
        "current_lesson_id": state.current_lesson_id,
        "completed_lessons": state.completed_lessons
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def mark_lesson_complete(lesson_id: int, next_lesson_id: int = None):
    state = load_state()
    if lesson_id not in state.completed_lessons:
        state.completed_lessons.append(lesson_id)
    
    # Advance to next lesson if we just completed the current one
    if lesson_id == state.current_lesson_id and next_lesson_id:
        state.current_lesson_id = next_lesson_id
        
    save_state(state)
