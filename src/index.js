import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import ReactDOM from "react-dom";
import "bootstrap/dist/css/bootstrap.css";
import "remixicon/fonts/remixicon.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./index.css";
import store from "./store/store";
import { Provider } from "react-redux";
import { BrowserRouter as Router } from "react-router-dom";

const rootElement = document.getElementById("root");

const app = (
  <React.StrictMode>
    <Router>
      <Provider store={store}>
        <App />
      </Provider>
    </Router>
  </React.StrictMode>
);

// Check if the browser supports React 18's createRoot API
const supportsCreateRoot = typeof createRoot === "function";

// Render the app accordingly
if (supportsCreateRoot) {
  const root = createRoot(rootElement);
  root.render(app);
} else {
  // Fallback to ReactDOM.render if createRoot is not supported
  ReactDOM.render(app, rootElement);
}
