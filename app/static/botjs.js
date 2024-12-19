Tawk_API = Tawk_API || {};

Tawk_API.onLoad = function() {
    console.log('Tawk.to widget loaded');
    Tawk_API.onMessageSent = function(message) {
        console.log('User sent a message:', message);

        fetch('https://fastapi-service-728413338172.us-central1.run.app/api/client/process-tawk-query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('API response:', data);

            Tawk_API.addMessage({
                text: data.response,
                type: 'system',
            });
        })
        .catch(error => console.error('Error:', error));
    };
};
