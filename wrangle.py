import json

def get_session_id():
    session_log_path = "data/session_log.json"
    
    try:
        with open(session_log_path, 'r', encoding='utf-8') as file:
            session_data = json.load(file)
            return session_data["dialogue_segments"][2]["modality"]
    except FileNotFoundError:
        return "Error: Session log file not found"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format in session log"
    except KeyError:
        return "Error: No session_id found in session log"
    

id = get_session_id()
print(id)