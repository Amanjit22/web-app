document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form submission

    let value1 = document.getElementById('value1').value;
    let value2 = document.getElementById('value2').value;

    // Basic validation
    if (!value1 || !value2) {
        alert("Both values are required!");
        return;
    }

    // Simulate form submission (log values to console for now)
    console.log("Submitted values:", value1, value2);

    // Reset form after submission
    document.getElementById('data-form').reset();
});
