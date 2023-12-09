let submissionForm = document.querySelector('#challenge-submission');

let correctRevealBox = document.querySelector('#correct-reveal');
let correctnessMessage = document.querySelector('#correctness-message');

let showHintButton = document.querySelector('#show-hint-button');
let hintBox = document.querySelector('#hint-box');
let hintShown = false;

const hintDelay = 5;

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
      
      correctnessMessage.textContent = isCorrect ? 'Nicely done!' : 'That is incorrect.';

      if (isCorrect) {
        correctnessMessage.classList.remove('incorrect');
        correctnessMessage.classList.add('correct');
      } else {
        correctnessMessage.classList.remove('correct');
        correctnessMessage.classList.add('incorrect');
      }

      correctRevealBox.style.display = '';
    });
});

showHintButton.textContent = `Show hint (enabled after ${hintDelay} seconds)`;

setTimeout(() => {
  showHintButton.textContent = 'Show hint';
  showHintButton.disabled = false;
}, hintDelay * 1000);

showHintButton.addEventListener('click', () => {
  if (hintShown) {
    showHintButton.textContent = 'Show hint';
    hintBox.style.display = 'none';
  } else {
    showHintButton.textContent = 'Hide hint';
    hintBox.style.display = '';
  }

  hintShown = !hintShown;
});
