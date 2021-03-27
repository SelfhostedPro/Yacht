import { render, screen } from "@testing-library/react";
import React from "react";
import { TemplateList } from "../../../../components/Content/pages/Templates";
import TemplateCard from "../../../../components/Content/pages/Templates/TemplateCard";

const testTemplate = {
  id: 1,
  logo: "#",
  name: "testTemplate",
  description:
    "This is a test template, there are many like it but this one is mine",
} as TemplateList;

describe("<TemplateCard /> tests", () => {
  it("should render a template card with given information", () => {
    render(<TemplateCard template={testTemplate} />);
    const name = screen.getByText(/testtemplate/i);
    const desc = screen.getByText(/this is a test template/i);
    const logo = screen.getByTestId("template-logo");

    expect(name).toBeInTheDocument();
    expect(desc).toBeInTheDocument();
    expect(logo).toBeInTheDocument();
  });
});
