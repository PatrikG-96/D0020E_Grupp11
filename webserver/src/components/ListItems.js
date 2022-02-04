import {
  AnnouncementSharp,
  BookSharp,
  CircleNotifications,
  Dashboard,
  Logout,
  PeopleSharp,
  SettingsApplications,
} from "@mui/icons-material";
import { Badge, Fade, Icon, ListItemIcon, ListItemText } from "@mui/material";
import MuiListItem from "@mui/material/ListItem";
import React, { useEffect, useState } from "react";
import { styled, useTheme } from "@mui/material/styles";
import { Link } from "react-router-dom";
import { useNotification } from "../hooks/useNotification";

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
    // eslint-disable-next-line
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

export function SecondaryListItems(props) {
  const theme = useTheme();
  let notif = useNotification();
  const status = notif.userPermission;

  const openNotif = () => {
    props.openNotif();
  };

  const denied = () => {
    notif.RequestPermission();
    //TODO Create a alert on site that says something like notifications need to be on in order to receive alerts
  };

  //TODO Fix the online icon to be green on login
  const [workerOnline, setWorkerOnline] = useState(null);
  useEffect(() => {
    let endpoint = JSON.parse(localStorage.getItem("subscription"));
    if (endpoint) {
      setWorkerOnline(true);
    }
  }, [props]);

  return (
    <div>
      {status ? (
        <div>
          {workerOnline ? (
            <ListItem button onClick={openNotif}>
              <ListItemIcon>
                <Badge
                  badgeContent=""
                  showZero
                  overlap="circular"
                  variant="dot"
                  sx={[
                    {
                      "& .MuiBadge-badge": {
                        backgroundColor: theme.palette.success.main,
                      },
                    },
                  ]}
                >
                  <CircleNotifications
                    sx={[
                      { "&:hover ": { color: theme.palette.text.secondary } },
                      { color: theme.palette.text.disabled },
                    ]}
                    style={styles.largeIcon}
                  />
                </Badge>
              </ListItemIcon>
              <Fade
                in={props.open}
                {...(props.open ? { timeout: fadeInTime * 1 } : {})}
              >
                <ListItemText primary="Notifikationer" />
              </Fade>
            </ListItem>
          ) : (
            <ListItem button onClick={openNotif}>
              <ListItemIcon>
                <Badge
                  badgeContent=""
                  showZero
                  overlap="circular"
                  variant="dot"
                  sx={[
                    {
                      "& .MuiBadge-badge": {
                        backgroundColor: theme.palette.error.main,
                      },
                    },
                  ]}
                >
                  <CircleNotifications
                    sx={[
                      { "&:hover ": { color: theme.palette.text.secondary } },
                      { color: theme.palette.text.disabled },
                    ]}
                    style={styles.largeIcon}
                  />
                </Badge>
              </ListItemIcon>
              <Fade
                in={props.open}
                {...(props.open ? { timeout: fadeInTime * 1 } : {})}
              >
                <ListItemText primary="Notifikationer" />
              </Fade>
            </ListItem>
          )}
        </div>
      ) : (
        <ListItem
          button
          onClick={denied}
          sx={[
            { "&:hover ": { backgroundColor: theme.palette.warning.dark } },
            { backgroundColor: theme.palette.warning.main },
          ]}
        >
          <ListItemIcon>
            <Badge
              badgeContent="!"
              showZero
              overlap="circular"
              sx={[
                {
                  "& .MuiBadge-badge": {
                    color: theme.palette.error.contrastText,
                    backgroundColor: theme.palette.error.dark,
                  },
                },
              ]}
            >
              <CircleNotifications
                sx={{ color: theme.palette.warning.contrastText }}
                style={styles.largeIcon}
              />
            </Badge>
          </ListItemIcon>
          <Fade
            in={props.open}
            {...(props.open ? { timeout: fadeInTime * 1 } : {})}
          >
            <ListItemText
              sx={{ color: theme.palette.warning.contrastText }}
              primary="Notifikationer"
              secondary="Notifikationer av"
            />
          </Fade>
        </ListItem>
      )}

      <ListItem button>
        <ListItemIcon>
          <SettingsApplications
            color="disabled"
            style={styles.largeIcon}
            sx={[
              { "&:hover ": { color: theme.palette.text.secondary } },
              { color: theme.palette.text.disabled },
            ]}
          />
        </ListItemIcon>
        <Fade
          in={props.open}
          {...(props.open ? { timeout: fadeInTime * 2 } : {})}
        >
          <ListItemText primary="Inställningar" />
        </Fade>
      </ListItem>
      <ListItem button component={Link} to={"/logout"} onClick={() => {}}>
        <ListItemIcon>
          <Logout
            style={styles.largeIcon}
            sx={[
              { "&:hover ": { color: theme.palette.text.secondary } },
              { color: theme.palette.text.disabled },
            ]}
          />
        </ListItemIcon>
        <Fade
          in={props.open}
          {...(props.open ? { timeout: fadeInTime * 3 } : {})}
        >
          <ListItemText primary="Logga ut" />
        </Fade>
      </ListItem>
    </div>
  );
}
