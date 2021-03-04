import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import "./index.css";
import AppsTable from "./components/AppsTable";
import { RecoilRoot } from 'recoil';
import reportWebVitals from "./reportWebVitals";
import Header from "./components/Header";
import { mockUser } from "./utils";
import Test from "./components/Test";

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <RecoilRoot>
        <Header user={mockUser} />
        <Switch>
        <Route path="/test" component={Test} />
        <Route path="/apps" component={AppsTable} />
        </Switch>
      </RecoilRoot>
    </Router>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
