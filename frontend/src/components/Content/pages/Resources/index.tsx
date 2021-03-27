import clsx from "clsx";
import React, { useState } from "react";
import ContentWrapper from "../../ContentWrapper";
import Images from "./Images";
import Networks from "./Networks";
import Volumes from "./Volumes";

enum ResourcesView {
  IMAGES = "IMAGES",
  VOLUMES = "VOLUMES",
  NETWORKS = "NETWORKS",
}

const Resources = () => {
  const [currentView, setCurrentView] = useState(ResourcesView.IMAGES);

  const renderView = () => {
    switch (currentView) {
      case ResourcesView.VOLUMES: {
        return <Volumes />;
      }
      case ResourcesView.NETWORKS: {
        return <Networks />;
      }
      default: {
        return <Images />;
      }
    }
  };

  return (
    <ContentWrapper header={"Resources"}>
      <div
        className={
          "flex flex-row text-sm text-white uppercase font-semibold tracking-widest"
        }
        data-testid={"tabbed-nav-container"}
      >
        <div
          className={clsx(
            "content-tabbed-nav",
            currentView === ResourcesView.IMAGES && "border-b-2 border-btn-grn"
          )}
          onClick={() => setCurrentView(ResourcesView.IMAGES)}
        >
          Images
        </div>
        <div
          className={clsx(
            "content-tabbed-nav",
            currentView === ResourcesView.VOLUMES && "border-b-2 border-btn-grn"
          )}
          onClick={() => setCurrentView(ResourcesView.VOLUMES)}
        >
          Volumes
        </div>
        <div
          className={clsx(
            "content-tabbed-nav",
            currentView === ResourcesView.NETWORKS &&
              "border-b-2 border-btn-grn"
          )}
          onClick={() => setCurrentView(ResourcesView.NETWORKS)}
        >
          Networks
        </div>
      </div>
      <div className={"p-2"} data-testid={"view-container"}>
        {renderView()}
      </div>
    </ContentWrapper>
  );
};

export default Resources;
