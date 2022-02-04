import React, { useState } from "react";
import { AuthContext } from "../contexts/AuthContext";

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  let signin = (username, userID, token, callback) => {
    setUser({
      username: username,
      userID: userID,
      //Add user details insted of token as it is in localStorage
      userToken: token,
    });

    callback();
  };

  let signout = (callback) => {
    setUser(null);
    callback();
  };

  let value = { user, signin, signout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
