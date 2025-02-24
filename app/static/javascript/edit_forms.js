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

            let checkbox = document.createElement("input");
            checkbox.setAttribute("type", "checkbox");
            checkbox.setAttribute("id", `${column}-checkbox`);
            checkbox.classList.add("column-checkbox");

            let label = document.createElement("label");
            label.textContent = column;
            label.setAttribute("for", column);

            let input;
            if (column.toLowerCase().includes("image")) {
                // If column contains "image", use file input
                input = document.createElement("input");
                input.setAttribute("type", "file");
                input.setAttribute("name", column);
                input.setAttribute("id", column);
                input.disabled = true; // Initially disabled
            } else if (column.toLowerCase().includes("year") || column.toLowerCase().includes("date")) {
                // If column contains "year" or "date", use date input
                input = document.createElement("input");
                input.setAttribute("type", "date");
                input.setAttribute("name", column);
                input.setAttribute("id", column);
                input.disabled = true; // Initially disabled
            } else if (data.constraints && data.constraints[column]) {
                // If column has constraints, create a dropdown
                input = document.createElement("select");
                input.setAttribute("name", column);
                input.setAttribute("id", column);
                input.disabled = true; // Initially disabled

                data.constraints[column].forEach(value => {
                    let option = document.createElement("option");
                    option.value = value;
                    option.textContent = value;
                    input.appendChild(option);
                });
            } else {
                // Otherwise, create a regular text input field
                input = document.createElement("input");
                input.setAttribute("type", "text");
                input.setAttribute("name", column);
                input.setAttribute("id", column);
                input.disabled = true; // Initially disabled
            }

            checkbox.addEventListener("change", function() {
                input.disabled = !checkbox.checked;
            });

            inputGroup.appendChild(checkbox);
            inputGroup.appendChild(label);
            inputGroup.appendChild(input);
            formFields.appendChild(inputGroup);
        });
    })
    .catch(error => console.error("Error fetching columns:", error));

    // Handle form submission
    document.getElementById("edit-form").addEventListener("submit", function(event) {
        event.preventDefault();

        let formData = new FormData();
        document.querySelectorAll(".column-checkbox:checked").forEach(checkbox => {
            let column = checkbox.id.replace("-checkbox", "");
            let input = document.getElementById(column);
            if (input) {
                if (input.type === "file" && input.files.length > 0) {
                    formData.append(column, input.files[0]); // Append file
                } else {
                    formData.append(column, input.value);
                }
            }
        });

        fetch(`/edit_tables?table=${table}&id=${recordId}`, {
            method: "POST",
            body: formData // Send FormData for file support
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
