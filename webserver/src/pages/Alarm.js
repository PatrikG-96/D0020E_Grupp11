import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/auth/useAuth";
import AlarmService from "../services/alarm.service";
import AuthService from "../services/auth.service";

export default function Alarm() {
  let auth = useAuth();
  let navigate = useNavigate();

  const [alarms, setAlarms] = useState([]);
  useEffect(() => {
    AlarmService.getAllPrivateAlarms().then(
      (response) => {
        setAlarms(response.data);
      },
      (error) => {
        console.log("Alarm", error.response);

        if (error.response && error.response.status === 403) {
          console.log("[Remove token]");
          AuthService.logout();
          auth.signout(() => {
            navigate("/login");
          });
        }
      }
    );
  }, []);

  return (
    <div>
      <h3> {alarms.map((alarm) => alarm.content)}</h3>
    </div>
  );
}
