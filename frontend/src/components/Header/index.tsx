import React from "react";
import ChevronDown from "../../icons/ChevronDown";
import YachtLogo from "../../icons/YachtLogo";
import { User } from "../../utils";


interface OwnProps {
  user: User;
}

const Header = ({ user }: OwnProps) => {
  return (
    <div className={"header mat-ui-shadow"} data-testid={"app-header"}>
      <div className={"flex flex-row justify-between"}>
        <div className={"flex flex-row text-xl"}>
          <YachtLogo /> <span className={"ml-2 hidden xs:block"}>Yacht</span>
        </div>
        <span className={"font-bold text-xl hidden md:block"}>Home</span>
        <div
          className={"btn mat-ui-shadow"}
          style={{ backgroundColor: "#41B883", height: "36px" }}
        >
          <span className={"hidden sm:block"}>{user.username}</span>
          <ChevronDown />
        </div>
      </div>
    </div>
  );
};

export default Header;
