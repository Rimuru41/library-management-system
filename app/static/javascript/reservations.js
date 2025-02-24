async function handleReservation(button) {
    const action = button.textContent.trim();
    const bookId = button.dataset.bookId;

    if (action === 'Reserve') {
        Swal.fire({
            title: 'Are you sure?',
            text: 'Do you want to reserve this book?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, reserve it!',
            cancelButtonText: 'No, cancel',
        }).then(async (result) => {
            if (result.isConfirmed) {
                button.textContent = 'Reservation Pending';

                const response = await fetch('/reserve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ book_id: bookId, action: 'reserve' }),
                });

                const result = await response.json();

                if (result.success) {
                    Swal.fire('Success!', result.message, 'success');
                    button.textContent = 'Reservation Pending';
                    button.disabled = false;
                } else {
                    Swal.fire('Error!', result.message, 'error');
                    button.textContent = 'Reserve';
                }
            }
        });
    } else if (action === 'Not Available') {
        Swal.fire('Oops!', 'Sorry, the book is already reserved.', 'info');
    } else if (action === 'Reservation Pending') {
        Swal.fire({
            title: 'Cancel Reservation?',
            text: 'Are you sure you want to cancel this reservation?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, cancel it!',
            cancelButtonText: 'No, keep it',
        }).then(async (result) => {
            if (result.isConfirmed) {
                button.textContent = 'Reserve';

                const response = await fetch('/cancel_reserve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ book_id: bookId, action: 'cancel' }),
                });

                const result = await response.json();

                if (result.success) {
                    Swal.fire('Error!', result.message, 'error');
                    button.textContent = 'Reservation Pending';
                    button.disabled = false;
                } else {
                    Swal.fire('Cancelled!', result.message, 'success');
                    button.textContent = 'Reserve';
                }
            }
        });
    }
}
