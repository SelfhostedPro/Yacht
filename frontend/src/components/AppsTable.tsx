import { useEffect } from "react";
import { atom, useRecoilState } from "recoil";

const appsState = atom({
  key: "AppsState",
  default: [] as App[],
});

interface App {
  name: string;
  short_id: string;
  ports: {};
}

//  This would be a good interface for a Port, and above `ports: {}` would become `ports: Port[]`
//  interface Port {
//    id: number;
//    Name: string;
//    HostIp: string;
//    HostPort: string;
//  }

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
      <div className={"flex flex-row justify-between w-1/4"}>
        <div>name</div>
        <div>short_id</div>
        {/* <div>ports</div> */}
      </div>
      {apps.map((app, index) => {
        return (
          <div className={"flex flex-row justify-between w-1/4"} key={index}>
            <div>{app.name}</div>
            <div>{app.short_id}</div>
            {/* <div>{app.ports}</div> */}
          </div>
        );
      })}
    </div>
  );
};

export default AppsTable;
