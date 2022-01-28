import React, { useState } from "react";

import {
  Box,
  Button,
  Typography,
  Modal,
  Backdrop,
  Fade,
  Card,
  Grid,
  Divider,
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import { ArrowRight } from "@mui/icons-material";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "./auth/useAuth";

const styles = {
  modal: {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    boxShadow: 24,
  },
  largeIcon: {
    width: 60,
    height: 60,
  },
};

export default function BasicModal({ open, handleClose, user }) {
  const [loading, setLoading] = useState(false);
  let navigate = useNavigate();
  let location = useLocation();
  let auth = useAuth();
  let from = location.state?.from?.pathname || "/";

  const handleClick = () => {
    setLoading(true);
  };

  const handleOffline = () => {
    auth.signin(user.username, "Offline", () => {
      navigate(from, { replace: true });
    });
  };

  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={open}>
          <Box sx={styles.modal}>
            <Card>
              <Box
                bgcolor="primary.dark"
                sx={{
                  pt: 1.2,
                  pl: 1.2,
                  pr: 4,
                  height: 50,
                }}
              >
                <Grid container justifyContent="center" alignItems="center">
                  <Grid item xs={11}>
                    <Typography variant="h5" color="primary.contrastText">
                      Could not connect to server
                    </Typography>
                  </Grid>
                </Grid>
              </Box>
              <Box sx={{ height: 100, p: 1.5 }}>
                <Typography>
                  Connect to the server has failed, you can start in
                  <strong> offline mode </strong>
                  to retreive saved logs or try to connect again.
                </Typography>
              </Box>
              <Divider variant="fullWidth" />

              <Grid container justifyContent="space-evenly">
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ borderRadius: 0 }}
                    onClick={handleOffline}
                  >
                    Offline mode
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <LoadingButton
                    fullWidth
                    variant="contained"
                    sx={{ borderRadius: 0 }}
                    onClick={handleClick}
                    endIcon={<ArrowRight />}
                    loading={loading}
                    loadingPosition="end"
                  >
                    Try again
                  </LoadingButton>
                </Grid>
              </Grid>
            </Card>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
