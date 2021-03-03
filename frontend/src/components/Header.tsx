import ChevronDown from "../icons/ChevronDown";
import YachtLogo from "../icons/YachtLogo";
import { User } from "../utils";

interface OwnProps {
  user: User;
}

const Header = ({ user }: OwnProps) => {
  return (
    <div
      className={"flex flex-row justify-between p-4 text-black dark:text-white bg-header-lgt dark:bg-header-drk"}
      style={{ height: "64px" }}
    >
      <div className={"flex flex-row text-xl"}>
        <YachtLogo /> <span className={"ml-2"}>Yacht</span>
      </div>
      <span className={"font-bold text-xl"}>Home</span>
      <div
        className={"btn"}
        style={{ backgroundColor: "#41B883", height: "36px" }}
      >
        {user.username}
        <ChevronDown />
      </div>
    </div>
  );
};

export default Header;
