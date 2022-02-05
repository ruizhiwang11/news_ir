import React, { Component } from "react";
import { render } from "react-dom";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <p className='center'>
        You can write your frontend code here
      </p>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);