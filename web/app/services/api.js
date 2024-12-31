export class API {
    hostname = "http://localhost:8080/"

    // Destroy methods
    static Login(username, password, viewtype) {
        const data = { 
            username: username,
            password: password,
            viewtype: viewtype,
        };
        fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log("API RSULT:")
            console.log(data)
            // document.getElementById("post-result").innerText = JSON.stringify(data);
            return data;
        })
        .catch(error => {
            console.error("Error with POST request:", error);
        });
    }

}