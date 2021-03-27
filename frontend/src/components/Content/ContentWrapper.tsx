import React, { FC } from "react";

interface OwnProps {
  header: string;
}

const ContentWrapper: FC<OwnProps> = ({ header, children }) => {
  return (
    <div className={"content-wrapper"}>
      <div
        className={
          "text-black dark:text-white text-3xl bg-content-header rounded-t p-4"
        }
      >
        {header}
      </div>
      <div
        className={
          "content dark:text-white text-black p-2 overflow-y-auto whitespace-normal"
        }
      >
        {children}
      </div>
    </div>
  );
};

export default ContentWrapper;
