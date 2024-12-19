Tawk_API = Tawk_API || {};

Tawk_API.onLoad = function () {
  console.log("Tawk.to widget loaded");
  Tawk_API.onChatMessageVisitor = function (message) {
    console.log("User sent a message:", message);

    fetch(
      "https://fastapi-service-728413338172.us-central1.run.app/api/client/process-tawk-query",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          message: message["message"],
        }),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("API response:", data);
        let response = data["response"];
        console.log("Bot response:", response);
      })
      .catch((error) => console.error("Error:", error));
  };
};
