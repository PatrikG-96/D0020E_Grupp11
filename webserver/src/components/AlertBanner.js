import { Close } from "@mui/icons-material";
import { Alert, AlertTitle, Box, Collapse, IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useOnlineStatus } from "../hooks/useOnlineStatus";

function AlertBanner({title, message, severity }) {
  const [open, setOpen] = useState();
  const onlineStatus = useOnlineStatus();

  useEffect(() => {
    setOpen(!onlineStatus);
  }, [onlineStatus]);

  return (
    <Box sx={{ width: "100%" }} spacing={2}>
      <Collapse in={open}>
        <Alert
          severity={severity}
          action={
            <IconButton
              onClick={() => {
                setOpen(false);
              }}
            >
              <Close />
            </IconButton>
          }
        >
          <AlertTitle>{title}</AlertTitle>
          {message}
        </Alert>
      </Collapse>
    </Box>
  );
}

export default AlertBanner;
