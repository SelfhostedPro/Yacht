import React, { useEffect, useState } from "react";
import { useFetch } from "../../../../utils";

interface Volume {
  CreatedAt: string;
  Driver: string;
  Labels: null | string;
  MountPoint: string;
  Name: string;
  Options: null | string;
  Scope: string;
  inUse: boolean;
}

const Volumes = () => {
  const { data, error, loading } = useFetch("/api/resources/volumes/");
  const [volumes, setVolumes] = useState([] as Volume[]);

  useEffect(() => {
    if (data.length > 0) {
      setVolumes(data);
    }
    error && console.log(error);
  }, [error, data]);

  return (
    <>
      <div className={"text-2xl"}>VOLUMES</div>
      <div className={"flex flex-row justify-between"}>
        <span className={"w-1/5 truncate"}>Name</span>
        <span className={"w-1/5 truncate"}>inUse</span>
        <span className={"w-1/5 truncate"}>Project</span>
        <span className={"w-1/5 truncate"}>Driver</span>
        <span className={"w-1/5 truncate"}>Created</span>
      </div>
      <div>
        {loading
          ? "Loading..."
          : volumes.map((volume, index) => {
              return (
                <div className={"flex flex-row justify-between"} key={index}>
                  <span className={"w-1/5 truncate"}>{volume.Name}</span>
                  <span className={"w-1/5 truncate"}>
                    {volume.inUse ? "inUse" : "Unused"}
                  </span>
                  <span className={"w-1/5 truncate"}>{volume.Name}</span>
                  <span className={"w-1/5 truncate"}>{volume.Driver}</span>
                  <span className={"w-1/5 truncate"}>{volume.CreatedAt}</span>
                </div>
              );
            })}
      </div>
    </>
  );
};

export default Volumes;
