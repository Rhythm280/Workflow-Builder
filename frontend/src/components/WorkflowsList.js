import React, { useState } from 'react';
import axios from 'axios';

const DragDropCanvas = () => {
    const [workflowName, setWorkflowName] = useState('');
    const [description, setDescription] = useState('');
    const [elements, setElements] = useState([]);

    const handleDrop = (event) => {
        event.preventDefault();
        const newElement = { id: Date.now(), name: 'New Step' };
        setElements([...elements, newElement]);
    };

    const saveWorkflow = async () => {
        try {
            const workflow = {
                name: workflowName,
                description: description,
                elements: elements,
            };
            const response = await axios.post('http://127.0.0.1:5000/api/save-workflow', workflow);
            alert(response.data.message);
        } catch (error) {
            console.error('Error saving workflow:', error);
        }
    };

    const executeWorkflow = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/execute-workflow', {
                name: workflowName,
                description: description,
                elements: elements,
            });
            alert(`Execution started: ${response.data.id}`);
        } catch (error) {
            console.error('Error executing workflow:', error);
        }
    };


    return (
        <div>
            <input
                type="text"
                placeholder="Workflow Name"
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
            />
            <input
                type="text"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <div
                style={{ border: '1px solid black', width: '400px', height: '200px', margin: '20px' }}
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
            >
                {elements.map((el) => (
                    <div key={el.id}>{el.name}</div>
                ))}
            </div>
            <button onClick={saveWorkflow}>Save Workflow</button>
            <button onClick={executeWorkflow}>Execute Workflow</button>
        </div>
    );
};

export default DragDropCanvas;
