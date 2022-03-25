import React, { useCallback, useMemo } from "react";
import * as THREE from "three";

function RoomBoundry({ firstPos, secPos, color }) {
  const points = useMemo(
    () => [
      new THREE.Vector3(firstPos.x, firstPos.y, firstPos.z),
      new THREE.Vector3(secPos.x, firstPos.y, firstPos.z),
      new THREE.Vector3(secPos.x, firstPos.y, secPos.z),
      new THREE.Vector3(firstPos.x, firstPos.y, secPos.z),
      new THREE.Vector3(firstPos.x, firstPos.y, firstPos.z),

      new THREE.Vector3(firstPos.x, secPos.y, firstPos.z),
      new THREE.Vector3(secPos.x, secPos.y, firstPos.z),
      new THREE.Vector3(secPos.x, secPos.y, secPos.z),
      new THREE.Vector3(firstPos.x, secPos.y, secPos.z),
      new THREE.Vector3(firstPos.x, secPos.y, firstPos.z),

      new THREE.Vector3(secPos.x, secPos.y, firstPos.z),
      new THREE.Vector3(secPos.x, firstPos.y, firstPos.z),
      new THREE.Vector3(secPos.x, firstPos.y, secPos.z),
      new THREE.Vector3(secPos.x, secPos.y, secPos.z),
      new THREE.Vector3(firstPos.x, secPos.y, secPos.z),
      new THREE.Vector3(firstPos.x, firstPos.y, secPos.z),
    ],
    [firstPos, secPos]
  );
  const onUpdate = useCallback((self) => self.setFromPoints(points), [points]);
  return (
    <>
      <line position={[0, 0, 0]}>
        <bufferGeometry attach="geometry" onUpdate={onUpdate} />
        <lineBasicMaterial
          attach="material"
          color={color}
          linewidth={10}
          linecap={"round"}
          linejoin={"round"}
        />
      </line>
    </>
  );
}

export default RoomBoundry;
