hideNotifications=() => {
  setTimeout(() => {
    const notification = document.getElementById('notification')
    if (notification) {
      setTimeout(() => {
        notification.style.display = 'none'
      }, 1000);
    }
  }, 5);
}

hideNotifications()