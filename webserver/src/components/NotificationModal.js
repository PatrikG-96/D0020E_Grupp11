import React, { useEffect, useState } from "react";
import {
  Backdrop,
  Box,
  Modal,
  Fade,
  Button,
  Typography,
  Card,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import swDev from "../swDev";
import { DataObject, Engineering, ExpandMore } from "@mui/icons-material";
import InstallServiceWorker from "./InstallServiceWorker";
import eventBus from "../services/EventBus";
import PrettyPrintJson from "../services/PrettyPrintJson";
import AlertBanner from "./AlertBanner";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  minWidth: "300px",
  width: "50%",
  transform: "translate(-50%, -50%)",
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 1,
};

export default function NotificationsModal(props) {
  const [open, setOpen] = useState(false);

  const handleClose = () => props.handleClose();

  useEffect(() => {
    setOpen(props.open);
  }, [props]);

  useEffect(() => {
    if (open === true) {
      let endpoint = JSON.parse(localStorage.getItem("subscription"));
      if (endpoint) {
        setSwComplete(true);
        setSub_token(endpoint);
      }
    }
  }, [open]);

  const handleSetupSW = () => {
    swDev();
  };

  const [expanded, setExpanded] = useState(false);

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const [swComplete, setSwComplete] = useState(false);
  const [sub_token, setSub_token] = useState(null);
  const [message, setMessage] = useState("");
  eventBus.on("subscribeProgress", (data) => {
    setMessage(data.message);
    if (data.complete) {
      setSwComplete(true);
      setSub_token(data.sub);
      eventBus.remove("subscribeProgress");
    }
  });

  return (
    <Modal
      open={open}
      onClose={handleClose}
      closeAfterTransition
      BackdropComponent={Backdrop}
      BackdropProps={{
        timeout: 500,
      }}
    >
      <Fade in={props.open}>
        <Card sx={style}>
          <Grid container>
            <AlertBanner
              title="Warning"
              message="Notifictions will only be received when online"
              severity="warning"
            />
            <Grid item xs={12}>
              <Typography variant="h6" component="h2">
                Notifications
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <div>
                <Accordion
                  expanded={expanded === "panel1"}
                  onChange={handleChange("panel1")}
                >
                  <AccordionSummary>
                    {swComplete ? (
                      <Grid
                        container
                        alignContent="center"
                        justifyContent="space-between"
                      >
                        <Grid item xs={11} sm={6} md={7}>
                          <Typography variant="overline">
                            Setup service worker
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Service worker installed
                          </Typography>
                        </Grid>
                        <Grid item xs={1} sm={1} md={1}>
                          <Engineering color="success" fontSize="large" />
                        </Grid>
                      </Grid>
                    ) : (
                      <Grid
                        container
                        alignContent="center"
                        justifyContent="space-between"
                      >
                        <Grid item xs={12} sm={12} md={7}>
                          <Typography variant="overline">
                            Setup service worker
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {message}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={12} md={4} lg={3}>
                          <Button variant="contained" onClick={handleSetupSW}>
                            Setup up worker
                          </Button>
                        </Grid>
                        <Grid item xs={12}>
                          <InstallServiceWorker />
                        </Grid>
                      </Grid>
                    )}
                  </AccordionSummary>
                </Accordion>
                {/*TODO Fix the background for the overflow*/}
                <Box component="div" sx={{ overflow: "auto" }}>
                  <Accordion
                    expanded={expanded === "panel2"}
                    onChange={handleChange("panel2")}
                  >
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Grid
                        container
                        alignContent="center"
                        justifyContent="space-between"
                      >
                        <Grid item xs={10} sm={7} md={7}>
                          <Typography variant="overline">Endpoint</Typography>
                        </Grid>
                        <Grid item xs={2} sm={2} md={1}>
                          <DataObject color="primary" fontSize="large" />
                        </Grid>
                      </Grid>
                    </AccordionSummary>
                    <AccordionDetails>
                      {sub_token ? (
                        <PrettyPrintJson data={sub_token} />
                      ) : (
                        <Typography>Run the service worker</Typography>
                      )}
                    </AccordionDetails>
                  </Accordion>
                </Box>
              </div>
            </Grid>
          </Grid>
        </Card>
      </Fade>
    </Modal>
  );
}
