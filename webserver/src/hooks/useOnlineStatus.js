import React, { useState, useEffect, useContext, createContext } from "react";

const OnlineStatusContext = createContext(true);

export const OnlineStatusProvider = ({ children }) => {
  const [onlineStatus, setOnlinestatus] = useState(true);

  useEffect(() => {
    window.addEventListener("offline", () => {
      setOnlinestatus(false);
    });

    window.addEventListener("online", () => {
      setOnlinestatus(true);
    });

    return () => {
      window.removeEventListener("offline", () => {
        setOnlinestatus(false);
      });

      window.removeEventListener("online", () => {
        setOnlinestatus(true);
      });
    };
  }, []);

  return (
    <OnlineStatusContext.Provider value={onlineStatus}>
      {children}
    </OnlineStatusContext.Provider>
  );
};

export const useOnlineStatus = () => {
  const store = useContext(OnlineStatusContext);
  return store;
};
