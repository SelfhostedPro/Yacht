import React, { useEffect } from "react";
import { useRecoilState } from "recoil";
import { appsState } from "../../../../store/apps";
import { useFetch } from "../../../../utils";
import ContentWrapper from "../../ContentWrapper";
import TableBody from "./TableBody";
import TableHeader from "./TableHeader";

const Apps = () => {
  const tableHeaders = ["name", "short_id", "created", "status", "ports"];

  const [, setApps] = useRecoilState(appsState);
  const { data, error, loading } = useFetch("/api/apps/");
  setApps(data);

  useEffect(() => {
    error && console.log(error);
  }, [error]);

  return (
    <ContentWrapper header={"Applications"}>
      <table className={"w-full table-auto my-4"}>
        <TableHeader headers={tableHeaders} />
        <TableBody loading={loading} />
      </table>
    </ContentWrapper>
  );
};

export default Apps;
