import React from "react";
import { useRecoilValue } from "recoil";
import { appsState } from "../../../../store/apps";
import TableRow from "./TableRow";

interface OwnProps {
  loading: boolean;
}

const TableBody = ({ loading }: OwnProps) => {
  const apps = useRecoilValue(appsState);

  return (
    <tbody
      className={
        "text-gray-700 dark:text-gray-300 bg-transparent text-sm font-light"
      }
    >
      {loading ? (
        <tr>
          <td>Loading apps...</td>
        </tr>
      ) : (
        apps.map((app, index) => <TableRow app={app} key={`row-${index}`} />)
      )}
    </tbody>
  );
};

export default TableBody;
