this.addEventListener("push", (event) => {
  // TODO event.data can receive a json object to use as options
  if(!event.data){
    return "No data in message"
  }

  const message = event.data.json()

  const options = {
    body: message.title,
    icon: "images/ccard.png",
    vibrate: [200, 100, 200, 100, 200, 100, 400],
    tag: "request",
    actions: [
      { action: "yes", title: "Yes", icon: "images/yes.png" },
      { action: "no", title: "No", icon: "images/no.png" },
    ],
  };
  this.registration.showNotification(message.title, options);
});

this.addEventListener('notificationclick', function(event) {
  if (!event.action) {
    // Was a normal notification click
    console.log('Notification Click.');
    return;
  }

  switch (event.action) {
    case 'yes':
      console.log('User ❤️️\'s coffee.');
      break;
    case 'no':
      console.log('User ❤️️\'s doughnuts.');
      break;
    default:
      console.log(`Unknown action clicked: '${event.action}'`);
      break;
  }
});