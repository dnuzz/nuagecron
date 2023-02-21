import { useRouteError } from "react-router-dom";
import React from 'react';

export default function ErrorPage() {
    const error = useRouteError();
    console.error(error);
  
    return (
      <div id="error-page">
        <h1>Oops!</h1>
        <p>Sorry, an unexpected error has occurred.</p>
        <p>
          <i>{error.statusText}</i>
          <b>{error.message}</b>
          <p>Chaos Stacktrace below</p>
          <i>{error.stack}</i>
        </p>
      </div>
    );
  }
