import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import axios from "axios";
const API_PATH = "http://localhost:5000";

const columns = [
  { field: "alarmID", headerName: "Alarm ID", width: 90 },
  {
    field: "deviceID",
    headerName: "Device ID",
    width: 90,
  },
  {
    field: "type",
    headerName: "Alarm Type",
    width: 150,
    editable: true,
  },

  {
    field: "read",
    headerName: "Read",
    width: 110,
    editable: true,
  },
  {
    field: "resolved",
    headerName: "Resolved",
    width: 110,
    editabe: true,
  },
];

function AlarmTable() {
  const [alarms, setAlarms] = useState([]);
  var uid = localStorage.getItem("userID");

  useEffect(() => {
    axios
      .get(API_PATH + "/alarm/active/subscribed", {
        params: { user_id: uid },
      })
      .then((response) => {
        console.log(response);
        //setAlarms(response.data);
      });
  }, []);

  //useEffect(() => {
  //fetch("/alarm/active/subscribed?user_id=" + uid)
  //.then((response) => response.json())
  //.then((data) => {
  //var arr = [];
  //var n = data.length;
  //for (let i = 0; i < n; i++) {
  //var row = data[i.toString()];
  //row.id = i;
  //arr.push(row);
  //}
  //setAlarms(arr);
  //});
  //// eslint-disable-next-line
  //}, []);

  return (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid
        rows={alarms}
        getRowId={(row) => row.alarmID}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[5]}
        checkboxSelection
        loading={false}
        disableSelectionClick
      ></DataGrid>
    </div>
  );
}

export default AlarmTable;
