import React from "react";

const pathD =
  "M13,12H20V13.5H13M13,9.5H20V11H13M13,14.5H20V16H13M21,4H3A2,2 0 0,0 1,6V19A2,2 0 0,0 3,21H21A2,2 0 0,0 23,19V6A2,2 0 0,0 21,4M21,19H12V6H21";

const ProjectsIcon = () => {
  return (
    <svg
      xmlns={"http://www.w3.org/2000/svg"}
      viewBox={"0 0 24 24"}
      className={"w-6 h-6"}
    >
      <path d={pathD} fill={"currentColor"} />
    </svg>
  );
};

export default ProjectsIcon;
