import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthProvider from "./providers/AuthProvider.js";
import RequireAuth from "./components/auth/RequireAuth.js";
import Home from "./pages/Home.js";
import NoMatch from "./pages/NoMatch.js";
import { ThemeProvider } from "@mui/material/styles";
import { themeOptions } from "./theme.js";
import Log from "./pages/Log.js";
import Alarm from "./pages/Alarm.js";
import Elders from "./pages/Elders.js";
import LoginForm from "./components/LoginForm.js";
import SignupForm from "./components/SignupForm.js";
import Logout from "./components/Logout.js";
import NotificationProvider from "./providers/NotificationProvider.js";
import Dashboard from "./pages/Dashboard.js";

const App = () => {
  return (
    <ThemeProvider theme={themeOptions}>
      <NotificationProvider>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              <Route
                path="/"
                element={
                  <RequireAuth>
                    <Dashboard />
                  </RequireAuth>
                }
              >
                <Route path="" element={<Home />} />
                <Route path="log" element={<Log />} />
                <Route path="alarm" element={<Alarm />} />
                <Route path="elders" element={<Elders />} />
              </Route>

              <Route path="login" element={<LoginForm />}>
                <Route path="forgot" element={<></>} />
              </Route>
              <Route path="signup" element={<SignupForm />} />
              <Route path="logout" element={<Logout />} />
              <Route path="*" element={<NoMatch />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </NotificationProvider>
    </ThemeProvider>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));
