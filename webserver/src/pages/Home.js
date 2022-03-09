import React, { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
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
  const [beacons, setBeacons] = useState([]);
  const [beaconPositions, setBeaconPositions] = useState([]);

  const [tags, setTags] = useState([]);
  const [tagPositions, setTagPositions] = useState([]);

  const [offset, setOffset] = useState({ x: 0, y: 0, z: 0 });

  const socket = io("http://localhost:5000");
  socket.connect();

  socket.on("new-rapport", (data) => {
    const i = tags.findIndex((ele) => ele.id === data.id);
    if (i >= 0) {
      if (tags[i].id === data.id) {
        tags[i] = data;
        console.log(tagPositions[i]);
        tagPositions[i] = {
          id: data.id,
          position: {
            x: parseFloat(data.posX / 10),
            y: parseFloat(data.posZ / 10),
            z: parseFloat(data.posY / 10),
          },
        };
      }
    } else {
      console.log("Adding new Tag");
      setTags((oldArray) => [...oldArray, data]);
      setTagPositions((oldArray) => [
        ...oldArray,
        {
          id: data.id,
          position: {
            x: parseFloat(data.posX / 10),
            y: parseFloat(data.posZ / 10),
            z: parseFloat(data.posY / 10),
          },
        },
      ]);
    }
  });

  socket.on("new-beacon", (data) => {
    const i = beacons.findIndex((ele) => ele.id === data.id);
    if (i >= 0) {
      if (beacons[i].id === data.id) {
        beacons[i] = data;
      }
    } else {
      console.log("Adding new beacon");
      console.log({ x: data.posX / 10, y: data.posZ / 10, z: data.posY / 10 });
      setBeacons((oldArray) => [...oldArray, data]);
      setBeaconPositions((oldArray) => [
        ...oldArray,
        {
          id: data.id,
          position: {
            x: parseFloat(data.posX / 10),
            y: parseFloat(data.posZ / 10),
            z: parseFloat(data.posY / 10),
          },
        },
      ]);
      console.log("Beacon postitions:");
      console.log(beaconPositions);
    }
  });

  const [room, setRoom] = useState([]);

  useEffect(() => {
    if (beaconPositions.length >= 2) {
      setRoom([beaconPositions[0], beaconPositions[1]]);
    }
  }, [beaconPositions]);

  const CameraControls = () => {
    // Get a reference to the Three.js Camera, and the canvas html element.
    // We need these to setup the OrbitControls class.
    // https://threejs.org/docs/#examples/en/controls/OrbitControls

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

  return (
    <Box sx={{ height: 600 }}>
      <Canvas>
        <PerspectiveCamera near={0.1} far={3000} position={[0, 0, 0]} />
        <CameraControls />
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        {room.length > 0 ? (
          <RoomBoundry
            firstPos={{
              x: room[1].position.x,
              y: room[1].position.y,
              z: room[1].position.z,
            }}
            secPos={{
              x: room[0].position.x,
              y: room[0].position.y,
              z: room[0].position.z,
            }}
          />
        ) : (
          <></>
        )}

        {tagPositions.map((client) => (
          <ClientBox
            key={client.id}
            id={client.id}
            position={[client.position.x, client.position.y, client.position.z]}
          />
        ))}

        {beaconPositions.map((beacon) => (
          <BeaconBox
            position={[beacon.position.x, beacon.position.y, beacon.position.z]}
            key={beacon.id}
            id={beacon.id}
          />
        ))}
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
              </Tabs>
            </Box>
            <TabPanel value={value} index={0}></TabPanel>
            <TabPanel value={value} index={1}></TabPanel>
          </Box>
        </Card>
      </Box>
    </Box>
  );
}

export default Home;
