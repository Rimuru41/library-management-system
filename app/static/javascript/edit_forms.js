document.addEventListener("DOMContentLoaded", function() {
    const params = new URLSearchParams(window.location.search);
    const table = params.get("table");
    const recordId = params.get("id");

    if (!table || !recordId) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Request',
            text: 'Missing table or ID!',
        });
        return;
    }

    // Fetch columns, constraints, and foreign keys from backend
    fetch(`/get_columns?table=${table}&id=${recordId}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: data.error,
            });
            return;
        }

        let formFields = document.getElementById("form-fields");
        formFields.innerHTML = "";

        let foreignKeys = data.foreign_keys || [];  // Get foreign key columns

        data.columns.forEach(column => {
            // Skip foreign key columns
            if (foreignKeys.includes(column)) {
                return;  
            }

            let inputGroup = document.createElement("div");
            inputGroup.classList.add("input-group");

            let label = document.createElement("label");
            label.textContent = column;
            label.setAttribute("for", column);

            if (data.constraints && data.constraints[column]) {
                // If column has constraints, create a dropdown
                let select = document.createElement("select");
                select.setAttribute("name", column);
                select.setAttribute("id", column);

                data.constraints[column].forEach(value => {
                    let option = document.createElement("option");
                    option.value = value;
                    option.textContent = value;
                    select.appendChild(option);
                });

                inputGroup.appendChild(label);
                inputGroup.appendChild(select);
            } else {
                // Otherwise, create a regular input field
                let input = document.createElement("input");
                input.setAttribute("type", "text");
                input.setAttribute("name", column);
                input.setAttribute("id", column);

                inputGroup.appendChild(label);
                inputGroup.appendChild(input);
            }

            formFields.appendChild(inputGroup);
        });
    })
    .catch(error => console.error("Error fetching columns:", error));


    // Handle form submission
    document.getElementById("edit-form").addEventListener("submit", function(event) {
        event.preventDefault();

        let formData = new FormData(this);
        let jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        fetch(`/edit_tables?table=${table}&id=${recordId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: data.success,
                    confirmButtonText: 'OK'
                }).then(() => {
                    window.location.href = data.redirect_url;
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.error,
                });
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Something went wrong!',
            });
            console.error("Error submitting form:", error);
        });
    });
});
