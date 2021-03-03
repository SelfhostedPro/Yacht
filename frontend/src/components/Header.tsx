import ChevronDown from "../icons/ChevronDown";
import YachtLogo from "../icons/YachtLogo";
import { User } from "../utils";

interface OwnProps {
  user: User;
}

const Header = ({ user }: OwnProps) => {
  return (
    <div className={"header mat-ui-shadow"}>
      <div className={"flex flex-row text-xl"}>
        <YachtLogo /> <span className={"ml-2"}>Yacht</span>
      </div>
      <span className={"font-bold text-xl"}>Home</span>
      <div
        className={"btn mat-ui-shadow"}
        style={{ backgroundColor: "#41B883", height: "36px" }}
      >
        {user.username}
        <ChevronDown />
      </div>
    </div>
  );
};

export default Header;
