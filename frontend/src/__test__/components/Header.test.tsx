import React from "react";
import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";

import Header from "../../components/Header";
import { mockUser } from "../../utils";

describe("<Header /> tests", () => {
  it("should render the Yacht logo & text", () => {
    render(
      <Router>
        <Header user={mockUser} />
      </Router>
    );

    const username = screen.getByText(/admin@yacht.local/i);
    const homeText = screen.getByText(/home/i);
    const yachtText = screen.getByText(/^yacht/i);
    const yachtLogo = screen.getByTestId("yacht-logo");

    expect(homeText).toBeInTheDocument();
    expect(yachtText).toBeInTheDocument();
    expect(username).toBeInTheDocument();
    expect(yachtLogo).toBeInTheDocument();
  });
});
