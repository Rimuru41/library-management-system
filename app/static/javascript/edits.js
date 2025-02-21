function handleEdit(button) {
    const table = button.getAttribute("data-table");
    const recordId = button.getAttribute("data-id");

    // Redirect to the edit_forms.html page with table and record ID as URL parameters
    window.location.href = `/edit_forms.html?table=${table}&id=${recordId}`;
}

function handleDelete(button) {
    const table = button.getAttribute("data-table");
    const recordId = button.getAttribute("data-id");
    const data = { table, recordId };

    Swal.fire({
        title: 'Are you sure?',
        text: 'Do you want to delete this?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel'
    }).then(async (result) => {
        if (result.isConfirmed) {
            // Optionally update the button text to indicate progress
            button.textContent = 'Removing...';

            try {
                const response = await fetch('/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const responseData = await response.json();

                if (responseData.success) {
                    // Show success message then refresh the page
                    Swal.fire('Success!', responseData.message, 'success')
                        .then(() => window.location.reload());
                } else {
                    Swal.fire('Error!', responseData.message, 'error');
                    button.textContent = 'Delete';
                }
            } catch (error) {
                Swal.fire('Error!', error.message, 'error');
                button.textContent = 'Delete';
            }
        }
    });
}
