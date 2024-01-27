let submissionForm = document.querySelector('#challenge-submission');

let correctRevealBox = document.querySelector('#correct-reveal');
let correctnessMessage = document.querySelector('#correctness-message');

let showHintButton = document.querySelector('#show-hint-button');
let hintBox = document.querySelector('#hint-box');
let hintShown = false;

const hintDelay = 60;

submissionForm.addEventListener('submit', (event) => {
  event.preventDefault();
  
  let formData = new FormData(submissionForm);
  
  fetch(submissionForm.action, {
    method: submissionForm.method,
    body: formData
  })
    .then(response => response.json())
    .then((data) => {
      let isCorrect = data.is_correct;
      
      correctnessMessage.textContent = isCorrect ? 'Nicely done! Challenge marked as complete.' : `"${formData.get('submission')}" is incorrect.`;

      if (isCorrect) {
        challengeIsCompleted = 1;
        
        correctnessMessage.classList.remove('incorrect');
        correctnessMessage.classList.add('correct');

        document.querySelectorAll('.challenge-link')[challengeNum - 1].classList.add('completed');

        document.querySelector('#score-number-end-statement').style.display = '';
      } else {
        correctnessMessage.classList.remove('correct');
        correctnessMessage.classList.add('incorrect');
      }

      if (!challengeIsCompleted) {
        scoreNumberElt = document.querySelector('#score-number-text');
        scoreNumberElt.textContent ++;
        document.querySelector('#score-number-pluralize').textContent = scoreNumberElt.textContent === '1' ? '' : 's';
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
