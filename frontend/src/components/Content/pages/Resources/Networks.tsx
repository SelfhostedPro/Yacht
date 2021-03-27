import React, { useEffect, useState } from "react";
import { useFetch } from "../../../../utils";

interface Network {
  Name: string;
  Id: string;
  Created: string;
  Driver: string;
  EnableIPv6: boolean;
  IPAM: {
    Driver: string;
    Options: null | string;
    Config: { Subnet: string; Gateway: string };
  };
  Internal: boolean;
  Attachable: boolean;
  Ingress: boolean;
  ConfigFrom: { Network: string };
  ConfigOnly: boolean;
  Containers: {};
  Options: {};
  Labels: {};
  inUse: boolean;
}

const Networks = () => {
  const [networks, setNetworks] = useState([] as Network[]);
  const { data, error, loading } = useFetch("/api/resources/networks/");

  useEffect(() => {
    data && setNetworks(data);
    error && console.log(error);
  }, [data, error]);

  return (
    <>
      <div className={"text-2xl"}>NETWORKS</div>
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
          : networks.map((network, index) => {
              return (
                <div className={"flex flex-row justify-between"} key={index}>
                  <span className={"w-1/5 truncate"}>{network.Name}</span>
                  <span className={"w-1/5 truncate"}>
                    {!network.inUse ? "Unused" : "inUse"}
                  </span>
                  <span className={"w-1/5 truncate"}>{network.Name}</span>
                  <span className={"w-1/5 truncate"}>{network.Driver}</span>
                  <span className={"w-1/5 truncate"}>{network.Created}</span>
                </div>
              );
            })}
      </div>
    </>
  );
};

export default Networks;
