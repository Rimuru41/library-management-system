async function handleFines(button) {
    const action = button.textContent.trim();
    const fineId = button.dataset.fineId;
    const copyId=button.dataset.copyId;

    if (action === 'False') {
        Swal.fire({
            title: 'Are you sure?',
            text: 'Is fine paid for overdue?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, Paid it!',
            cancelButtonText: 'No, did not',
        }).then(async (result) => {
            if (result.isConfirmed) {
                button.textContent = 'True';

                const response = await fetch('/update_fines', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ fine_id:fineId, action: 'False' }),
                });

                const result = await response.json();

                if (result.success) {
                    Swal.fire('Success!', result.message, 'success');
                    button.textContent = 'True';
                    button.disabled = false;
                } else {
                    Swal.fire('Error!', result.message, 'error');
                    button.textContent = 'False';
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
