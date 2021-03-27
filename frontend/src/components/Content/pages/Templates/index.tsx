import React, { useEffect, useState } from "react";
import { useFetch } from "../../../../utils";
import ContentWrapper from "../../ContentWrapper";
import TemplateCard from "./TemplateCard";

export interface TemplateList {
  id: number;
  type: number;
  title: string;
  name: string;
  platform: string;
  description: string;
  logo: string;
  image: string;
  command: null | string;
  notes: string;
  categories: string[];
  restart_policy: string;
  ports: [];
  volumes: [];
  env: [];
  devices: [];
  labels: [];
  sysctls: [];
  cap_add: [];
  network_mode: string;
  network: string;
  cpus: null | number;
  mem_limit: null | number;
}
interface Template {
  title: string;
  url: string;
  id: number;
  updated_at: string;
  created_at: string;
}

const Templates = () => {
  const [template, setTemplate] = useState([] as Template[]);
  const [templates, setTemplates] = useState([] as TemplateList[]);
  const { data, error, loading } = useFetch("/api/templates/");

  useEffect(() => {
    error && console.log(error);
    data && setTemplate(data);
    if (template[0] && template[0].url) {
      fetch(template[0].url)
        .then((res) => res.json())
        .then((response) => setTemplates(response));
    }
  }, [data, error, template]);

  return (
    <ContentWrapper header={"Templates"}>
      <div className={"flex flex-row flex-wrap"}>
        {loading ? (
          <span>Loading...</span>
        ) : (
          templates.map((template, index) => {
            return <TemplateCard template={template} key={index} />;
          })
        )}
      </div>
    </ContentWrapper>
  );
};

export default Templates;
