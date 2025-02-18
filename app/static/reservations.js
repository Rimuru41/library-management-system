
        function handleReservation(button) {
            if (button.textContent === 'Reserve') {
                if (confirm('Are you sure you want to reserve this book?')) {
                    button.textContent = 'Reservation Pending';
                    setTimeout(() => {
                        button.textContent = 'Issued';
                        button.disabled = true;
                    }, 2000);
                }
            } else if (button.textContent === 'Reservation Pending') {
                if (confirm('Do you want to cancel the reservation?')) {
                    button.textContent = 'Reserve';
                }
            }
        }
