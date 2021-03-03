import { atom } from "recoil";

export interface Port {
  HostIp: string;
  HostPort: string;
}

export interface App {
  name: string;
  short_id: string;
  ports: {[key: string]: Port[]};
}

export const appsState = atom({
  key: "AppsState",
  default: [] as App[],
});