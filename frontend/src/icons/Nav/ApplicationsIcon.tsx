import React from "react";

const pathD =
  "M19,4C20.11,4 21,4.9 21,6V18A2,2 0 0,1 19,20H5C3.89,20 3,19.1 3,18V6A2,2 0 0,1 5,4H19M19,18V8H5V18H19Z";

const ApplicationsIcon = () => {
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

export default ApplicationsIcon;
