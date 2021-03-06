import { Link } from "react-router-dom";

interface navLink {
  label: string;
  route: string;
}

interface extLink {
  label: string;
  uri: string;
}

export const navLinks: navLink[] = [
  { label: "dash", route: "/" },
  { label: "apps", route: "/apps" },
  { label: "tmpl", route: "/templates" },
  { label: "proj", route: "/projects" },
  { label: "rsrc", route: "/resources" },
  { label: "stgs", route: "/settings" },
];

const bottomLinks: extLink[] = [
  { label: "yacht", uri: "https://yacht.sh" },
  { label: "github", uri: "https://github.com/SelfHostedPro/Yacht" },
];

const Nav = () => {
  return (
    <div className={"nav"} data-testid={"app-nav"}>
      <div className={"side-nav"}>
        <div
          className={
            "flex flex-col justify-between text-black dark:text-white bg-header-lgt dark:bg-header-drk inset-x-0 top-0 h-full w-14 p-2"
          }
        >
          <ul>
            {navLinks.map((link, index) => (
              <div key={`link-${index}`}>
                <Link
                  
                  to={link.route}
                  data-testid={"nav-link"}
                >
                  <li>{link.label}</li>
                </Link>
                <hr />
              </div>
            ))}
          </ul>
          <ul>
            {bottomLinks.map((link, index) => (
              <li key={index}>
                <a href={link.uri}>{link.label}</a>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className={"bottom-nav"}>
        <div
          className={"flex flex-row justify-around h-full p-4 overflow-auto"}
        >
          {navLinks.map((link, index) => (
            <Link
              key={`link-${index}`}
              to={link.route}
              data-testid={"nav-link"}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Nav;
