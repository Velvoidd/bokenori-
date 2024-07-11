var modalBtns = document.querySelectorAll('.delete-button');
var modals = document.querySelectorAll('.modal');
var spans = document.querySelectorAll('.close');

modalBtns.forEach(function(btn, index) {
    btn.onclick = function() {
        modals[index].style.display = "block";
    }
});

spans.forEach(function(span, index) {
    span.onclick = function() {
        modals[index].style.display = "none";
    }
});

window.onclick = function(event) {
    modals.forEach(function(modal) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
}



document.addEventListener("DOMContentLoaded", function() {
  const container = document.getElementById('sakura-container');

  function createPetal() {
    const petal = document.createElement('div');
    petal.className = 'sakura-petal';
    container.appendChild(petal);

    const startPosition = Math.random() * window.innerWidth;
    petal.style.left = startPosition + 'px';

    const animationDuration = Math.random() * 6 + 5; // Случайная длительность анимации
    const animationDelay = Math.random() * 6; // Случайная задержка перед анимацией

    petal.style.animationDuration = animationDuration + 's';
    petal.style.animationDelay = animationDelay + 's';

    petal.addEventListener('animationend', function() {
      container.removeChild(petal); // Удаляем лепесток после окончания анимации
    });
  }

  setInterval(createPetal, 500); // Создаем новый лепесток каждые 500 миллисекунд
});
