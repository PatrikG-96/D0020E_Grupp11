import {
  AnnouncementSharp,
  BookSharp,
  CircleNotifications,
  Dashboard,
  Logout,
  PeopleSharp,
  SettingsApplications,
} from "@mui/icons-material";
import { Fade, Icon, ListItemIcon, ListItemText } from "@mui/material";
import MuiListItem from "@mui/material/ListItem";
import React, { useEffect, useState } from "react";
import { styled } from "@mui/material/styles";
import { Link } from "react-router-dom";

const styles = {
  largeIcon: {
    fontSize: 40,
  },
};

const mainTabs = [
  {
    id: 0,
    text: "Dashboard",
    link: "/",
    icon: <Dashboard style={styles.largeIcon} />,
  },
  {
    id: 1,
    text: "Logg bok",
    link: "/log",
    icon: <BookSharp style={styles.largeIcon} />,
  },
  {
    id: 2,
    text: "Alarm",
    link: "/alarm",
    icon: <AnnouncementSharp style={styles.largeIcon} />,
  },
  {
    id: 3,
    text: "Äldre",
    link: "/elders",
    icon: <PeopleSharp style={styles.largeIcon} />,
  },
];

const secTabs = [
  { id: 4, text: "Notifikationer", link: "/notifications" },
  { id: 5, text: "Inställningar", link: "/settings" },
  { id: 6, text: "Logga ut", link: "/logout" },
];

let fadeInTime = 200;

const ListItem = styled(MuiListItem, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  paddingLeft: theme.spacing(5),
  transition: theme.transitions.create(["padding"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  [theme.breakpoints.down("sm")]: { paddingLeft: theme.spacing(2) },
  ...(open && {
    transition: theme.transitions.create(["padding"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

export function MainListItems(props) {
  const [currentTab, setCurrentTab] = useState(0);

  useEffect(() => {
    let tab = mainTabs.find((x) => x.id === currentTab).text;
    props.currTab(tab);
  }, [currentTab]);

  return (
    <div>
      {mainTabs.map((tab) => (
        <ListItem
          button
          key={tab.id}
          component={Link}
          to={tab.link}
          onClick={() => {
            setCurrentTab(tab.id);
          }}
        >
          <ListItemIcon className={styles.listItem}>
            {currentTab === tab.id ? (
              <Icon style={styles.largeIcon} color="Primary">
                {tab.icon}
              </Icon>
            ) : (
              <Icon style={styles.largeIcon} color="disabled">
                {tab.icon}
              </Icon>
            )}
          </ListItemIcon>
          <Fade in={props.open}>
            <ListItemText primary={tab.text} />
          </Fade>
        </ListItem>
      ))}
    </div>
  );
}

export function SecondaryListItems({ open }) {
  return (
    <div>
      <ListItem button>
        <ListItemIcon>
          <CircleNotifications color="disabled" style={styles.largeIcon} />
        </ListItemIcon>
        <Fade in={open} {...(open ? { timeout: fadeInTime * 1 } : {})}>
          <ListItemText primary="Notifikationer" />
        </Fade>
      </ListItem>
      <ListItem button>
        <ListItemIcon>
          <SettingsApplications color="disabled" style={styles.largeIcon} />
        </ListItemIcon>
        <Fade in={open} {...(open ? { timeout: fadeInTime * 2 } : {})}>
          <ListItemText primary="Inställningar" />
        </Fade>
      </ListItem>
      <ListItem button component={Link} to={"/logout"} onClick={() => {}}>
        <ListItemIcon>
          <Logout style={styles.largeIcon} />
        </ListItemIcon>
        <Fade in={open} {...(open ? { timeout: fadeInTime * 3 } : {})}>
          <ListItemText primary="Logga ut" />
        </Fade>
      </ListItem>
    </div>
  );
}
