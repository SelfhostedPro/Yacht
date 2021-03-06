import { useEffect } from "react";
import { useRecoilState } from "recoil";
import { appsState } from "../../store/apps";
import TableBody from "./TableBody";
import TableHeader from "./TableHeader";

const Apps = () => {
  const tableHeaders = ["name", "short_id", "created", "status", "ports"];

  const [, setApps] = useRecoilState(appsState);

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
    <div className={"flex flex-col justify-center align-center"}>
      <div>Hello world, we be fetching apps!</div>
      <table className={"min-w-full w-full table-auto"}>
        <TableHeader headers={tableHeaders} />
        <TableBody />
      </table>
    </div>
  );
};

export default Apps;
