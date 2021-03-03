import { useEffect } from "react";
import { atom, useRecoilState } from "recoil";

const appsState = atom({
  key: 'AppsState',
  default: {} // TODO:  We really should apply types here later, and possibly move the Atoms into a consolidated location/file
});

const AppsTable = () => {
  const [apps, setApps] = useRecoilState(appsState);

  useEffect(() => {
    const fetchApps = async () => {
      await fetch("/api/apps/")
        .then((res) => res.json())
        .then((data) => setApps(data));
    };

    fetchApps();
  }, [setApps]);

  return (
    <div>
      <div>Hello world, we be fetching apps!</div>
      <div className="text-xs">{JSON.stringify(apps)}</div>
    </div>
  );
};

export default AppsTable;
