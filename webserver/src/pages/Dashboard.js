import { styled } from "@mui/material/styles";
import MuiAppBar from "@mui/material/AppBar";
import MuiDrawer from "@mui/material/Drawer";
import {
  Badge,
  Box,
  Container,
  CssBaseline,
  Divider,
  IconButton,
  List,
  Paper,
  Toolbar,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { ChevronLeft, Menu, Notifications } from "@mui/icons-material";
import { MainListItems, SecondaryListItems } from "../components/ListItems";
import { Outlet } from "react-router-dom";

const drawerWidth = 250;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer - 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    [theme.breakpoints.down("sm")]: {
      marginLeft: drawerWidth,
      zIndex: theme.zIndex.drawer - 1,
    },
  }),
  ...(!open && {
    paddingLeft: theme.spacing(9.5),
    transition: theme.transitions.create(["width", "margin", "padding"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    [theme.breakpoints.down("sm")]: {
      zIndex: theme.zIndex.drawer + 1,
      paddingLeft: theme.spacing(0),
    },
  }),
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  "& .MuiDrawer-paper": {
    position: "relative",
    whiteSpace: "nowrap",
    transition: theme.transitions.create(["width", "paddingLeft"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    ...(open && {
      width: drawerWidth,
      transition: theme.transitions.create(["width", "paddingLeft"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),

      [theme.breakpoints.down("sm")]: {
        width: theme.spacing(25),
      },
    }),
    boxSizing: "border-box",
    ...(!open && {
      width: theme.spacing(15),
      overflowX: "hidden",
      transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),

      [theme.breakpoints.down("sm")]: {
        width: drawerWidth / 3.2,
      },
    }),
  },
}));

function DashboardContent() {
  const [open, setOpen] = useState(false);
  const [currentTab, setCurrentTab] = useState("Dashboard");
  const toggleDrawer = () => {
    setOpen(!open);
  };

  const retrieveCurrentTab = (data) => {
    setCurrentTab(data);
  };

  return (
    <>
      <CssBaseline />
      <AppBar position="absolute" open={open}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={toggleDrawer}
            sx={{
              marginRight: 0,
              ...(open && { display: "none" }),
            }}
          >
            <Menu />
          </IconButton>
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            sx={{ flexGrow: 1 }}
          >
            {currentTab}
          </Typography>
          <IconButton color="inherit">
            <Badge badgeContent={4} color="secondary">
              <Notifications />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Drawer variant="permanent" open={open}>
          {open ? (
            <Toolbar
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "flex-end",
                px: [1],
              }}
            >
              <Typography
                component="h1"
                variant="h6"
                color="inherit"
                noWrap
                sx={{ pl: 2, flexGrow: 1 }}
              >
                {currentTab}
              </Typography>
              <IconButton size="large" onClick={toggleDrawer}>
                <ChevronLeft />
              </IconButton>
            </Toolbar>
          ) : (
            <Toolbar
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "flex-end",
                px: [5.5],
              }}
            >
              <IconButton
                edge="start"
                color="inherit"
                aria-label="open drawer"
                onClick={toggleDrawer}
              >
                <Menu />
              </IconButton>
            </Toolbar>
          )}
          <Divider />
          <List>
            <MainListItems open={open} currTab={retrieveCurrentTab} />
          </List>
          <Divider />
          <List>
            <SecondaryListItems open={open} />
          </List>
        </Drawer>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Paper>
              <Outlet />
            </Paper>
          </Container>
        </Box>
      </Box>
    </>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}
