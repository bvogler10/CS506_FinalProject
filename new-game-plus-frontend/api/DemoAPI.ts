const DemoAPI = {
    demoGetRequest: async () => {
        const response = await fetch(`http://127.0.0.1:8000/demo/demo_get_request`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }
        
        const data = await response.json();

        return data.message;
    }
}

export default DemoAPI;