import {
  Avatar,
  Box,
  Button,
  Checkbox,
  Container,
  CssBaseline,
  FormControlLabel,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import { LockOutlined } from "@mui/icons-material";
import React, { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import BasicModal from "./Modal";
import AuthService from "../services/auth.service";
import { useNotification } from "../hooks/useNotification";
import eventBus from "../EventBus";
import { useOnlineStatus } from "../hooks/useOnlineStatus";

function LoginForm() {
  let navigate = useNavigate();
  let location = useLocation();
  let auth = useAuth();
  let notification = useNotification();
  let from = location.state?.from?.pathname || "/";

  const [form, setForm] = useState({ username: "", password: "" });
  const [openModal, setOpenModal] = useState(false);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await AuthService.login(form.username, form.password).then(
        (response) => {
          if (checked) {
            localStorage.setItem("savedUser", form.username);
          }

          auth.signin(
            form.username,
            response.userID,
            response.accessToken,
            () => {
              notification.RequestPermission();
              navigate(from, { replace: true });
              eventBus.dispatch("login", {});
            }
          );
        },
        (error) => {
          console.log(error);
          handleOpen();
        }
      );
    } catch (err) {
      console.log(err);
    }
  };

  const handleOpen = () => setOpenModal(true);
  const handleClose = () => setOpenModal(false);

  const [checked, setChecked] = useState(false);

  const handleChecked = (event) => {
    setChecked(event.target.checked);
  };

  return (
    <Container>
      <BasicModal open={openModal} handleClose={handleClose} user={form} />
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlined />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              name="username"
              value={form.username}
              onChange={handleChange}
              label="Username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              type="password"
              label="Password"
              name="password"
              value={form.password}
              onChange={handleChange}
              autoComplete="current-password"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={checked}
                  onChange={handleChecked}
                  color="primary"
                />
              }
              label="Remember me"
            />
            <Button
              type="button"
              fullWidth
              variant="contained"
              onClick={handleSubmit}
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                {/* TODO Change the link styling to not clicked*/}
                <Link to="forgot" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link to="/signup" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </Container>
  );
}

export default LoginForm;
