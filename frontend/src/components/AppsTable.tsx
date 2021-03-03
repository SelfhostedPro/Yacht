import { useEffect } from "react";
import { useRecoilState } from "recoil";
import { appsState } from "../store/apps";

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
      <table>
        <thead>
          <tr className={"flex flex-row justify-between w-1/2"}>
            <th>name</th>
            <th>short_id</th>
            <th>ports</th>
          </tr>
        </thead>
      </table>
      <tbody>
        {apps.map((app, index) => {
          return (
            <tr className={"flex flex-row justify-between w-1/2"} key={index}>
              <td>{app.name}</td>
              <td>{app.short_id}</td>
              <td>
              {app.ports.map((port, index) => {
                return (
                  <p>{app.ports[index]["Label"] + '=>' + app.ports[index]["HostIp"] + ':' + app.ports[index]["HostPort"] || app.ports[index]["ContainerPort"] + '=>' + app.ports[index]["HostIp"] + ':' + app.ports[index]["HostPort"]}</p>
                )
              })}
              </td>
            </tr>
          );
        })}
      </tbody>
    </div>
  );
};

export default AppsTable;
