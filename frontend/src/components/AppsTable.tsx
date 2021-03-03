import { useEffect } from "react";
import { useRecoilState } from "recoil";
import { appsState } from "../atoms";

const AppsTable = () => {
  const [apps, setApps] = useRecoilState(appsState);

  useEffect(() => {
    const fetchApps = async () => {
      await fetch("/api/apps/")
        .then((res) => res.json())
        .then((data) => {
          setApps(data);
        })
        .catch((err) => console.log(`Fetch error: ${err}`));
    };

    fetchApps();
  }, [setApps]);

  return (
    <div className={"flex flex-col justify-center align-center m-4"}>
      <div>Hello world, we be fetching apps!</div>
      <div className={"flex flex-row justify-between w-1/2"}>
        <div>name</div>
        <div>short_id</div>
        <div>ports</div>
      </div>
      {apps.map((app, index) => {
        return (
          <div className={"flex flex-row justify-between w-1/2"} key={index}>
            <div>{app.name}</div>
            <div>{app.short_id}</div>
            <div className={"flex flex-col"}>
              {Object.keys(app.ports).map((port) => {
                return (
                  <span>
                    {app.ports[port][0].HostIp + app.ports[port][0].HostPort}
                  </span>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default AppsTable;
