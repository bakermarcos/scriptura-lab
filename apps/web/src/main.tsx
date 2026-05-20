import React from "react";
import ReactDOM from "react-dom/client";
import { MantineProvider, createTheme } from "@mantine/core";

import App from "./App";
import "@mantine/core/styles.css";
import "@fontsource/newsreader/latin-400.css";
import "@fontsource/newsreader/latin-600.css";
import "@fontsource/source-sans-3/latin-400.css";
import "@fontsource/source-sans-3/latin-600.css";
import "./styles.css";

const theme = createTheme({
  fontFamily: '"Source Sans 3", sans-serif',
  headings: {
    fontFamily: '"Newsreader", serif',
    fontWeight: "600",
  },
  primaryColor: "red",
  defaultRadius: "sm",
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <MantineProvider theme={theme}>
      <App />
    </MantineProvider>
  </React.StrictMode>,
);
