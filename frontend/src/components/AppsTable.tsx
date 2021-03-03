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
      <table className={"min-w-max w-full table-auto"}>
        <thead>
          <tr className={"bg-gray-200 text-gray-600 uppercase text-sm leading-normal"}>
            <th>name</th>
            <th>short_id</th>
            <th>created</th>
            <th>status</th>
            <th>ports</th>
          </tr>
        </thead>
        <tbody className={"text-gray-600 text-sm font-light"}>
          {apps.map((app, index) => {
            return (
              <tr className={"border-b border-gray-200 hover:bg-gray-100"} key={index}>
                <td className={"py-3 px-6 text-center"}>{app.name}</td>
                <td className={"py-3 px-6 text-center"}>{app.short_id}</td>
                <td className={"py-3 px-6 text-center"}>{app.created}</td>
                <td className={"py-3 px-6 text-center"}>{app.status}</td>
                <td className={"py-3 px-6 text-center"}>{app.ports.map((port, index) => {
                  return (
                    <div>
                      { app.ports[index]["Label"] ?
                        <span className="px-3 py-1 text-xs text-purple-600 bg-purple-200 rounded-full has-tooltip">{app.ports[index]["Label"]}</span> 
                        : <span>{app.ports[index]["HostPort"] + '=>' + app.ports[index]["HostIp"] + ':'+app.ports[index]["ContainerPort"]}</span>}
                    </div>
                  )
                })}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default AppsTable;
