from typing import List,Dict
class AgentResponse:
    """schema for the agent's response"""
    summary:str
    suspicious_ip:List[Dict]
    attack_pattern:str
    recommendations:List[str]
