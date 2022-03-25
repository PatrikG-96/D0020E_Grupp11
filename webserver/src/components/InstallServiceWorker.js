import { Box, Grid, LinearProgress } from "@mui/material";
import React, { useState } from "react";
import eventBus from "../services/EventBus";

function InstallServiceWorker() {
  const [progress, setProgress] = useState(0);

  eventBus.on("subscribeProgress", (data) => {
    setProgress(data.progress);
  });

  return (
    <Box sx={{ width: "100%" }}>
      <Grid container justifyContent="space-between">
        <Grid item xs={12} sx={{ pt: 1, pl: 1 }}>
          <LinearProgress
            color="primary"
            variant="determinate"
            value={progress}
          />
        </Grid>
      </Grid>
    </Box>
  );
}

export default InstallServiceWorker;
