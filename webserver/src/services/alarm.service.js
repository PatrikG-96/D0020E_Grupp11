import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://127.0.0.1:5000/alarms";

const getAllPublicAlarms = () => {
  return axios.get(API_URL + "/public");
};

const getAllPrivateAlarms = () => {
  return axios.get(API_URL + "/private", { headers: authHeader() });
};

const AlarmService = {
  getAllPublicAlarms,
  getAllPrivateAlarms,
};

export default AlarmService;
