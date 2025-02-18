    // Select elements
    const filterButton = document.getElementById('filter-button');
    const filterModal = document.getElementById('filter-modal');
    const closeModal = document.getElementById('close-modal');
    const applyFilterButton = document.getElementById('apply-filter-button');

    // Show the modal when the filter button is clicked
    filterButton.addEventListener('click', () => {
      filterModal.style.display = 'flex'; // Use flex to align modal centrally
      document.body.style.overflow = 'hidden'; // Prevent background scrolling
    });

    // Hide the modal when the close button is clicked
    closeModal.addEventListener('click', () => {
      filterModal.style.display = 'none';
      document.body.style.overflow = 'auto'; // Restore scrolling when modal closes
    });


    // Optional: Hide the modal when clicking outside the modal content
    window.addEventListener('click', (event) => {
      if (event.target === filterModal) {
        filterModal.style.display = 'none';
      }
    });
  // Get the elements
  const yearOperator = document.getElementById('year-operator');
  const yearValue2 = document.getElementById('year-value-2');

  // Function to toggle visibility of year-value-2
  function toggleYearInputs() {
      if (yearOperator.value === 'BETWEEN') {
          yearValue2.style.display = 'inline'; // Show the second input
      } else {
          yearValue2.style.display = 'none'; // Hide the second input
      }
  }

  // Listen for changes to the year operator
  yearOperator.addEventListener('change', toggleYearInputs);

  // Call the function once to ensure the input is correctly displayed on page load
  toggleYearInputs();
 
    // Fetch genres from the API
async function fetchGenres() {
  try {
    const response = await fetch('/genres'); // Your backend route
    if (!response.ok) {
      throw new Error('Failed to fetch genres');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching genres:', error);
    return [];
  }
}

// Populate genres dynamically
async function populateGenres() {
  try {
    const genres = await fetchGenres();
    const genreOptions = document.getElementById('genre-options');
    genreOptions.innerHTML = ''; // Clear existing options

    genres.forEach((genre) => {
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = 'genres';
      checkbox.value = genre;
      checkbox.id = `genre-${genre}`; // Unique ID for label association

      const label = document.createElement('label');
      label.textContent = genre;
      label.setAttribute('for', checkbox.id); // Associate label with checkbox
      label.style.whiteSpace = 'nowrap'; // Prevents wrapping

      const wrapper = document.createElement('div'); // Wrap them to prevent misalignment
      wrapper.style.display = 'flex'; // Ensures elements stay in one line
      wrapper.style.alignItems = 'center'; // Aligns checkbox and text properly
      wrapper.style.gap = '8px'; // Adds spacing between text and checkbox

      wrapper.appendChild(label); // Append label first
      wrapper.appendChild(checkbox); // Append checkbox after label

      genreOptions.appendChild(wrapper);
    });
  } catch (error) {
    console.error('Error populating genres:', error);
  }
}

// Handle genre button click (MODIFIED)
const genreButton = document.getElementById('genre-btn');
const genreOptions = document.getElementById('genre-options');

let genresLoaded = false; // Prevent repeated fetching

genreButton.addEventListener('click', async () => {
  genreOptions.classList.toggle('hidden'); // Show/hide without resetting

  if (!genresLoaded) { 
    await populateGenres();  // Only fetch genres once
    genresLoaded = true; 
  }
});




document.getElementById('filter-form').addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent the form from reloading the page

  // Get the filter values
  const genres = [...document.querySelectorAll('input[name="genres"]:checked')].map(input => input.value);
  const yearOperator = document.getElementById('year-operator').value;
  const yearValue1 = document.getElementById('year-value-1').value;
  const yearValue2 = document.getElementById('year-value-2').value;
  const sortBy = document.getElementById('sort-by').value;
  const sortOrder = document.getElementById('sort-order').value;

  // Prepare the data for the backend
  const filterData = {
    genres,
    yearOperator,
    yearValue: yearOperator === 'BETWEEN' ? [yearValue1, yearValue2] : yearValue1,
    sortBy,
    sortOrder,
  };

  try {
    // Send a POST request to  backend
    const response = await fetch('/filter_books', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(filterData),
    });

    if (!response.ok) {
      throw new Error('Failed to apply filters');
    }

    // Get the filtered books
    const books = await response.json();

    // Update the book feed
    const bookFeed = document.getElementById('book-feed');
    bookFeed.innerHTML = ''; // Clear the book feed
    books.forEach((book) => {
      const bookCard = document.createElement('div');
      bookCard.className = 'book-card';
      bookCard.innerHTML = `
        <h3>${book.title}</h3>
        <p><strong>Author:</strong> ${book.author}</p>
        <p><strong>Genre:</strong> ${book.genre}</p>
        <p><strong>Year:</strong> ${book.year}</p>
      `;
      bookFeed.appendChild(bookCard);
    });
  } catch (error) {
    console.error('Error applying filters:', error);
  }
});

// Function to fetch and display all books
async function fetchAllBooks() {
  try {
    const response = await fetch('/get_books'); // Fetch all books from the backend
    if (!response.ok) {
      throw new Error('Failed to fetch all books');
    }

    const books = await response.json();

    // Populate the book feed with all books
    const bookFeed = document.getElementById('book-feed');
    bookFeed.innerHTML = ''; // Clear the book feed
    books.forEach((book) => {
      const bookCard = document.createElement('div');
      bookCard.className = 'book-card';
      bookCard.innerHTML = `
        <h3>${book.title}</h3>
        <p><strong>Author:</strong> ${book.author}</p>
        <p><strong>Genre:</strong> ${book.genre}</p>
        <p><strong>Year:</strong> ${book.year}</p>
      `;
      bookFeed.appendChild(bookCard);
    });
  } catch (error) {
    console.error('Error fetching all books:', error);
  }
}

// Fetch all books when the page loads
window.addEventListener('DOMContentLoaded', fetchAllBooks);


    

document.getElementById('reset-filters').addEventListener('click', () => {
  // Reset genres checkboxes
  const checkboxes = document.querySelectorAll('input[name="genres"]');
  checkboxes.forEach(checkbox => checkbox.checked = false);

  // Reset year filter inputs
  document.getElementById('year-operator').value = 'ANY';
  document.getElementById('year-value-1').value = '';
  document.getElementById('year-value-2').value = '';

  // Reset sort options
  document.getElementById('sort-by').value = 'title'; // Or whatever the default is
  document.getElementById('sort-order').value = 'asc'; // Or whatever the default is

  // Optionally, reset the genres dropdown visibility
  const genreOptions = document.getElementById('genre-options');
  genreOptions.classList.add('hidden'); // Hide the genre list if needed

  // Trigger the form submission or update the book feed after resetting
  fetchAllBooks(); // Or update the books based on reset filters
});


document.getElementById("search-bar").addEventListener("input", function() {
  let query = this.value.toLowerCase();
  let books = document.querySelectorAll(".book-card");

  books.forEach(function(book) {
      let title = book.querySelector("h3").textContent.toLowerCase();
      let author = book.querySelector("p strong").nextSibling.textContent.toLowerCase();
      let genre = book.querySelector("p:nth-of-type(2)").textContent.toLowerCase().replace("genre: ", ""); 
      let year = book.querySelector("p:nth-of-type(3)").textContent.toLowerCase().replace("year: ", ""); 

      if (title.includes(query) || author.includes(query) || genre.includes(query) || year.includes(query)) {
          book.style.display = "block"; // Show book if it matches
      } else {
          book.style.display = "none"; // Hide book if it doesn't match
      }
  });
});



