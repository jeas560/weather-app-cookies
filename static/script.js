hideNotifications=() => {
  setTimeout(() => {
    const gelmao = document.getElementById('notification')
    if (gelmao) {
      setTimeout(() => {
        gelmao.style.display = 'none'
      }, 3000);
    }
  }, 10);
}

hideNotifications()