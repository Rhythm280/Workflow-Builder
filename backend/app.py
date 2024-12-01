from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
import requests

app = Flask(__name__)
CORS(app)  # This will allow all origins (for testing purposes)

# Simulate database for workflows
workflows = []

# Root route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Workflow Builder API!"})


@app.route('/api/save-workflow', methods=['POST'])
def save_workflow():
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    workflows.append(data)
    print("Current Workflows:", workflows)  # Print stored workflows to the console
    return jsonify({'message': 'Workflow saved successfully!'}), 200

@app.route('/api/debug-workflows', methods=['GET'])
def debug_workflows():
    return jsonify(workflows), 200


@app.route('/api/get-workflows', methods=['GET'])
def get_workflows():
    return jsonify(workflows), 200

@app.route('/api/kestra-trigger', methods=['POST'])
def kestra_trigger():
    data = request.json
    print(f"Received Trigger Request: {data}")
    
    if not data or 'namespace' not in data or 'flowId' not in data:
        return jsonify({"message": "Missing required fields: namespace or flowId"}), 400
    
    # Trigger the workflow
    payload = {
        "namespace": data['namespace'],
        "flowId": data['flowId']
    }

    # Call Kestra API to trigger the workflow
    url = f"http://localhost:8080/api/v1/flows/{data['namespace']}/{data['flowId']}/start"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return jsonify({"message": "Workflow triggered successfully", "data": response.json()}), 200
    else:
        return jsonify({"message": "Failed to trigger workflow", "error": response.json()}), response.status_code



def convert_to_kestra_workflow(data):
    # Use a simpler task like ScriptTask or another basic task
    workflow = {
        "id": data["name"].lower().replace(" ", "-"),
        "namespace": "examples",
        "tasks": [
            {
                "id": "example-task",
                "type": "io.kestra.core.tasks.scripts.ScriptTask",  # A valid, basic task
                "script": f"echo {data['description']}"  # A simple script
            }
        ]
    }
    return yaml.dump(workflow, default_flow_style=False)


def submit_workflow_to_kestra(yaml_string):
    """Submit a workflow to the Kestra server."""
    url = "http://localhost:8080/api/v1/flows"
    headers = {"Content-Type": "application/x-yaml"}
    try:
        response = requests.post(url, headers=headers, data=yaml_string)
        if response.status_code in [200, 201]:
            return {"success": True}
        else:
            return {"success": False, "details": response.text}
    except Exception as e:
        return {"success": False, "details": str(e)}

def trigger_workflow(namespace, flow_id):
    """Trigger a workflow execution in Kestra."""
    url = "http://localhost:8080/api/v1/executions"
    payload = {
        "namespace": namespace,
        "flowId": flow_id
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return {"success": True, "execution": response.json()}
        else:
            return {"success": False, "details": response.text}
    except Exception as e:
        return {"success": False, "details": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
