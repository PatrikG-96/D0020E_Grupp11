import { DataGrid } from "@mui/x-data-grid";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Button } from "@mui/material";
const API_PATH = "http://localhost:5000";

function ElderlyTable() {
  const [elderly, setEldery] = useState([]);
  const uid = localStorage.getItem("userID");

  useEffect(() => {
    axios.get(API_PATH + "/elders/all").then((response) => {
      console.log(response);
      setEldery(response.data);
    });
  }, []);

  const handleUpdateElders = () => {
    console.log(elderly);
  };

  const columns = [
    { field: "elderlyID", headerName: "Elderly ID", width: 90 },
    {
      field: "name",
      headerName: "Namn",
      width: 90,
    },
    {
      field: "address",
      headerName: "Address",
      width: 150,
      editable: true,
    },
    {
      field: "subscribed",
      headerName: "Premunerat?",
      width: 110,
      editable: true,
    },
  ];

  return (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid
        rows={elderly}
        getRowId={(row) => row.elderlyID}
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

export default ElderlyTable;
