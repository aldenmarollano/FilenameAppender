// function fetchData() {
//     fetch('/path/to/your/view')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Handle successful response
//             console.log(data);
//         })
//         .catch(error => {
//             // Handle error response
//             alert('Error: ' + error.message);
//         });
// }

// // Call fetchData function
// fetchData();

// document.getElementById('formUpload').addEventListener('click', function() {
//     var form = document.getElementById('deleteButton');
//     form.method = 'POST';  // Change form method to POST
//     form.submit();  // Submit the form
// });