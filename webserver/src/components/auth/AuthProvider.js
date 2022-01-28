import React, { useState } from "react";
import { AuthContext } from "../../context/AuthContext";

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

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

  let value = { user, signin, signout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
