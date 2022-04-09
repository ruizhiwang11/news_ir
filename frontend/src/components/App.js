import React, { Component } from "react";
import { render } from "react-dom";
import SearchPage from "./SearchPage";

function App() {
  return (
    <div className="App">
      <SearchPage />
    </div>
  );
}



export default App;
const appDiv = document.getElementById("app");
render(<App />, appDiv);
