document.getElementById("loanForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    
    let formData = new FormData(this);
    let jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = Number(value);  // Convert inputs to numbers
    });

    document.getElementById("result").classList.add("d-none");
    document.getElementById("result").textContent = "Processing...";

    try {
        let response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData),
        });

        let data = await response.json();
        let resultDiv = document.getElementById("result");

        resultDiv.textContent = data.prediction;
        resultDiv.classList.remove("d-none");

        if (data.prediction === "Approved") {
            resultDiv.classList.add("alert", "alert-success");
        } else {
            resultDiv.classList.add("alert", "alert-danger");
        }
    } catch (error) {
        alert("Error connecting to the server. Please try again.");
    }
});
