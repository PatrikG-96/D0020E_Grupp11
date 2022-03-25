/**
 * * authHeader
 * retreives the accessToken stored with the user in order to access API
 *
 */
function authHeader() {
  const user = JSON.parse(localStorage.getItem("user"));

  if (user && user.accessToken) {
    //console.log("[AUTH TOKEN]:" + user.accessToken);
    return { "x-auth-token": user.accessToken };
  } else {
    //console.log("[NO AUTH TOKEN]:");
    return {};
  }
}

export default authHeader;
