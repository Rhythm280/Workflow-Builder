import axios from 'axios';

export const saveWorkflow = (workflow) => {
    return axios.post('http://127.0.0.1:5000/api/save-workflow', workflow);
};

export const getWorkflows = () => {
    return axios.get('http://127.0.0.1:5000/api/get-workflows');
};
