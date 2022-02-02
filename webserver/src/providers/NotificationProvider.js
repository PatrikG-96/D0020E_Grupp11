import React, { useEffect, useState } from "react";
import { NotificationContext } from "../contexts/NotificationContext";

function NotificationProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    if(!("Notification" in window)) {
        console.log("This browser does not support desktop notification");
    }else {
        console.log("Notifications are supported");
        Notification.requestPermission();
    }
  }, []);

  let showNotification = (message) => {
      new Notification(message)
  }

  let signin = (username, token, callback) => {
    setUser({
      username: username,
      //Add user details insted of token as it is in localStorage
      userToken: token,
    });

    callback();
  };

  let signout = (callback) => {
    setUser(null);
    callback();
  };

  let value = { user, signin, signout, showNotification };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}

export default NotificationProvider;
