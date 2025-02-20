document.addEventListener("DOMContentLoaded", function () {
    // Ensure modal is hidden when the page loads
    document.getElementById("myModal").style.display = "none";
});

// Function to show the modal
function showModal(button) {
    const modal = document.getElementById("myModal");
    const modalContent = document.querySelector(".modal-content"); 
    const bookId = button.getAttribute("data-book-id");

    // Store book ID or do something with it
    document.getElementById("addBookCopyForm").onsubmit = function(event) {
        event.preventDefault();
        const status = document.getElementById("bookStatus").value;
        const condition = document.getElementById("bookCondition").value;

        // Example: Send data to the backend via fetch
        fetch("/add_books_copies", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                book_id: bookId,
                status: status,
                condition: condition
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire("Success", "Book Copy Added Successfully!", "success");
            } else {
                Swal.fire("Error", "Failed to add book copy!", "error");
            }
        });
        closeModal();  // Close the modal after submission
    };

    // Make sure modal opens in the center
    modal.style.display = "flex";
    modalContent.style.transform = "scale(1)";  // Smooth transition effect
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById("myModal");
    const modalContent = document.querySelector(".modal-content"); 

    modalContent.style.transform = "scale(0.9)"; // Shrink effect before closing
    setTimeout(() => {
        modal.style.display = "none";
    }, 200); // Delay to match animation
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById("myModal");
    if (event.target === modal) {
        closeModal();
    }
};
