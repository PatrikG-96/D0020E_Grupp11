import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./useAuth";

function AuthStatus() {
  let auth = useAuth();
  let navigate = useNavigate();

  if (!auth.user) {
    return <p>You are not logged in</p>;
  }

  return (
    <p>
      Welcome {auth.user.username + " | Session id: " + auth.user.sid}
      <button
        onClick={() => {
          auth.signout(() => {
            navigate("/login");
          });
        }}
      >
        Sign out
      </button>
    </p>
  );
}

export default AuthStatus;
