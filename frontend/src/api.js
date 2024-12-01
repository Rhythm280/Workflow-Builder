import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000',
});

export const triggerWorkflow = (workflowId, inputs) => {
    return api.post('/trigger-workflow', { workflowId, inputs });
};
