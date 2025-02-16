window.onload = function() {
    {% for category, message in messages %}
        let msg = {{ message|tojson }}; // Proper escaping
        alert(msg); // Or use a modal instead of alert
    {% endfor %}
};