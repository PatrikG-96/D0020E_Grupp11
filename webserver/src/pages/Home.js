import React, { useEffect, useRef, useState } from "react";
import { Canvas, extend, useFrame, useThree } from "@react-three/fiber";
import {
  ArcballControls,
  FirstPersonControls,
  FlyControls,
  Html,
  PerspectiveCamera,
} from "@react-three/drei";
import PropTypes from "prop-types";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { Box, Card, Divider, Tab, Tabs, Typography } from "@mui/material";
import ClientBox from "../components/Three/ClientBox";
import RoomBoundry from "../components/Three/RoomBoundry";
import BeaconBox from "../components/Three/BeaconBox";
import AlarmService from "../services/alarm.service";
import * as THREE from "three";

extend({ OrbitControls });

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

function Home() {
  const alarmListener = AlarmService.SetListener("", 1);
  const [alarms, setAlarms] = useState([]);
  const [latestAlarm, setLatestAlarm] = useState();
  const [latestAlarmPosition, setLatestAlarmPosition] = useState();

  useEffect(() => {
    console.log(alarmListener);
    setAlarms(alarmListener);
    setLatestAlarm(alarmListener[alarmListener.length - 1]);
  }, [alarmListener]);

  useEffect(() => {
    console.log("Latest Alarm updated: ");
    console.log(latestAlarm);
    if (latestAlarm !== undefined) {
      console.log(latestAlarm.coords);
      const position = latestAlarm.coords.split("'");

      setLatestAlarmPosition({
        id: latestAlarm.sensor_id,
        pos: {
          x: parseFloat(position[1]),
          y: parseFloat(position[3]),
          z: parseFloat(position[5]),
        },
      });
      console.log({
        id: latestAlarm.sensor_id,
        pos: {
          x: parseFloat(position[1]),
          y: parseFloat(position[3]),
          z: parseFloat(position[5]),
        },
      });
    }
  }, [latestAlarm]);

  const [beacons, setBeacons] = useState([
    { id: "4B2A8EE2B9BAAAC0", pos: { x: 4890, y: 6110, z: 350 } },
    { id: "6881445FDC01E3F2", pos: { x: 3280, y: 240, z: 1550 } },
    { id: "03FF5C0A2BFA3A9B", pos: { x: -10, y: 280, z: 2500 } },
    { id: "543D85B1B2D91E29", pos: { x: -40, y: -5930, z: 2500 } },
    { id: "9691FE799F371A4C", pos: { x: 5190, y: -5820, z: 2500 } },
    { id: "D4984282E2E4D10B", pos: { x: 5060, y: 540, z: 2500 } },
  ]);

  const yOffset = 2291;

  const [firstRoom, setFirstRoom] = useState({
    first: {
      id: "Upper corner 1",
      pos: { x: -177, y: -6432, z: 0 },
    },
    second: {
      id: "Lower corner 1",
      pos: { x: 6110, y: -237, z: 4342 - yOffset },
    },
  });

  const [secondRoom, setSecondRoom] = useState({
    first: { id: "Upper corner 2", pos: { x: 143, y: 168, z: 3915 - yOffset } },
    second: {
      id: "Lower corner 2",
      pos: { x: 3987, y: 6701, z: 0 },
    },
  });

  const [thirdRoom, setThirdRoom] = useState({
    first: {
      id: "Upper corner 3",
      pos: { x: 151, y: 6489, z: 4025 - yOffset },
    },
    second: {
      id: "Lower corner 3",
      pos: { x: 5005, y: 8962, z: 0 },
    },
  });

  const [tags, setTags] = useState([]);

  const CameraControls = () => {
    const {
      camera,
      gl: { domElement },
    } = useThree();

    // Ref to the controls, so that we can update them on every frame using useFrame
    const controls = useRef();
    useFrame((state) => controls.current.update());
    return (
      <orbitControls
        ref={controls}
        args={[camera, domElement]}
        minDistance={3}
        maxDistance={550}
      />
    );
  };

  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const scale = 100;

  return (
    <Box sx={{ height: 600 }}>
      <Canvas>
        <PerspectiveCamera near={0.1} far={3000} position={[0, 0, 0]} />
        <CameraControls />
        <ambientLight />
        {/* <gridHelper args={[10, 10]} /> */}
        <pointLight position={[10, 10, 10]} />

        <RoomBoundry
          color={"red"}
          firstPos={{
            x: firstRoom.first.pos.x / scale,
            y: firstRoom.first.pos.z / scale,
            z: firstRoom.first.pos.y / scale,
          }}
          secPos={{
            x: firstRoom.second.pos.x / scale,
            y: firstRoom.second.pos.z / scale,
            z: firstRoom.second.pos.y / scale,
          }}
        />
        <RoomBoundry
          color={"blue"}
          firstPos={{
            x: secondRoom.first.pos.x / scale,
            y: secondRoom.first.pos.z / scale,
            z: secondRoom.first.pos.y / scale,
          }}
          secPos={{
            x: secondRoom.second.pos.x / scale,
            y: secondRoom.second.pos.z / scale,
            z: secondRoom.second.pos.y / scale,
          }}
        />
        <RoomBoundry
          color={"orange"}
          firstPos={{
            x: thirdRoom.first.pos.x / scale,
            y: thirdRoom.first.pos.z / scale,
            z: thirdRoom.first.pos.y / scale,
          }}
          secPos={{
            x: thirdRoom.second.pos.x / scale,
            y: thirdRoom.second.pos.z / scale,
            z: thirdRoom.second.pos.y / scale,
          }}
        />

        {latestAlarmPosition !== undefined ? (
          <ClientBox
            position={[
              latestAlarmPosition.pos.x / scale,
              latestAlarmPosition.pos.z / scale,
              latestAlarmPosition.pos.y / scale,
            ]}
          />
        ) : (
          <></>
        )}

        {/* {beacons.map((beacon) => (
          <BeaconBox
            position={[beacon.pos.x / 10, beacon.pos.z / 10, beacon.pos.y / 10]}
            key={beacon.id}
            id={beacon.id}
          />
        ))} */}
      </Canvas>
      <Box>
        <Divider />
        <br />
        <Card sx={{ height: 500 }}>
          <Box sx={{ width: "100%" }}>
            <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
              <Tabs value={value} onChange={handleChange}>
                <Tab label="Beacons" {...a11yProps(0)} />
                <Tab label="Tags" {...a11yProps(1)} />
                <Tab label="Alarms" {...a11yProps(2)} />
              </Tabs>
            </Box>
            <TabPanel value={value} index={0}></TabPanel>
            <TabPanel value={value} index={1}></TabPanel>
            <TabPanel value={value} index={2}></TabPanel>
          </Box>
        </Card>
      </Box>
    </Box>
  );
}

export default Home;
