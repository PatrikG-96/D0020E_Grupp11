import { useEffect, useState } from "react";
import useEventSource from "../hooks/useEventSource";

function SetListener(endpoint, user_id) {
  const eventSource = useEventSource(
    // ? Endpoint might be obsolete here
    `http://localhost:2000/alarm/listen?user_id=${user_id}`
  );
  const [alarms, setAlarms] = useState([]);

  useEffect(() => {
    if (eventSource) setAlarms((oldArray) => [...oldArray, eventSource]);
  }, [eventSource]);

  return alarms;
}

const AlarmService = {
  SetListener,
};

export default AlarmService;
