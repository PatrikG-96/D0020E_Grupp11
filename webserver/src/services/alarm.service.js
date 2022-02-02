import axios from "axios";
import React ,{ useEffect, useState } from "react";
import useEventSource from "../hooks/useEventSource";
import authHeader from "./auth-header";

const API_URL = "http://127.0.0.1:5000/alarms";

const getAllPublicAlarms = () => {
  return axios.get(API_URL + "/public");
};

const getAllPrivateAlarms = () => {
  return axios.get(API_URL + "/private", { headers: authHeader() });
};

function SetListener(endpoint, user_id) {
  const eventSource = useEventSource(
    // ? Endpoint might be obsolete here
    `http://localhost:5000/alarm/listen?user_id=${user_id}`
  );
  const [alarms, setAlarms] = useState([]);

  useEffect(() => {
    if (eventSource) setAlarms((oldArray) => [...oldArray, eventSource]);
    //console.log(alarms);
  }, [eventSource]);

  return alarms
};

const AlarmService = {
  SetListener
};


export default AlarmService;
