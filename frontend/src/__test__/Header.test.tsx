import React from "react";
import { render, screen } from "@testing-library/react";

import Header from "../components/Header";
import YachtLogo from "../icons/YachtLogo";
import { mockUser } from "../utils";


describe("<Header />", () => {
  it("should render the Yacht logo & text", () => {
    render(<Header user={mockUser} />);
    const username = screen.getByText(/admin@yacht.local/i);
    const homeText = screen.getByText(/home/i);
    const yachtText = screen.getByText(/yacht/i);

    expect(homeText).toBeInTheDocument();
    expect(yachtText).toBeInTheDocument();
    expect(username).toBeInTheDocument();
    expect(YachtLogo).toBeInTheDocument();
  });
});
