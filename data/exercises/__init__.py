from dataclasses import dataclass
from typing import Callable, List, Optional
import importlib
import pkgutil
import os

@dataclass
class Lesson:
    id: int
    title: str
    content: str
    example_code: str
    exercise_prompt: str
    validator: Callable[[str], tuple[bool, str]]
    hint: str
    type: str = "interactive"  # interactive | informational

@dataclass
class Module:
    id: int
    title: str
    lessons: List[Lesson]

def load_modules() -> List[Module]:
    modules = []
    # Dynamically load modules starting with 'module_'
    package_path = os.path.dirname(__file__)
    for _, name, _ in pkgutil.iter_modules([package_path]):
        if name.startswith("module_"):
            module = importlib.import_module(f"data.exercises.{name}")
            if hasattr(module, "MODULE"):
                modules.append(module.MODULE)
    
    # Sort by ID
    modules.sort(key=lambda m: m.id)
    return modules

def get_lesson_by_id(modules: List[Module], lesson_id: int) -> Optional[Lesson]:
    # Flattens the structure to find a lesson by absolute ID
    # This assumes lesson IDs are unique across the entire course
    for module in modules:
        for lesson in module.lessons:
            if lesson.id == lesson_id:
                return lesson
    return None

def get_next_lesson_id(modules: List[Module], current_lesson_id: int) -> Optional[int]:
    all_lessons = []
    for module in modules:
        all_lessons.extend(module.lessons)
    
    all_lessons.sort(key=lambda l: l.id)
    
    for i, lesson in enumerate(all_lessons):
        if lesson.id == current_lesson_id:
            if i + 1 < len(all_lessons):
                return all_lessons[i + 1].id
    return None
