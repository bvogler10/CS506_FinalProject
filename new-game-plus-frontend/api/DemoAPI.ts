// For all different models, we should create a separate API declared as follows
const DemoAPI = {
    // This is a demo API function that sends a GET request to the server asynchronously
    demoGetRequest: async () => {
        // This is a fetch request to the server (hardcoded to localhost for now), with the method GET and the endpoint /demo/demo_get_request
        const response = await fetch(`http://127.0.0.1:8000/demo/demo_get_request`, {
            method: 'GET',
        });

        // We check if the response is ok to do error handling
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        
        // We parse the response to JSON
        const data = await response.json();

        // Return data.message since the server sends a JSON object with message as the key
        return data.message;
    }
}

// We export the API so that we can import it in other files
export default DemoAPI;