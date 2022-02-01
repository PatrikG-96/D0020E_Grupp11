import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth.service";
import { useAuth } from "./auth/useAuth";

function Logout() {
  const auth = useAuth();
  const navigate = useNavigate();

    useEffect(() => {
      
        auth.signout(() => {
            AuthService.logout();
            navigate("/", { replace: true})
        })

    }, []);
    

  return <div></div>;
}

export default Logout;
