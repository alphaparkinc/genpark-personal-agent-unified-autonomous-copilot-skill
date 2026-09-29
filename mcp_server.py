import sys, json
from client import PersonalAgentUnifiedCopilot

def handle_mcp():
    copilot = PersonalAgentUnifiedCopilot()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(copilot.run_unified_copilot_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-personal-agent-unified-autonomous-copilot-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "process_personal_request", "description": "Execute master personal agent cognitive pipeline.", "inputSchema": {"type": "object", "properties": {"user_command": {"type": "string"}, "ambient_context": {"type": "object"}}}},
                    {"name": "get_copilot_telemetry", "description": "Get status of all 5 personal agent engines.", "inputSchema": {"type": "object"}},
                    {"name": "run_unified_copilot_benchmark", "description": "Run unified personal copilot benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "process_personal_request":
                    res = copilot.process_personal_request(args.get("user_command", ""), args.get("ambient_context"))
                elif tname == "get_copilot_telemetry":
                    res = copilot.get_copilot_telemetry()
                else:
                    res = copilot.run_unified_copilot_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
