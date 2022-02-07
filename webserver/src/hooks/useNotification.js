import  { useContext } from "react";
import { NotificationContext } from "../contexts/NotificationContext";

export function useNotification() {
  return useContext(NotificationContext);
}
