import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n¡Hasta luego!")
        sys.exit(0)
