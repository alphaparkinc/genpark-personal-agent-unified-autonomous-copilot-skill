from client import PersonalAgentUnifiedCopilot
import json

copilot = PersonalAgentUnifiedCopilot()
print("=== PERSONAL AGENT UNIFIED MASTER COPILOT BENCHMARK ===")
res = copilot.run_unified_copilot_benchmark()
print(json.dumps(res, indent=2))
