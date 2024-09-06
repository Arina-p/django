document.addEventListener('DOMContentLoaded', () => {
    const currentUrl = window.location.pathname; // Получаем текущий URL
    const navLinks = document.querySelectorAll('.navlist a');
  
    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentUrl) {
        link.classList.add('active'); // Добавляем класс 'active' к активной ссылке
      }
    });
  });