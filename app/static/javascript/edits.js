function handleEdit(button) {
    const table = button.getAttribute("data-table");
    const recordId = button.getAttribute("data-id");

    // Redirect to the edit_forms.html page with table and record ID as URL parameters
    window.location.href = `/edit_forms.html?table=${table}&id=${recordId}`;
}
