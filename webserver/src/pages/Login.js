import { Close } from "@mui/icons-material";
import { Alert, AlertTitle, Collapse, IconButton } from "@mui/material";
import { Box } from "@mui/system";
import React, { useEffect, useState } from "react";
import AlertBanner from "../components/AlertBanner";
import LoginForm from "../components/LoginForm";
import { useOnlineStatus } from "../hooks/useOnlineStatus";

function Login() {
  const [open, setOpen] = useState();
  const onlineStatus = useOnlineStatus();

  useEffect(() => {
    setOpen(!onlineStatus);
  }, [onlineStatus]);

  return (
    <div>
      <AlertBanner title="Warning" message="You are offline, some functionality will be disabled" severity="warning" />
      <LoginForm />;
    </div>
  );
}

export default Login;
