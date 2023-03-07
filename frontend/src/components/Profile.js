import React, { useContext} from "react";
import { AuthContext } from "react-oauth2-code-pkce";

const Profile = () => {
  const { token, idTokenData, loginInProgress } = useContext(AuthContext)

  if (loginInProgress) {
    return <div>Loading ...</div>;
  }

  return (
    token.length > 0 && (
      <div>
        <img src={idTokenData?.picture} alt={idTokenData?.name} />
        <h2>{idTokenData?.name}</h2>
        <p>{idTokenData?.email}</p>
        <p>{JSON.stringify(idTokenData, null, 2)}</p>
      </div>
    )
  );
};

export default Profile;