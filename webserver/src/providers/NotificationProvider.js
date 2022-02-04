import React, { useState } from "react";
import { NotificationContext } from "../contexts/NotificationContext";

function NotificationProvider({ children }) {
  const [userPermission, setPermission] = useState(null);

  let RequestPermission = () => {
    if (!("Notification" in window)) {
      console.log("This browser does not support desktop notification");
    } else {
      checkPermission();
    }
  };

  let checkPermission = () => {
    if (Notification.permission === "granted") {
      setPermission(true);
    }
    if (Notification.permission === "default") {
      Notification.requestPermission(function (perm) {
        if (perm === "granted") {
          setPermission(true);
        }
      });
    }
    if (Notification.permission === "denied") {
      setPermission(false);      
    }
  };

  let value = { userPermission, RequestPermission, checkPermission };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}

export default NotificationProvider;
