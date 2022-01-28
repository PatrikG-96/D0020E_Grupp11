import { createTheme } from "@mui/material/styles";

export const themeOptions = createTheme({
  palette: {
    type: "light",
    primary: {
      main: "#6b78df",
      dark: "#6270dd",
      light: "#7380f2",
    },
    secondary: {
      main: "#ff7940",
      contrastText: "#ffffff",
    },
    info: {
      main: "#2196f3",
    },
    success: {
      main: "#4caf50",
    },
  },
  typography: {
    fontFamily: "Roboto",
  },
});
