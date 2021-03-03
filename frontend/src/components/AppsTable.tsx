import { useEffect } from "react";
import { atom, useRecoilState } from "recoil";

const appsState = atom({
  key: "AppsState",
  default: [] as App[], // TODO:  We really should apply types here later, and possibly move the Atoms into a consolidated location/file
});

interface App {
  name: string;
  short_id: string;
  ports: {}; // {[name: string]: [{HostIp: string, HostPort: string}]} // something like this?
}

// interface Port {
//   HostIp: string;
//   HostPort: string;
// }

const AppsTable = () => {
  const [apps, setApps] = useRecoilState(appsState);

  useEffect(() => {
    const fetchApps = async () => {
      await fetch("/api/apps/")
        .then((res) => res.json())
        .then((data) => {
          setApps(data);
        });
    };

    fetchApps();
  }, [setApps]);

  return (
    <div>
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
