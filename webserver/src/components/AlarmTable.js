import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";


const columns = [
  { field: 'alarmID', headerName: 'Alarm ID', width: 90 },
  {
    field: 'deviceID',
    headerName: 'Device ID',
    width: 90,
  },
  {
    field: 'type',
    headerName: 'Alarm Type',
    width: 150,
    editable: true,
  },
  
  {
    field: 'read',
    headerName: 'Read',
    width: 110,
    editable: true,
  },
  {
    field: 'resolved',
    headerName: 'Resolved',
    width: 110,
    editabe: true,
  }
  /*{
    field: 'fullName',
    headerName: 'Full name',
    description: 'This column has a value getter and is not sortable.',
    sortable: false,
    width: 160,
    valueGetter: (params) =>
      `${params.row.firstName || ''} ${params.row.lastName || ''}`,
  },*/
];

const rows = [
  { id: 1, alarmType: 'fall', deviceID: 1, read: 'Yes', resolved: 'Yes'},
  { id: 2, alarmType: 'fall', deviceID: 1, read: 'Yes', resolved: 'No' },
  { id: 3, alarmType: 'fall', deviceID: 1, read: 'Yes', resolved: 'No' },
  { id: 4, alarmType: 'fall', deviceID: 5, read: 'Yes', resolved: 'Yes' },
  { id: 5, alarmType: 'fall', deviceID: 8, read: 'No', resolved: 'Yes' },
  { id: 6, alarmType: 'fall', deviceID: 0, read: 'No', resolved: 'Yes' },
  { id: 7, alarmType: 'fall', deviceID: 9, read: 'Yes', resolved: 'No' },
  { id: 8, alarmType: 'fall', deviceID: 2, read: 'No', resolved: 'Yes'},
  { id: 9, alarmType: 'fall', deviceID: 2, read:  'No', resolved: 'No'},
];

function AlarmTable() {
  const [alarms, setAlarms] = useState([])
  var uid = localStorage.getItem('userID')
  useEffect(() => {
    fetch("/alarm/active/subscribed?user_id="+uid).then(response => response.json()).then(data => {
      var arr = []
      var n = data.length
      for (let i = 0; i < n; i++) {
        var row = data[i.toString()]
        row.id = i
        arr.push(row)
      }
      setAlarms(arr)
    })
  }, [])


  return (
    <div style={{ height: 700, width: '100%' }}>
      <DataGrid
        rows={alarms}
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
