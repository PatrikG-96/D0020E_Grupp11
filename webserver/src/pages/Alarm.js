import React, { useEffect, useState } from "react";
import { useNotification } from "../hooks/useNotification";
import AlarmService from "../services/alarm.service";

export default function Alarm() {
  const notification = useNotification();
  const alarms = AlarmService.SetListener("","1")

  useEffect(() => {
    notification.showNotification("Alarm test")
  }, [alarms]);
  

  return (
    <div>
      {alarms.length > 0 ? (
        <div>
          <h1>Alarms</h1>
          {alarms.map((alarm) => (
            <h3>
              The device id: {alarm.device_id}. Type of alarm: {alarm.type}
            </h3>
          ))}
        </div>
      ) : (
        <div>
          <h1>No alert received</h1>
        </div>
      )}
    </div>
  );
}
