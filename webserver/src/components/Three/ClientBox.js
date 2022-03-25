import {
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  IconButton,
  List,
  ListItem,
  ListSubheader,
  Typography,
} from "@mui/material";
import { Close } from "@mui/icons-material";
import { Html } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect, useReducer, useRef, useState } from "react";
import * as THREE from "three";
import ActionsDrawer from "../ActionsDrawer";

const initialState = { isOpen: false };

function reducer(state, action) {
  switch (action.type) {
    case "toggle":
      return { isOpen: !state.isOpen };
    default:
      throw new Error();
  }
}

function ClientBox(props) {
  const boxRef = useRef();

  const [hovered, hover] = useState(false);
  const [clicked, setClicked] = useState(false);
  const [focusOnTarget, setFocusOnTarget] = useState(false);
  const [lookAtTarget, setLookAtTarget] = useState(false);
  const [offset, setOffset] = useState({ horizontal: 250, vertical: 350 });

  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    if (state.isOpen) {
      setOffset({ horizontal: 900, vertical: 350 });
    } else {
      setOffset({ horizontal: 345, vertical: 350 });
    }
  }, [state.isOpen]);

  useEffect(() => {
    if (focusOnTarget) {
      const timer = setTimeout(() => {
        setFocusOnTarget(false);
        setLookAtTarget(false);
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [focusOnTarget]);

  const v1 = new THREE.Vector3();
  const overrideCalculatePosition = (el, camera, size) => {
    const objectPos = v1.setFromMatrixPosition(el.matrixWorld);
    objectPos.project(camera);
    const widthHalf = size.width / 2;
    const heightHalf = size.height / 2;
    return [
      Math.min(
        size.width - offset.horizontal,
        Math.max(0, objectPos.x * widthHalf + widthHalf)
      ),
      Math.min(
        size.height - offset.vertical,
        Math.max(0, -(objectPos.y * heightHalf) + heightHalf)
      ),
    ];
  };

  useFrame((state, delta) => {
    if (props.id !== null) {
      //console.log(props.position);
      const vec = new THREE.Vector3(
        props.position[0],
        props.position[1],
        props.position[2]
      );

      boxRef.current.position.lerp(vec, 0.01);

      const cameraVec = new THREE.Vector3(
        props.position[0],
        props.position[1],
        props.position[2]
      );

      var distance = state.camera.position.distanceTo(boxRef.current.position);
      if (focusOnTarget && distance > 40) {
        state.camera.position.lerp(cameraVec, 0.1);
        setLookAtTarget(true);
      }

      if (lookAtTarget) {
        state.camera.lookAt(vec);
      }
    }
  });
  return (
    <mesh
      ref={boxRef}
      {...props.position}
      onPointerOver={(event) => hover(true)}
      onPointerOut={(event) => hover(false)}
      onClick={(event) => setClicked(!clicked)}
      scale={5}
    >
      <boxBufferGeometry attach="geometry" />
      <meshStandardMaterial color={hovered ? "hotpink" : "blue"} />
      {clicked ? (
        <Html
          position={[0, 1, 0]}
          occlude={[boxRef]}
          calculatePosition={overrideCalculatePosition}
          //distanceFactor={}
        >
          <ActionsDrawer toggle={state.isOpen} dispatch={dispatch} />
          <Box sx={{ minWidth: 345 }}>
            <Card sx={{ maxWidth: 345 }}>
              <Box
                sx={{
                  pl: 2,
                  pt: 1,
                  display: "inline-flex",
                  alignItems: "center",
                }}
              >
                <Box sx={{ display: "inline-flex", alignItems: "center" }}>
                  <Avatar />
                  <Box sx={{ pr: 2 }} />
                  <Typography>Alexander</Typography>
                </Box>
                <Box sx={{ pr: 2 }} />
                <Box sx={{ justifyContent: "flex-end" }}>
                  <Button
                    size="small"
                    onClick={() => setFocusOnTarget(!focusOnTarget)}
                  >
                    Focus
                  </Button>
                  <Button
                    size="small"
                    onClick={() => dispatch({ type: "toggle" })}
                  >
                    Actions
                  </Button>
                  <IconButton onClick={() => setClicked(!clicked)}>
                    <Close />
                  </IconButton>
                </Box>
              </Box>

              <CardContent>
                <List
                  disablePadding={true}
                  dense={true}
                  subheader={
                    <ListSubheader>
                      <Typography variant="h6">Information</Typography>
                    </ListSubheader>
                  }
                >
                  <ListItem>
                    <Typography variant="subtitle1">Tag ID: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">{props.id}</Typography>
                  </ListItem>
                  <ListItem>
                    <Typography variant="subtitle1">Battery: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">100</Typography>
                  </ListItem>
                  <ListItem>
                    <Typography variant="subtitle1">RSSI: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">1000</Typography>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Box>
        </Html>
      ) : (
        <Html></Html>
      )}
    </mesh>
  );
}

export default ClientBox;
