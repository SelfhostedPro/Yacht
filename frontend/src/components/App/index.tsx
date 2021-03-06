import { mockUser } from "../../utils";
import Content from "../Content";
import Header from "../Header";
import Nav from "../Nav";

const App = () => {
   return (
    <div className={"app-container"} data-testid={"app-container"}>
      <Header user={mockUser} />
      <Nav />
      <Content />
    </div>
  );
};

export default App;
