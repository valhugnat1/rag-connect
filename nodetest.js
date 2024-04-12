const axios = require("axios");

// Define the FastAPI server URL
const fastApiUrl = "http://127.0.0.1:8000/";

// Make a GET request to the FastAPI streaming endpoint
axios
  .get(fastApiUrl, { responseType: "stream" })
  .then((response) => {
    // Handle the streaming response
    response.data.on("data", (chunk) => {
      console.log(chunk.toString()); // Process each chunk of data
    });
    response.data.on("end", () => {
      console.log("Streaming ended");
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
