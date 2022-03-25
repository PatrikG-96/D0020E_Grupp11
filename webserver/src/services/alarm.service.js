import { useEffect, useState } from "react";
import useEventSource from "../hooks/useEventSource";

/**
 * * SSE - Server Sent Events
 
 * @method SetListener() Creates and eventSource that is triggered when event is sent on the endpoint from server
 *  @param endpoint API endpoint that client should listen to
 *  @param user_id API data
 *
 */
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
