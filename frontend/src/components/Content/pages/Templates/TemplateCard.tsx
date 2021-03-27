import React from "react";
import { TemplateList } from ".";

interface OwnProps {
  template: TemplateList;
}

const TemplateCard = ({ template }: OwnProps) => {
  return (
    <div
      className={
        "flex flex-col justify-between w-11/12 md:w-72 h-96 mx-auto my-2 rounded-md shadow-lg bg-white dark:bg-gray-700"
      }
      data-testid={"template-card"}
    >
      <div
        className={
          "w-full h-56 rounded-t-md flex flex-row justify-center items-center self-center p-2 object-scale-down z-0"
        }
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)), url(${template.logo})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "contain",
          backgroundPosition: "center, center",
        }}
        data-testid="template-logo"
      />
      <span
        className={
          "relative bottom-10 z-20 left-4 font-semibold capitalize text-white text-xl"
        }
      >
        {template.name}
      </span>
      <div className={"-mt-5 h-20 line-clamp-4 text-sm mx-2 px-2"}>
        {template.description}
      </div>
      <div className={"flex flex-row justify-between"}>
        <span className={"p-4 uppercase tracking-wider font-medium"}>view</span>
        <span
          className={"p-4 uppercase tracking-wider font-medium text-btn-grn"}
        >
          deploy
        </span>
      </div>
    </div>
  );
};

export default TemplateCard;
