import React from "react";
import { Outlet, useNavigate } from "react-router-dom";

import { AuthProvider } from "react-oauth2-code-pkce"

export const OAuthProviderWithNavigate = ({ children }) => {
  const navigate = useNavigate();


  const authConfig = {
    clientId: process.env.REACT_APP_OAUTH_CLIENT_ID,
    authorizationEndpoint: process.env.REACT_APP_OAUTH_DOMAIN + process.env.REACT_APP_OAUTH_TOKEN_ENDPOINT,
    tokenEndpoint: window.location.origin + '/api/token',
    redirectUri: window.location.origin,
    scope: 'email openid profile',
    onRefreshTokenExpire: (event) => window.confirm('Session expired. Refresh page to continue using the site?') && event.login(),
    preLogin: () => localStorage.setItem('preLoginPath', window.location.pathname),
    postLogin: () => navigate(localStorage.getItem('preLoginPath') || ''),
    autoLogin: true
  }

  return (
    <AuthProvider authConfig={authConfig}>
      {<Outlet /> || children}
    </AuthProvider>
  );
};