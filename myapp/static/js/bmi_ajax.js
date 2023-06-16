function calculateBMI() {
  // Get the height and weight from the user input
  let height = document.getElementById("height").value;
  let weight = document.getElementById("weight").value;
  // Calculate the BMI
  let bmi = weight / (height * height);
  // Display the BMI in the results div
  document.getElementById("results").innerHTML = bmi;
}
// // AJAX request
// function makeAJAXRequest() {
//   // Create a new XMLHttpRequest object
//   var xhr = new XMLHttpRequest();

//   // Define the request URL
//   var url = '/calculate_bmi/';  // Update with the correct URL for your Django view

//   // Define the request parameters
//   var params = 'weight=' + weightInput.value + '&height=' + heightInput.value;

//   // Configure the request
//   xhr.open('POST', url, true);
//   xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

//   // Define the callback function
// xhr.onload = function() {
//   if (xhr.status === 200) {
//     resultContainer.innerHTML = xhr.responseText; // Update the result container
//   } else {
//     resultContainer.innerHTML = 'Error: ' + xhr.statusText;
//   }
// };

//   // Send the request
//   xhr.send(params);
// }
