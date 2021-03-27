import React from "react";
import { render, screen } from "@testing-library/react";
import Templates from "../../../../components/Content/pages/Templates";

describe("<Templates /> tests", () => {
  it("should render the templates page", () => {
    render(<Templates />);
    const templatesHeader = screen.getByText(/templates/i);
    expect(templatesHeader).toBeInTheDocument();
  });

  // TODO: Once templates are simplified a bit, test that the cards get rendered
});
