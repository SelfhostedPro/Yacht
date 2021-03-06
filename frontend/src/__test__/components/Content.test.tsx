import React from "react";
import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";

import Content from "../../components/Content";

describe("<Content /> tests", () => {
  it("should render content for the app", () => {
    render(
      <Router>
        <Content />
      </Router>
    );

    const content = screen.getByTestId("app-content");
    expect(content).toBeInTheDocument();
  });
});
