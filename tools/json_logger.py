import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from crewai.tools import BaseTool

class JSONLoggerTool(BaseTool):
    name: str = "JSON Logger Tool"
    description: str = "Logs user queries and responses to a JSON file"
    log_file_path: str = 'logs/user_queries.json'
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, log_file_path: str = 'logs/user_queries.json'):
        super().__init__()
        self.log_file_path = log_file_path
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        
        # Create empty JSON file if it doesn't exist
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as f:
                json.dump([], f)
    
    def _run(self, query: str, response: str = "", query_type: str = "user_query", session_id: Optional[str] = None) -> str:
        try:
            # Load existing logs
            with open(self.log_file_path, 'r') as f:
                logs = json.load(f)
            
            # Create new log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": response,
                "query_type": query_type,
                "session_id": session_id or self._get_session_id()
            }
            
            # Add to logs
            logs.append(log_entry)
            
            # Save back to file
            with open(self.log_file_path, 'w') as f:
                json.dump(logs, f, indent=2)
            
            print(f"Logged query: {query}")
            return f"Successfully logged query: {query}"
            
        except Exception as e:
            return f"Error logging to JSON: {e}"
    
    def _get_session_id(self) -> str:
        # Simple session ID based on current hour
        return datetime.now().strftime("%Y%m%d_%H")
    
    def get_recent_logs(self, limit: int = 10) -> list:
        try:
            with open(self.log_file_path, 'r') as f:
                logs = json.load(f)
            return logs[-limit:] if logs else []
        except:
            return []

    def get_session_logs(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            with open(self.log_file_path, 'r') as f:
                logs = json.load(f)
            session_logs = [log for log in logs if log.get("session_id") == session_id]
            return session_logs[-limit:] if session_logs else []
        except:
            return []