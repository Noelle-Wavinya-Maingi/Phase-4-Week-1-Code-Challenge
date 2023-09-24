import { Route, Router } from "react-router";
import Home from "./Home";
import Navbar from "./Navbar";
import Restaurant from "./Restaurant";

function App() {
  return (
    <>
      <Navbar />
      <Router>
        <Route exact path="/restaurants/:id">
          <Restaurant />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
      </Router>
    </>
  );
}

export default App;
