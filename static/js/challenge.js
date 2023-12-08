let submissionForm = document.querySelector('#challenge-submission')

let correctRevealBox = document.querySelector('#correct-reveal')
let correctnessMessage = document.querySelector('#correctness-message')

submissionForm.addEventListener('submit', (event) => {
  event.preventDefault();
  
  let data = new FormData(submissionForm);
  
  fetch(submissionForm.action, {
    method: submissionForm.method,
    body: data
  })
    .then(response => response.json())
    .then((data) => {
      let isCorrect = data.is_correct;
      if (isCorrect) {
        correctnessMessage.textContent = 'Nicely done!';
      } else {
        correctnessMessage.textContent = 'That is incorrect.';
      }

      correctRevealBox.style.display = '';
    });
})