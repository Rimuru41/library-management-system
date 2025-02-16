document.getElementById("bookForm").addEventListener("submit", function(event) {
    var isbnInput = document.getElementById("ISBN");
    var isbnError = document.getElementById("isbnError");
    var isbnValue = isbnInput.value.trim();

    // Check if ISBN is exactly 13 digits and contains only numbers
    if (!/^\d{13}$/.test(isbnValue)) {
        event.preventDefault(); // Prevent form submission
        isbnError.style.display = "block"; // Show error message
        isbnInput.style.border = "1px solid red"; // Highlight the input
    } else {
        isbnError.style.display = "none"; // Hide error message
        isbnInput.style.border = "1px solid #ccc"; // Reset input border
    }
});

var pagesInput = document.getElementById("Pages");
var pagesValue = pagesInput.value.trim();

if (!/^\d+$/.test(pagesValue) || parseInt(pagesValue, 10) <= 0) {
    event.preventDefault();
    alert("Pages must be a positive integer greater than zero.");
    pagesInput.style.border = "1px solid red";
} else {
    pagesInput.style.border = "1px solid #ccc";
}
