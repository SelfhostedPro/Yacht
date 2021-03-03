import { atom } from "recoil";

export interface Port {
  ContainerPort: string;
  HostIp: string;
  HostPort: string;
  Label: string;

}

export interface App {
  name: string;
  short_id: string;
  ports: Port[];
}

export const appsState = atom({
  key: "AppsState",
  default: [] as App[],
});