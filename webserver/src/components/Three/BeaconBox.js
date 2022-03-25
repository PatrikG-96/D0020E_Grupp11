import {
  Box,
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
import * as THREE from "three";
import { useFrame } from "@react-three/fiber";
import { useEffect, useReducer, useRef, useState } from "react";
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

function BeaconBox(props) {
  const boxRef = useRef();

  const [hovered, hover] = useState(false);
  const [clicked, setClicked] = useState(false);
  const [focusOnTarget, setFocusOnTarget] = useState(false);
  const [lookAtTarget, setLookAtTarget] = useState(false);

  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    if (state.isOpen) {
      setOffset({ horizontal: 900, vertical: 350 });
    } else {
      setOffset({ horizontal: 345, vertical: 350 });
    }
  }, [state.isOpen]);

  const [offset, setOffset] = useState({ horizontal: 250, vertical: 350 });

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

  useEffect(() => {
    if (focusOnTarget) {
      const timer = setTimeout(() => {
        setFocusOnTarget(false);
        setLookAtTarget(false);
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [focusOnTarget]);

  useFrame((state, delta) => {
    //console.log(props.position[0]);
    const vec = new THREE.Vector3(
      props.position[0],
      props.position[1],
      props.position[2]
    );

    boxRef.current.position.lerp(vec, 0.1);

    const cameraVec = new THREE.Vector3(
      props.position[0] + 3,
      props.position[1] + 2,
      props.position[2] + 3
    );

    var distance = state.camera.position.distanceTo(boxRef.current.position);
    if (focusOnTarget && distance > 4) {
      state.camera.position.lerp(cameraVec, 0.1);
      setLookAtTarget(true);
    }

    if (lookAtTarget) {
      state.camera.lookAt(vec);
    }
  });

  return (
    <mesh
      ref={boxRef}
      {...props.position}
      onPointerOver={(event) => hover(true)}
      onPointerOut={(event) => hover(false)}
      onClick={(event) => setClicked(!clicked)}
      scale={10}
    >
      <boxBufferGeometry attach="geometry" />
      <meshStandardMaterial
        color={
          hovered || props.id === "03FF5C0A2BFA3A9B" ? "hotpink" : "orange"
        }
      />
      {clicked ? (
        <Html
          position={[0, 1, 0]}
          occlude={[boxRef]}
          calculatePosition={overrideCalculatePosition}
          //distanceFactor={15}
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
                  <Typography>Beacon</Typography>
                </Box>
                <Box sx={{ pr: 28 }} />
                <Box sx={{ justifyContent: "flex-end" }}>
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
                    <Typography variant="subtitle1">Beacon ID: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">{props.id}</Typography>
                  </ListItem>
                  <ListItem>
                    <Typography variant="subtitle1">Pos X: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">{props.position[0]}</Typography>
                  </ListItem>
                  <ListItem>
                    <Typography variant="subtitle1">Pos Y: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">{props.position[1]}</Typography>
                  </ListItem>
                  <ListItem>
                    <Typography variant="subtitle1">Pos Z: </Typography>
                    <Typography> &nbsp;</Typography>
                    <Typography variant="body2">{props.position[2]}</Typography>
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

export default BeaconBox;
