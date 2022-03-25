import { LockOutlined } from "@mui/icons-material";
import {
  Avatar,
  Box,
  Button,
  Container,
  CssBaseline,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthService from "../services/auth.service";
import { useAuth } from "../hooks/useAuth";
import eventBus from "../services/EventBus";
import { useNotification } from "../hooks/useNotification";

function SignupForm() {
  let navigate = useNavigate();
  let auth = useAuth();
  let notification = useNotification();
  const [form, setForm] = useState({
    signupCode: "",
    username: "",
    password: "",
  });

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await AuthService.signup(
        form.username,
        form.password,
        form.signupCode
      ).then(
        (response) => {
          // check for token and user already exists with 200
          console.log("Sign up successfully", response);
          doLogin();
        },
        (error) => {
          console.log(error.response.data);
        }
      );
    } catch (err) {
      console.log(err);
    }
  };

  const doLogin = async () => {
    try {
      await AuthService.login(form.username, form.password).then(
        (response) => {
          auth.signin(
            form.username,
            response.userID,
            response.accessToken,
            () => {
              notification.RequestPermission();
              navigate("/", { replace: true });
              eventBus.dispatch("login", {});
            }
          );
        },
        (error) => {
          console.log(error);
        }
      );
    } catch (err) {
      console.log(err);
    }
  };

  return (
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
          Sign up
        </Typography>
        <Box component="form" noValidate sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Signup code"
                name="signupCode"
                value={form.signupCode}
                onChange={handleChange}
                autoComplete="family-name"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                value={form.username}
                onChange={handleChange}
                autoComplete="username"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                value={form.password}
                onChange={handleChange}
                autoComplete="new-password"
              />
            </Grid>
          </Grid>
          <Button
            type="button"
            fullWidth
            onClick={handleSubmit}
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign Up
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link to="/login" variant="body2">
                Already have an account? Sign in
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}

export default SignupForm;
