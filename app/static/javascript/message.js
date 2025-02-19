document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("bookForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission
        
        let formData = new FormData(this);

        fetch("{{ url_for('main.add_book') }}", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: "Success",
                    text: data.message,
                    icon: "success",
                    confirmButtonText: "OK"
                }).then(() => {
                    window.location.href = data.redirect_url; // Redirect after alert
                });
            }
        })
        .catch(error => console.error("Error:", error));
    });
});