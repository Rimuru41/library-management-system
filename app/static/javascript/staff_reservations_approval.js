async function handleReservation(button) {
    const action = button.textContent.trim();
    const memberId = button.dataset.memberId;
    const copyId=button.dataset.copyId;

    if (action === 'Pending') {
        Swal.fire({
            title: 'Are you sure?',
            text: 'Do you want to confirm for issuing this book?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, issue it!',
            cancelButtonText: 'No, cancel',
        }).then(async (result) => {
            if (result.isConfirmed) {
                button.textContent = 'Issued';

                const response = await fetch('/Issue_book', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ member_id:memberId, copy_id:copyId, action: 'Pending' }),
                });

                const result = await response.json();

                if (result.success) {
                    Swal.fire('Success!', result.message, 'success');
                    button.textContent = 'Issued';
                    button.disabled = false;
                } else {
                    Swal.fire('Error!', result.message, 'error');
                    button.textContent = 'Pending';
                }
            }
        });
    } else if (action === 'Not Available') {
        Swal.fire('Oops!', 'Sorry, the book is already reserved.', 'info');
    } else if (action.toLowerCase() === 'issued') {
        Swal.fire({
            title: 'Return book?',
            text: 'Are you sure you want to return this book?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, return it!',
            cancelButtonText: 'No, keep it',
        }).then(async (result) => {
            if (result.isConfirmed) {
                button.textContent = 'Returned';

                const response = await fetch('/return_issued_book', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ member_id:memberId, copy_id:copyId, action: 'Pending' }),
                });

                const result = await response.json();

                if (result.success) {
                    Swal.fire('success!', result.message, 'success');
                    button.textContent = 'Returned';
                    button.disabled = false;
                } else {
                    Swal.fire('Cancelled!', result.message, 'success');
                    button.textContent = 'Issued';
                }
            }
        });
    }
}
