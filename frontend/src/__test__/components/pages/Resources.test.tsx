import React from "react";
import { fireEvent, render, screen, within } from "@testing-library/react";
import Resources from "../../../components/Content/pages/Resources";

describe("<Resources /> tests", () => {
  let tabbedNav: HTMLElement;
  let volumes: HTMLElement;
  let images: HTMLElement;
  let networks: HTMLElement;

  beforeEach(() => {
    render(<Resources />);

    tabbedNav = screen.getByTestId("tabbed-nav-container");
    volumes = within(tabbedNav).getByText(/volumes/i);
    images = within(tabbedNav).getByText(/images/i);
    networks = within(tabbedNav).getByText(/networks/i);
  });

  it("should render the resources page", () => {
    const resources = screen.getByText(/resources/i);
    expect(resources).toBeInTheDocument();
  });

  it("should have a tabbed navigation container with links", () => {
    expect(tabbedNav).toBeInTheDocument();
    expect(volumes).toBeInTheDocument();
    expect(images).toBeInTheDocument();
    expect(networks).toBeInTheDocument();
  });

  it("should have working tabbed navigation", () => {
    const viewContainer = screen.getByTestId("view-container");

    fireEvent.click(volumes);

    const volHeader = within(viewContainer).getByText(/volumes/i);
    expect(volHeader).toBeInTheDocument();

    fireEvent.click(images);

    const imgHeader = within(viewContainer).getByText(/images/i);
    expect(imgHeader).toBeInTheDocument();

    fireEvent.click(networks);

    const ntwkHeader = within(viewContainer).getByText(/networks/i);
    expect(ntwkHeader).toBeInTheDocument();
  });
});
