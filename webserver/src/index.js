import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthProvider from "./components/auth/AuthProvider.js";
import RequireAuth from "./components/auth/RequireAuth.js";
import Home from "./pages/Home.js";
import Login from "./pages/Login.js";
import NoMatch from "./pages/NoMatch.js";
import { ThemeProvider } from "@mui/material/styles";
import { themeOptions } from "./theme.js";
import Log from "./pages/Log.js";
import Alarm from "./pages/Alarm.js";
import Elders from "./pages/Elders.js";
import LoginForm from "./components/LoginForm.js";
import SignupForm from "./components/SignupForm.js";

const App = () => {
  return (
    <ThemeProvider theme={themeOptions}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route
              path="/"
              element={
                <RequireAuth>
                  <Home />
                </RequireAuth>
              }
            >
              <Route path="log" element={<Log />} />
              <Route path="alarm" element={<Alarm />} />
              <Route path="elders" element={<Elders />} />
            </Route>

            <Route path="login" element={<LoginForm />}>
              <Route path="forgot" element={<></>} />
            </Route>
            <Route path="signup" element={<SignupForm />} />
            <Route path="*" element={<NoMatch />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));
