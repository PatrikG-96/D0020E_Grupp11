import React from "react";
import AlertBanner from "../components/AlertBanner";
import LoginForm from "../components/LoginForm";

function Login() {

  return (
    <div>
      <AlertBanner title="Warning" message="You are offline, some functionality will be disabled" severity="warning" />
      <LoginForm />;
    </div>
  );
}

export default Login;
